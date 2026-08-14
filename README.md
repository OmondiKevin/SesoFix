# SesoFix

SesoFix is a research project on **cross-standard adaptation from South African
Sesotho to Lesotho Sesotho**. It asks how much human supervision is needed to
adapt internationalized text to the intended written standard and whether that
adaptation improves downstream semantic parsing.

Both written standards are treated as legitimate. The task is adaptation, not
correction of an inferior variety.

## Current evidence

- Common Voice 26.0 provides 2,339 validated South African Sesotho sentences and
  14,837 additional pending sentences.
- All 2,337 legacy workbook sources match the current validated corpus exactly by
  ID and text.
- One bidialectal collaborator supplied 74 Lesotho Sesotho targets: 51 direct
  changed targets and 23 formula-copied no-change targets.
- Those 74 examples were exposed during rule development and remain
  development-only.
- No publishable model comparison, human evaluation, or downstream result exists
  yet. All older numerical claims are archived as unverified legacy material.

## Current phase

The archive and lossless merge are frozen. A deterministic 200-sentence pilot is
ready for blind human annotation from the new pending pool:

- 150 probability-sampled items for prevalence and source-quality estimates;
- 15 short-sentence coverage items;
- 15 downvoted-sentence coverage items; and
- 20 non-government-source coverage items.

The primary collaborator and an independent Lesotho reviewer receive separate,
blinded workbooks. Pilot results will determine the final annotation workload
and benchmark size.

See the [pilot package](docs/PILOT_PACKAGE.md) for the handoff and quality checks,
and [WORKPLAN.md](WORKPLAN.md) for completed and pending tasks.

## Research design

1. **Intrinsic adaptation benchmark:** identity, frozen rules, translation pivot,
   zero-shot/few-shot language models, retrieval/edit templates, ByT5, and mT5
   across a supervision curve.
2. **Downstream internationalization:** a human South African/Lesotho Sesotho
   MASSIVE test subset measuring intent accuracy, slot F1, and frame exact match.

Authoritative documents:

- [Research protocol](docs/RESEARCH_PROTOCOL.md)
- [Common Voice release profile](docs/COMMON_VOICE_RELEASE_26_PROFILE.md)
- [Common Voice merge protocol](docs/COMMON_VOICE_REFRESH.md)
- [Annotation protocol](docs/ANNOTATION_PROTOCOL.md)
- [Pilot package](docs/PILOT_PACKAGE.md)
- [Dataset provenance](docs/DATA_PROVENANCE.md)
- [Evidence audit](docs/REPRODUCIBILITY_STATUS.md)
- [Paper outline](paper/PAPER_OUTLINE.md)

## Execution boundary

**No model training is run locally.** Local work is limited to inventory,
checksums, lossless merging, deterministic sampling, annotation QA, metrics,
tests, and preparing Colab notebooks. All supervised training will run in Google
Colab after evaluation manifests are frozen.

## Repository layout

```text
SesoFix/
├── configs/          # Protocol configuration; not executed-result evidence
├── data/             # Tracked metadata/manifests; raw text remains ignored
├── docs/             # Active protocol, provenance, and audit documents
├── notebooks/legacy/ # Unverified prior notebook, retained for history
├── paper/            # Active paper outline and clearly separated legacy work
├── results/          # Result acceptance policy; no confirmatory results yet
├── scripts/          # Data preparation and diagnostic commands
├── src/sesofix/      # Tested data, metric, rule, and sampling modules
└── tests/            # Engineering tests; not linguistic validation
```

## Local checks

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
make test
```

`make train` intentionally fails: training is Colab-only.

## Licensing

Code is covered by [LICENSE](LICENSE). Third-party dataset and collaborator
annotation rights are recorded separately in `data/DATA_MANIFEST.csv`; the
project does not assert one blanket license over all research data.
