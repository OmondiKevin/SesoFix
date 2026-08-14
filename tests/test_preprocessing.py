"""
Unit tests for preprocessing and leakage-free splitting (src/sesofix/preprocessing.py).
"""

import unittest
from src.sesofix.preprocessing import (
    CanonicalExample,
    normalize_sesotho_text,
    split_dataset_leakage_free
)


class TestPreprocessing(unittest.TestCase):

    def test_normalize_sesotho_text(self):
        self.assertEqual(normalize_sesotho_text("  Ke   rata   ho  bala.  "), "Ke rata ho bala.")
        self.assertEqual(normalize_sesotho_text("“Dijo” le ‘bana’"), "\"Dijo\" le 'bana'")

    def test_split_dataset_leakage_free(self):
        # Create 10 genuine examples across 5 documents
        genuine = [
            CanonicalExample(f"EX_{i}", f"SA {i}", f"LS {i}", "human_verified", "DS03", f"DOC_{i // 2}", False)
            for i in range(10)
        ]
        # Create 4 synthetic examples across 2 documents
        synth = [
            CanonicalExample(f"SYN_{i}", f"SA synth {i}", f"LS synth {i}", "synthetic_rule", "DS01", f"DOC_SYN_{i // 2}", True)
            for i in range(4)
        ]

        train_df, val_df, test_df, audit = split_dataset_leakage_free(
            genuine_examples=genuine,
            synthetic_examples=synth,
            val_ratio=0.2,
            test_ratio=0.2,
            seed=42
        )

        # 1. Check strict zero synthetic leakage in val and test
        self.assertTrue(audit["leakage_check_val_synth_zero"])
        self.assertTrue(audit["leakage_check_test_synth_zero"])
        self.assertEqual(val_df["is_synthetic"].sum(), 0)
        self.assertEqual(test_df["is_synthetic"].sum(), 0)

        # 2. Check document isolation
        val_docs = set(val_df["document_id"])
        test_docs = set(test_df["document_id"])

        # Val and test docs should not overlap with each other
        self.assertEqual(len(val_docs.intersection(test_docs)), 0)


if __name__ == "__main__":
    unittest.main()
