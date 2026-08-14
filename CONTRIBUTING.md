# Contributing to SesoFix

SesoFix is an active research benchmark, so evidence lineage matters as much as
code correctness.

## Local setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
make test
```

Local dependencies cover data preparation and metrics only. Do not add local
training commands or commit model weights, raw data, collaborator workbooks, API
outputs, or credentials.

## Contribution rules

- Preserve raw source and human target text; transformations belong in separate
  derived fields.
- Add dataset IDs, release/version, licenses, and checksums to provenance docs.
- Never label machine output as human gold.
- Do not use final-test items for rule, prompt, example, or hyperparameter design.
- Treat the 74 legacy references as development-only.
- Add deterministic tests for data or metric changes.
- Update `WORKPLAN.md` when a research gate changes status.
- Update `paper/PAPER_OUTLINE.md` only with evidence-backed structure or results.
- Run supervised model training only through reviewed Google Colab notebooks.

## Pull requests

Explain what changed, why it is scientifically safe, which artifacts were
affected, and which checks were run. Flag any change to sampling, normalization,
annotation eligibility, metrics, prompts, or split membership prominently.

Repository code contributions use the project license. Dataset and annotation
rights remain source-specific.
