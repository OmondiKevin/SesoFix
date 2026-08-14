"""SesoFix data, diagnostics, and evaluation utilities.

The local package does not train models. Supervised experiments are prepared for
and executed in Google Colab after benchmark manifests are frozen.
"""

__version__ = "0.2.0"

from .rules import SesothoRuleEngine, Rule, apply_rules
from .metrics import compute_all_metrics, character_edit_distance, word_error_rate
from .preprocessing import load_canonical_data, split_dataset_leakage_free, CanonicalExample
from .pilot_sampling import select_pilot, validate_pilot

__all__ = [
    "SesothoRuleEngine",
    "Rule",
    "apply_rules",
    "compute_all_metrics",
    "character_edit_distance",
    "word_error_rate",
    "load_canonical_data",
    "split_dataset_leakage_free",
    "CanonicalExample",
    "select_pilot",
    "validate_pilot",
]
