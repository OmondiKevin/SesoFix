#!/usr/bin/env python3
"""
CLI script to apply SesoFix rule-based orthographic harmonization.
Converts South African Sesotho text to Lesotho Sesotho text.
"""

import os
import sys
import argparse

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.sesofix.rules import SesothoRuleEngine


def main():
    parser = argparse.ArgumentParser(description="Convert South African Sesotho to Lesotho Sesotho using linguistic rules.")
    parser.add_argument("--text", type=str, default=None, help="Input sentence in South African Sesotho")
    parser.add_argument("--input_file", type=str, default=None, help="Path to input text file (one sentence per line)")
    parser.add_argument("--output_file", type=str, default=None, help="Path to output text file")
    parser.add_argument("--verbose", action="store_true", help="Print applied rule trace")
    args = parser.parse_args()

    engine = SesothoRuleEngine()

    if args.text:
        converted, rules = engine.convert(args.text)
        print(f"Source: {args.text}")
        print(f"Target: {converted}")
        if args.verbose and rules:
            print(f"Applied Rules: {', '.join(rules)}")
        return

    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f]

        outputs = []
        for line in lines:
            if not line:
                outputs.append("")
                continue
            conv, _ = engine.convert(line)
            outputs.append(conv)

        if args.output_file:
            with open(args.output_file, "w", encoding="utf-8") as f:
                for out in outputs:
                    f.write(out + "\n")
            print(f"Wrote {len(outputs)} converted lines to {args.output_file}")
        else:
            for out in outputs:
                print(out)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
