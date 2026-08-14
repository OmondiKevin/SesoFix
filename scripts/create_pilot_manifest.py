#!/usr/bin/env python3
"""Freeze the development-only 200-sentence annotation pilot manifest."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.sesofix.pilot_sampling import DEFAULT_SEED, select_pilot, validate_pilot


def load_pending(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return [row for row in rows if row.get("status") == "pending"]


def write_manifest(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    public_fields = [
        "release",
        "pilot_id",
        "sentence_id",
        "source_sha256",
        "sample_role",
        "selection_stratum",
        "source_name",
        "up_votes",
        "down_votes",
        "token_count",
        "primary_order",
        "reviewer_order",
        "selection_seed",
        "algorithm_version",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=public_fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows({key: record[key] for key in public_fields} for record in records)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pending-tsv", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--workbook-input-json", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    records = select_pilot(load_pending(args.pending_tsv), seed=args.seed)
    summary = validate_pilot(records)
    write_manifest(args.manifest, records)

    args.workbook_input_json.parent.mkdir(parents=True, exist_ok=True)
    with args.workbook_input_json.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    with args.summary_json.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
