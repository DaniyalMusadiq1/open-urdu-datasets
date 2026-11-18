"""Ingest rights-cleared source JSONL locally; never upload automatically."""
import argparse
import json
from urdu_data.phase2 import build


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSONL records with rights evidence")
    parser.add_argument("output", help="New local output directory")
    parser.add_argument("--shard-records", type=int, default=50000)
    args = parser.parse_args()
    print(json.dumps(build(args.input, args.output,
                           max_records_per_shard=args.shard_records), indent=2))


if __name__ == "__main__":
    main()
