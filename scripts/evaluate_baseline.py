#!/usr/bin/env python3
"""
Runs a development-only diagnostic for Identity Copy and the candidate Rule Engine.

The 74 references come from one annotator and were exposed during rule
development. Output from this script is not confirmatory test evidence.
"""

import os
import sys
import json
import argparse
from typing import Dict
import pandas as pd

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.sesofix.rules import SesothoRuleEngine
from src.sesofix.metrics import compute_all_metrics
from src.sesofix.preprocessing import load_common_voice_verification


def evaluate_baselines(xlsx_path: str, output_json: str = "results/baseline_results.json") -> Dict:
    """
    Evaluates:
    1. Identity Copy Baseline
    2. Rule Engine Baseline
    on the legacy single-annotator Common Voice development sentences.
    """
    verified_pairs, _ = load_common_voice_verification(xlsx_path)
    print(f"Loaded {len(verified_pairs)} legacy development pairs from {xlsx_path}")

    sources = [ex.source_text for ex in verified_pairs]
    references = [ex.target_text for ex in verified_pairs]

    engine = SesothoRuleEngine()
    rule_predictions = []
    rule_traces = []

    for src in sources:
        pred, rules = engine.convert(src)
        rule_predictions.append(pred)
        rule_traces.append(rules)

    # 1. Identity Copy Metrics
    identity_metrics = compute_all_metrics(
        predictions=sources, references=references, sources=sources
    )

    # 2. Rule Engine Metrics
    rule_metrics = compute_all_metrics(
        predictions=rule_predictions, references=references, sources=sources
    )

    results = {
        "dataset_source": "Southern Sesotho Sentence Verification (Common Voice)",
        "evaluation_role": "development_only_exposed_to_rule_development",
        "reference_status": "single_annotator_not_independently_reviewed",
        "num_development_pairs": len(verified_pairs),
        "identity_copy": identity_metrics,
        "rule_based_engine": rule_metrics,
    }

    os.makedirs(os.path.dirname(output_json) if os.path.dirname(output_json) else ".", exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print("DEVELOPMENT-ONLY DIAGNOSTIC (n = 74 Single-Annotator Pairs)")
    print("=" * 60)
    print(f"{'Metric':<25} | {'Identity Copy':<15} | {'Rule-Based':<15}")
    print("-" * 60)
    print(f"{'SacreBLEU ↑':<25} | {identity_metrics['sacrebleu']:<15} | {rule_metrics['sacrebleu']:<15}")
    print(f"{'chrF++ ↑':<25} | {identity_metrics['chrfpp']:<15} | {rule_metrics['chrfpp']:<15}")
    print(f"{'Avg CED ↓':<25} | {identity_metrics['avg_ced']:<15} | {rule_metrics['avg_ced']:<15}")
    print(f"{'Corpus CER (%) ↓':<25} | {identity_metrics['corpus_cer_pct']:<15} | {rule_metrics['corpus_cer_pct']:<15}")
    print(f"{'Corpus WER (%) ↓':<25} | {identity_metrics['corpus_wer_pct']:<15} | {rule_metrics['corpus_wer_pct']:<15}")
    print(f"{'Exact Match (%) ↑':<25} | {identity_metrics['exact_match_pct']:<15} | {rule_metrics['exact_match_pct']:<15}")
    print(f"{'Changed EM (%) ↑':<25} | {identity_metrics['changed_exact_match_pct']:<15} | {rule_metrics['changed_exact_match_pct']:<15}")
    print(f"{'No-change preserve (%) ↑':<25} | {identity_metrics['no_change_preservation_pct']:<15} | {rule_metrics['no_change_preservation_pct']:<15}")
    print("=" * 60)
    print(f"Results written to: {output_json}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Run legacy development diagnostics; not a test evaluation.")
    parser.add_argument(
        "--verification_file",
        type=str,
        default="data/raw/common_voice_verification/Southern_Sesotho_Sentence_Verification.xlsx",
        help="Path to Southern Sesotho Sentence Verification Excel workbook"
    )
    parser.add_argument(
        "--output_json",
        type=str,
        default="results/baseline_results.json",
        help="Output path for baseline metrics JSON"
    )
    args = parser.parse_args()

    evaluate_baselines(args.verification_file, args.output_json)


if __name__ == "__main__":
    main()
