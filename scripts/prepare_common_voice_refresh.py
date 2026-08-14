#!/usr/bin/env python3
"""Build a lossless Common Voice refresh package; performs no model training."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.sesofix.common_voice_refresh import prepare_refresh


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inventory a Common Voice archive and strictly match the legacy workbook."
    )
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--release", required=True)
    parser.add_argument(
        "--legacy-workbook",
        type=Path,
        default=Path(
            "data/raw/common_voice_verification/"
            "Southern_Sesotho_Sentence_Verification.xlsx"
        ),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    summary = prepare_refresh(
        archive_path=args.archive,
        legacy_workbook=args.legacy_workbook,
        release=args.release,
        output_dir=args.output_dir,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
