# Human annotation and adjudication protocol

**Draft status:** must be piloted with the primary collaborator and independent
reviewer before production annotation.

## 1. Annotation task

Given a sentence written in South African Sesotho, produce how the same meaning
would naturally be written for a Lesotho Sesotho audience. Preserve meaning,
named entities, numbers, punctuation intent, and register. Do not improve the
content, add information, or paraphrase merely for style.

If the source is already acceptable unchanged in the target standard, copy it
exactly and select `NO_CHANGE`. This is a substantive annotation decision, not a
spreadsheet convenience.

If the source is malformed, not Sesotho, impossible to interpret, or contains
content that cannot be safely adapted, choose the corresponding exclusion label
and explain briefly. Do not guess.

## 2. Required fields

| Field | Meaning |
|---|---|
| `example_id` | Frozen project ID |
| `source_text_raw` | Untouched Common Voice sentence |
| `target_text_raw` | Human Lesotho Sesotho adaptation |
| `decision` | `CHANGE`, `NO_CHANGE`, or exclusion reason |
| `meaning_preserved` | Annotator judgment: yes/no/uncertain |
| `phenomena` | One or more controlled categories; optional during first pass |
| `confidence` | high/medium/low |
| `comment` | Explanation for ambiguity or exclusion |
| `annotator_code` | Project-assigned and project-prefilled pseudonymous identifier |
| `annotation_timestamp` | Actual annotation date in `YYYY-MM-DD` format |

`exact_copy_derived` is computed later from source and target. It is never entered
as a substitute for the human `decision`.

### Annotator codes and dates

The project lead assigns and prefills codes before annotation begins. Annotators
do not guess, create, or edit their own codes:

- `P01` is assigned to the original primary collaborator;
- `R01` is assigned to the first independent reviewer; and
- later independent reviewers receive `R02`, `R03`, and so on.

The private identity-to-code key is held separately from the annotation sheets.
Each annotator receives a separate workbook or sheet copy with the assigned code
already present in every row. The annotator leaves that code unchanged and enters
only the actual date that item was annotated, using `YYYY-MM-DD` (for example,
`2026-08-15`). A row cannot pass workbook QC without both fields.

## 3. Phenomenon taxonomy

The initial taxonomy is revised during the legacy-74 pilot and then frozen:

- lexical choice;
- consonant/digraph spelling;
- vowel sequence or glide spelling;
- word joining/separation;
- noun-class prefix or concord;
- pronoun/demonstrative/possessive form;
- morphology beyond spacing;
- punctuation/capitalization only;
- multiple interacting changes;
- acceptable variation / more than one valid target; and
- source problem or uncertain.

The taxonomy describes human-adjudicated differences. It must not be generated
from rule traces and then used as if it were independent evidence for those
rules.

## 4. Review design

- Primary annotator: the existing bidialectal collaborator, with background and
  dialect exposure documented by self-description.
- Independent reviewer: a Lesotho Sesotho expert who did not see system outputs
  or rule predictions.
- All development, natural-test, and challenge-test items are independently
  reviewed.
- At least 25% of training items are independently reviewed, sampled across
  changed/no-change decisions, length, and phenomena.
- Disagreements are resolved in an adjudication pass. Both original decisions and
  the adjudicated target are retained.
- Reviewers are compensated and authorship/acknowledgment is discussed according
  to their intellectual contribution, not treated as anonymous free labor.

Agreement is reported separately for the change/no-change decision and for
categorical phenomena. Text targets can have multiple valid forms, so raw target
exact match is not a sufficient inter-annotator agreement statistic. The study
will report disagreement types and adjudication rates rather than forcing all
variation into one coefficient.

## 5. Blinding and contamination controls

Annotators and reviewers do not see identity, rule, Google, or language-model
outputs while creating references. Test IDs and targets are inaccessible to
system developers until systems/prompts/configurations are frozen. Any accidental
test exposure is logged and the affected item is replaced before final scoring.

The legacy 74 are explicitly visible development examples. They may be used to
pilot instructions and build the taxonomy, but never to estimate final
generalization.

## 6. Quality-control pass

Before a partition is frozen, verify:

- no blank required fields;
- one source and one adjudicated target per accepted example;
- no formula cells in exported final targets;
- stable IDs and source hashes match the frozen Common Voice inventory;
- `NO_CHANGE` decisions exactly copy the raw source unless the adjudicator
  explicitly documents Unicode/punctuation normalization;
- `CHANGE` decisions actually differ under the documented comparison view;
- duplicates and near-duplicates remain in one partition;
- named entities and numbers are preserved; and
- all exclusions have a reason and are excluded before scoring.

No machine-generated target can be promoted to human gold through automatic
filtering or exact-match agreement with another machine system.
