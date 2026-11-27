"""Generate paired, unreviewed Klam Chat candidates with a local Ollama model."""
import argparse
import json
import re
import sqlite3
import tempfile
import unicodedata
import urllib.request
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1] / "training" / "klam-chat"
SPLITS = ("train", "validation", "test")
SCRIPTS = ("Arab", "Latn")
ARABIC = re.compile(r"[\u0620-\u06ff]")
LATIN = re.compile(r"[A-Za-z]")
TOPICS = (
    "school and study", "workplace communication", "travel logistics",
    "household organization", "libraries and community events",
    "digital literacy", "everyday scheduling", "shopping and comparisons",
)


def key(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def generate(model, task, topic, sequence, timeout):
    prompt = (
        f"Write one original everyday assistant scenario in Pakistani Urdu. "
        f"Task: {task}. Topic: {topic}. Scenario sequence: {sequence}. "
        "Return JSON with keys Arab and Latn, each an array of message objects with "
        "role and content only. Use Urdu script for Arab and natural Roman Urdu for Latn. "
        "Both versions must convey the same scenario and answer. Start with user, "
        "alternate with assistant, and end with assistant. Use two or four messages "
        "per array. Vary the situation, style, wording, and difficulty. Avoid real "
        "personal data, copied text, and unsupported claims about current events."
    )
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps({
            "model": model, "prompt": prompt, "format": "json", "stream": False,
        }).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(json.load(response)["response"])


def candidate_rows(candidate, task, group, validator):
    if not isinstance(candidate, dict) or set(candidate) != set(SCRIPTS):
        raise ValueError("Expected one Arabic-script and one Roman Urdu conversation")
    rows = []
    for script in SCRIPTS:
        row = {
            "id": f"{group}-{script}", "group_id": group, "language": "ur",
            "script": script, "task": task, "source": "original-ai-generated",
            "license": "CC0-1.0", "review_status": "unreviewed",
            "messages": candidate[script],
        }
        error = next(validator.iter_errors(row), None)
        if error is not None:
            raise ValueError(error.message)
        messages = row["messages"]
        if len(messages) not in (2, 4):
            raise ValueError("Expected two or four messages")
        for index, message in enumerate(messages):
            role = "assistant" if index % 2 else "user"
            content = message["content"].strip()
            marker = ARABIC if script == "Arab" else LATIN
            if (message["role"] != role or not marker.search(content)
                    or len(content) > 2000 or (script == "Latn" and ARABIC.search(content))):
                raise ValueError("Invalid role, content length, or script")
            message["content"] = content
        rows.append(row)
    if len(rows[0]["messages"]) != len(rows[1]["messages"]):
        raise ValueError("Paired conversations must have the same turn count")
    return rows


def save_pair(db, rows):
    with db:
        for row in rows:
            db.execute("INSERT INTO prompts VALUES (?)", (key(row["messages"][0]["content"]),))
            db.execute(
                "INSERT INTO candidates VALUES (?, ?)",
                (row["id"], json.dumps(row, ensure_ascii=False)),
            )


def export_release(db, destination, model):
    if destination.exists():
        raise SystemExit(f"Export already exists: {destination}")
    with tempfile.TemporaryDirectory(dir=destination.parent) as scratch:
        staged = Path(scratch) / "release"
        staged.mkdir()
        counts = {}
        for split in SPLITS:
            with (ROOT / f"{split}.jsonl").open(encoding="utf-8") as source:
                with (staged / f"{split}.jsonl").open("w", encoding="utf-8") as output:
                    count = 0
                    for line in source:
                        output.write(line.rstrip("\\n") + "\\n")
                        count += 1
                    if split == "train":
                        for (row,) in db.execute("SELECT row FROM candidates ORDER BY rowid"):
                            output.write(row + "\\n")
                            count += 1
            counts[split] = count
        manifest = {
            "counts": counts, "total": sum(counts.values()),
            "generator_model": model, "generated_review_status": "unreviewed",
        }
        (staged / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\\n", encoding="utf-8"
        )
        staged.rename(destination)
    print(f"Exported {manifest['total']} rows to {destination}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--model", required=True, help="An Ollama model already installed locally")
    parser.add_argument("--target", type=int, default=1_000_000, help="Total rows including the starter")
    parser.add_argument("--max-pairs", type=int, default=100, help="New accepted pairs in this run")
    parser.add_argument("--export", type=Path, help="Export the saved snapshot and exit")
    parser.add_argument("--timeout", type=float, default=120)
    args = parser.parse_args()
    if args.target <= 0 or args.target % 2 or args.max_pairs < 1 or args.timeout <= 0:
        parser.error("Use a positive even target, a positive batch size, and a positive timeout")

    schema = json.loads((ROOT / "schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    tasks = schema["properties"]["task"]["enum"]
    existing = [
        json.loads(line) for split in SPLITS
        for line in (ROOT / f"{split}.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    first_group = 1 + max(int(row["group_id"].removeprefix("chat-")) for row in existing)
    # Keep this database tied to the starter snapshot and generator model.
    metadata = json.dumps({"starter": existing, "model": args.model}, sort_keys=True)
    with sqlite3.connect(args.db) as db:
        db.execute("CREATE TABLE IF NOT EXISTS metadata (snapshot TEXT NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS prompts (prompt TEXT PRIMARY KEY)")
        db.execute("CREATE TABLE IF NOT EXISTS candidates (id TEXT PRIMARY KEY, row TEXT NOT NULL)")
        previous = db.execute("SELECT snapshot FROM metadata").fetchone()
        if previous is None:
            with db:
                db.execute("INSERT INTO metadata VALUES (?)", (metadata,))
                db.executemany(
                    "INSERT INTO prompts VALUES (?)",
                    [(key(row["messages"][0]["content"]),) for row in existing],
                )
        elif previous[0] != metadata:
            parser.error("Database belongs to another starter snapshot or model; use a new database")
        if args.export is not None:
            export_release(db, args.export, args.model)
            return
        completed = db.execute("SELECT count(*) FROM candidates").fetchone()[0] // 2
        wanted = min(args.max_pairs, max(0, (args.target - len(existing)) // 2 - completed))
        accepted = rejected = 0
        while accepted < wanted and rejected < max(10, wanted * 3):
            sequence = completed + accepted
            task = tasks[sequence % len(tasks)]
            topic = TOPICS[(sequence // len(tasks)) % len(TOPICS)]
            try:
                candidate = generate(args.model, task, topic, sequence, args.timeout)
                rows = candidate_rows(candidate, task, f"chat-{first_group + sequence}", validator)
                save_pair(db, rows)
            except (ValueError, KeyError, sqlite3.IntegrityError) as error:
                rejected += 1
                print(f"Candidate rejected: {error}", flush=True)
                continue
            except OSError as error:
                raise SystemExit(f"Ollama unavailable: {error}. Saved pairs can be resumed.") from error
            accepted += 1
        print(f"Saved {accepted} pairs. Total rows: {len(existing) + 2 * (completed + accepted)}")
        if accepted < wanted:
            raise SystemExit("Stopped after repeated invalid or duplicate generations; saved pairs retained")


if __name__ == "__main__":
    main()
