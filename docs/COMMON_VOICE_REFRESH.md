# Common Voice refresh and lossless merge

**Current status:** release 26.0 has been hashed, profiled, and merged losslessly.
All 2,337 legacy rows matched exactly, all 74 human targets were preserved, and a
deterministic 200-item development pilot is ready for annotation. See
`COMMON_VOICE_RELEASE_26_PROFILE.md`, `PILOT_PACKAGE.md`, and the manifests under
`data/manifests/` for the recorded evidence.

## Archived source package

The project uses the full **Scripted Speech** archive for **Sesotho (`st`)**, not
Northern Sotho/Sepedi (`nso`). The untouched source package is retained at:

```text
data/incoming/common_voice/cv-corpus-26.0-2026-06-12/
1781705124250-cv-corpus-26.0-2026-06-12-st.tar.gz
```

Its SHA-256 is
`4c1863e94979c75a4dec3f6b479a5f9742b9af9b4b9e063f2d86e89d1eec6436`.
The ignored incoming-data directory also retains the extracted release. Future
release updates must keep:

- the original archive filename;
- the release/version and download date;
- the dataset page or download URL;
- the license/readme files bundled in the archive; and
- any checksum shown by the provider.

Prefer the full locale archive, including clips, if storage permits. At minimum,
the archive must retain every supplied TSV file—typically `validated.tsv`,
`train.tsv`, `dev.tsv`, `test.tsv`, `other.tsv`, and `invalidated.tsv`—plus any
sentence metadata files. Common Voice layouts change between releases, so do not
rename, re-save, filter, or extract individual tables before handoff.

Place any future release at:

```text
data/incoming/common_voice/<release-name>/<original-archive-name>
```

`data/incoming/` is intentionally ignored by Git. If the older Common Voice
archive used to create the workbook still exists, place that untouched archive in
a separate release-named directory as well. It is not required to preserve the
74 targets, but it would strengthen exact lineage claims.

Also retain, if available, the collaborator's original instructions/messages and
the script, notebook, query, or export used to select the 2,337 legacy sentences.

## What will never be overwritten

The existing workbook remains an immutable legacy source. Its 74 collaborator
targets are copied into a versioned annotation table with:

- original workbook filename, sheet, and row;
- original sentence ID and raw source text;
- raw collaborator target, including whether the cell was a formula;
- raw `SIMILARITY` cell for forensic lineage;
- newly derived `exact_copy_derived` value;
- source and target SHA-256 hashes;
- `single_annotator_reference=true`;
- `exposed_to_rule_development=true`; and
- review/adjudication status.

No merge operation is permitted to replace a non-empty human target with Common
Voice text, a rule output, a machine translation, or a language-model output.

## Merge order

Fresh rows are matched to legacy rows using increasingly weaker evidence:

1. exact stable sentence ID;
2. exact raw source text;
3. exact Unicode-NFC and whitespace-normalized text;
4. fuzzy candidate proposed for human review only.

Fuzzy matches are never accepted automatically. Ambiguous ID/text matches are
quarantined. A merge report records matched, unmatched, ambiguous, and
source-changed counts.

For each fresh sentence, the canonical inventory records release, locale, source
TSV/split appearances, sentence ID, raw text, normalized text, hashes, clip path
and validation metadata where available. Repetition across `validated.tsv` and a
train/dev/test TSV is recorded as multiple appearances of one sentence, not as
multiple independent examples.

## Eligibility after merging

- The 74 legacy rows remain development/calibration data even when an exact row
  appears in the fresh release.
- Exact or normalized duplicates of those rows inherit the same development-only
  restriction.
- Fresh, deduplicated, unannotated rows form the candidate annotation pool.
- Final evaluation candidates are selected and their IDs/hashes frozen before
  any new prompt, rule, or model work.
- The release's original ASR train/dev/test split is provenance metadata. It does
  not automatically define the cross-standard adaptation split.

## Outputs of the completed refresh phase

The merge produced, under the release-specific private interim directory:

1. archive and file checksum manifest;
2. raw-schema and row-count inventory;
3. canonical deduplicated sentence inventory;
4. preserved legacy annotation table;
5. legacy-to-fresh match table and quarantine table;
6. duplicate-cluster report;
7. annotation candidate profile; and
8. a pilot manifest containing IDs and hashes only.

The final benchmark split remains deliberately unfrozen until pilot annotation
has established source-validity and change-rate estimates. Growth in Common
Voice increases the sampling pool; it does not justify silently changing the 74
completed targets or calling them test data.
