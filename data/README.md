# SesoFix data organization and safeguards

## Data policy

1. Raw downloads are immutable and are never committed to Git.
2. Every raw archive must have provider, release, download date, license, and
   SHA-256 metadata before processing.
3. Intermediate tables and annotation exports remain untracked until their
   release/licensing decision is explicit.
4. Human targets are append-only: a merge may attach provenance or review fields
   but may not replace a non-empty human target.
5. No machine output is labeled as human gold.
6. The 74 existing targets are permanently development-only because they were
   visible during rule development.
7. Training artifacts are prepared locally but model training is run only in
   Google Colab.

## Local layout

```text
data/
├── README.md
├── DATA_MANIFEST.csv
├── manifests/                        # tracked IDs/hashes only; no target text
├── incoming/                         # untouched downloads; ignored
│   └── common_voice/<release>/
├── raw/                              # immutable extracted sources; ignored
│   └── common_voice_verification/    # legacy workbook
├── interim/                          # inventories and merge quarantine; ignored
├── annotations/                      # working human annotation exports; ignored
└── processed/                        # frozen manifests and model-ready data; ignored
```

## Canonical sentence identity

Common Voice releases can repeat a sentence across TSVs and releases. Canonical
identity therefore retains all of the following rather than trusting one field:

| Field | Purpose |
|---|---|
| `example_id` | Stable project-generated ID |
| `cv_sentence_id` | Provider sentence ID when supplied |
| `source_text_raw` | Untouched provider text |
| `source_text_nfc` | Unicode-NFC text; no linguistic rewriting |
| `source_sha256_raw` | Exact-byte lineage |
| `source_sha256_match` | NFC/whitespace matching only |
| `cv_release` | Common Voice release/version |
| `source_appearances` | Every TSV/split containing the sentence |
| `legacy_match_method` | ID, raw text, normalized text, manual, or unmatched |

## Canonical annotation record

| Field | Purpose |
|---|---|
| `target_text_raw` | Human Lesotho Sesotho adaptation |
| `decision` | `CHANGE`, `NO_CHANGE`, or exclusion reason |
| `exact_copy_derived` | Computed from source/target; not a human similarity label |
| `annotation_stage` | primary, review, or adjudicated |
| `single_annotator_reference` | True until independent review exists |
| `exposed_to_rule_development` | Permanent contamination marker |
| `legacy_workbook_row` | Exact original row for forensic recovery |
| `target_was_formula` | Whether the original target cell used a formula |
| `review_status` | pending, agreed, disagreed, or adjudicated |

The active merge protocol is [documented here](../docs/COMMON_VOICE_REFRESH.md).

The Common Voice 26.0 source archive and extracted files are stored locally under
`data/incoming/common_voice/cv-corpus-26.0-2026-06-12/`. Annotation workbooks are
generated under `outputs/` and remain untracked so human work is never committed
accidentally.
