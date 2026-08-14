# SesoFix result status

There are currently **no confirmatory paper results** in this directory.

`baseline_results.json` records a diagnostic run over the 74 legacy
single-annotator references. Those examples were visible during development of
the candidate rule engine, so the run measures fit to development evidence and
must not be described as test generalization.

The diagnostic implementation also used:

- Hugging Face `evaluate` BLEU, not a recorded SacreBLEU signature;
- default chrF (`word_order=0`), although older text labeled it chrF++; and
- an average of sentence-level WER values, not corpus WER.

The stored numbers are retained for audit history but are not suitable for a
paper table. Future results will use the frozen protocol, SacreBLEU signatures,
raw predictions, dataset/prompt/configuration hashes, model IDs, and paired
uncertainty estimates.

## Result acceptance checklist

A result can be cited only if it includes:

1. frozen evaluation-manifest hash;
2. system name and immutable version/model ID;
3. exact prompt/rule/configuration hash;
4. raw prediction file with one row per frozen ID;
5. metric implementation/version and SacreBLEU signature;
6. execution date and environment;
7. all seeds or stochastic replicates; and
8. a contamination declaration.

Training-run artifacts must originate from Google Colab. Locally generated data
inventories and deterministic diagnostic outputs must be labeled as such.
