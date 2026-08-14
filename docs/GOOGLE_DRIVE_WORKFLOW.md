# Google Drive workflow

**Verified:** 2026-08-14

The stable project folder is
[SesoFix](https://drive.google.com/drive/folders/1jC_13ekMXzxu1cKEbRlqXoA7jdV_-6VI).
Its IDs, online artifact links, and mounted local path are recorded in
`configs/google_drive.json`.

## Active layout

```text
SesoFix/
└── 00 Current Research/
    ├── 00 Project Control/
    ├── 01 Annotation/
    │   └── Pilot v1/
    │       ├── 01 Primary Annotation/
    │       ├── 02 Independent Review/
    │       ├── 03 Returned Completed/
    │       └── 04 Adjudication/
    ├── 02 Experiments/
    └── 03 Paper/
```

Existing files and historical folders at the project root were left untouched.
`00 Current Research` is the active controlled area; it does not replace or
silently reorganize the older material.

## Non-destructive rules

1. Never delete, rename, or overwrite an existing raw dataset or completed human
   annotation.
2. Update the four project-control files by their recorded Drive file IDs so
   links and version history remain stable.
3. Treat returned annotations as append-only. Preserve the submitted file or
   Sheet revision before any import, cleanup, or adjudication.
4. Create every experiment under `02 Experiments/<experiment_id>/` with separate
   `inputs`, `config`, `outputs`, and `analysis` subfolders when those artifacts
   exist.
5. Store model checkpoints only when a Colab experiment has an approved retention
   purpose. Local training remains prohibited.
6. Git remains canonical for code, manifests, and Markdown protocols. Drive is
   canonical for shareable human workbooks and large/private run artifacts.
7. The mounted folder is a synchronized mirror, not a second Git checkout. Do
   not run cleanup scripts against it.

## Mounted local path

```text
/Users/komondi/Library/CloudStorage/
GoogleDrive-kevochi09@gmail.com/My Drive/SesoFix
```

The path contains spaces and account-specific components. Code must read it from
`configs/google_drive.json`; it must never hard-code a shortened or guessed path.

## Annotation links

- [Primary annotation](https://docs.google.com/spreadsheets/d/1fmK-hxu5vMmd9aYb77MscDcRD1C_kWtn_Z3v1xZcFBQ/edit)
- [Independent review](https://docs.google.com/spreadsheets/d/1j-nfWo7zec04SjFR_s8616n8e3ERkrcIo14jH5vQW7I/edit)

Share only the role-specific file link. Do not share the project-root link with
annotators during the blind pass.

## Permission risk

The project root currently grants **anyone with the link editor access**. The
folder layout reduces accidental mixing but cannot enforce blinding. Before the
independent reviewer begins, either restrict the root permission and share the
two role files separately, or explicitly record that review blinding is
procedural rather than access-controlled. Do not claim permission-enforced
blinding while the root setting remains unchanged.
