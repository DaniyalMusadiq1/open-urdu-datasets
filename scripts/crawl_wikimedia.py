"""Collect a small, explicitly scoped Urdu web corpus; no recursive crawling."""
import argparse
import gzip
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urljoin, urlsplit
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

from lxml import html

AGENT = "OpenUrduDatasets/0.0 (https://github.com/DaniyalMusadiq1/open-urdu-datasets)"
SEEDS = [
    "https://ur.wikisource.org/wiki/قواعد_تذکیر_و_تانیث",
    "https://ur.wikisource.org/wiki/دیوان_غالب/غزلیات/ردیف_ے",
    "https://ur.wikipedia.org/wiki/اردو_قواعد",
]
HOSTS = {"ur.wikisource.org", "ur.wikipedia.org"}
LIMIT = 3_000_000


def digest(data):
    return hashlib.sha256(data).hexdigest()


def allowed_url(url):
    part = urlsplit(url)
    return (part.scheme == "https" and part.netloc in HOSTS
            and part.path.startswith("/wiki/") and not part.query and not part.fragment)


def fetch(url):
    request = Request(quote(url, safe=":/?=&%"), headers={
        "User-Agent": AGENT, "Accept-Encoding": "gzip"})
    with urlopen(request, timeout=45) as response:
        stream = (gzip.GzipFile(fileobj=response)
                  if response.headers.get("Content-Encoding") == "gzip" else response)
        body = stream.read(LIMIT + 1)
        if len(body) > LIMIT:
            raise ValueError("response size limit")
        return body, response.geturl(), response.headers.get_content_type()


def extract(body, url):
    tree = html.fromstring(body, parser=html.HTMLParser(encoding="utf-8"))
    footer = tree.xpath('//*[@id="footer-info-copyright"]')
    if (not footer or "Terms_of_Use" not in html.tostring(footer[0]).decode()
            or not any(label in footer[0].text_content()
                       for label in ["کریئیٹیو", "Creative Commons"])):
        raise ValueError("missing Wikimedia licensing notice")
    revisions = tree.xpath('//a[contains(@href,"oldid=")]/@href')
    revision = next((parse_qs(urlsplit(h).query).get("oldid", [None])[0]
                     for h in revisions if "oldid=" in h), None)
    if not revision or not revision.isdigit():
        raise ValueError("missing revision provenance")
    nodes = tree.xpath('//*[contains(concat(" ", normalize-space(@class), " "),'
                       ' " mw-parser-output ")]')
    if not nodes:
        raise ValueError("missing article body")
    node = nodes[0]
    for item in node.xpath('.//script|.//style|.//*[contains(@class,"mw-editsection")'
                           ' or contains(@class,"navbox") or @id="toc"'
                           ' or contains(@class,"metadata") or contains(@class,"noprint")]'):
        parent = item.getparent()
        if parent is not None:
            parent.remove(item)
    text = "\n".join(line.strip() for line in node.text_content().splitlines() if line.strip())
    if len(re.findall(r"[\u0600-\u06ff]", text)) < 100:
        raise ValueError("insufficient Arabic-script content")
    canonical = tree.xpath('//link[@rel="canonical"]/@href')
    source_url = canonical[0] if canonical else url
    if not allowed_url(source_url):
        raise ValueError("unexpected canonical URL")
    return {
        "id": digest(text.encode()), "text": text,
        "title": tree.xpath('string(//*[@id="firstHeading"])').strip(),
        "source": {"url": source_url, "revision_id": int(revision),
                   "revision_url": urljoin(url, "/w/index.php") + "?oldid=" + revision,
                   "history_url": urljoin(url, "/w/index.php") + "?title="
                   + quote(unquote(urlsplit(source_url).path.removeprefix("/wiki/"))) + "&action=history",
                   "response_sha256": digest(body)},
        "license": "CC-BY-SA-4.0", "review_status": "unreviewed",
        "attribution": "Original authors and Wikimedia contributors; see source revision and history",
        "changes": "HTML markup/navigation removed; blank lines omitted and line edges trimmed; no translation or spelling correction",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    robots = {}
    evidence = []
    rows = []
    for url in SEEDS:
        if not allowed_url(url):
            raise ValueError("seed outside allowlist")
        host = urlsplit(url).netloc
        if host not in robots:
            body, final, _ = fetch("https://" + host + "/robots.txt")
            if urlsplit(final).netloc != host:
                raise ValueError("robots redirect outside host")
            policy = RobotFileParser()
            policy.parse(body.decode("utf-8-sig").splitlines())
            robots[host] = policy
            (args.output / (host + "-robots.txt")).write_bytes(body)
            time.sleep(2)
        if not robots[host].can_fetch(AGENT, quote(url, safe=":/%")):
            raise ValueError("robots disallows " + url)
        body, final, kind = fetch(url)
        if not allowed_url(final) or kind != "text/html":
            raise ValueError("unexpected page response")
        row = extract(body, final)
        row["date_accessed"] = datetime.now(timezone.utc).date().isoformat()
        if row["id"] in {r["id"] for r in rows}:
            raise ValueError("duplicate page text")
        rows.append(row)
        evidence.append({"url": url, "final_url": final, "robots_allowed": True,
                         "response_sha256": digest(body), "revision_id": row["source"]["revision_id"]})
        print(json.dumps({"url": url, "characters": len(row["text"])}), flush=True)
        time.sleep(2)
    payload = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode()
    (args.output / "documents.jsonl.gz").write_bytes(gzip.compress(payload, mtime=0))
    manifest = {"documents": len(rows), "whitespace_tokens": sum(len(r["text"].split()) for r in rows),
                "human_reviewed_records": 0, "date_accessed": rows[0]["date_accessed"],
                "data_sha256": digest((args.output / "documents.jsonl.gz").read_bytes()),
                "crawl": {"recursive": False, "max_pages": len(SEEDS), "delay_seconds": 2,
                          "user_agent": AGENT, "pages": evidence},
                "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
                "terms_url": "https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use"}
    (args.output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"documents": len(rows), "whitespace_tokens": manifest["whitespace_tokens"]}))


if __name__ == "__main__":
    main()
