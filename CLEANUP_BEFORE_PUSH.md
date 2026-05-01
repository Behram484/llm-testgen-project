# Cleanup checklist before pushing to GitHub / submitting

The cleanup script could not delete files inside this folder from the assistant
sandbox (mount is read-only for delete operations). Run these commands on
Windows before you push or zip the repo.

## 1. Delete virtualenvs and Python caches

PowerShell, from the repo root:

```powershell
# .venv directories (~25 MB each)
Remove-Item -Recurse -Force .\testgen-runner\.venv
Remove-Item -Recurse -Force .\original\testgen-runner\.venv

# All __pycache__ directories
Get-ChildItem -Recurse -Filter "__pycache__" -Directory `
  | Where-Object { $_.FullName -notmatch "\\.git\\" } `
  | Remove-Item -Recurse -Force

# pytest cache
Get-ChildItem -Recurse -Filter ".pytest_cache" -Directory `
  | Where-Object { $_.FullName -notmatch "\\.git\\" } `
  | Remove-Item -Recurse -Force
```

These are already in `.gitignore`, so git will not commit them, but they bloat
any local zip you make for school submission.

## 2. Clear historical output

The `output/` directory under `testgen-runner/` still contains test artefacts
from local runs (LAPTOP-TALOA354 logs, batch_results.txt from earlier
configurations). Clear it but keep the README:

```powershell
Get-ChildItem -LiteralPath .\testgen-runner\output -Force `
  | Where-Object { $_.Name -ne 'README.md' } `
  | Remove-Item -Recurse -Force
```

If `testgen-runner\output` doesn't currently have a README, create a one-liner
explaining the directory is regenerated on every run.

## 3. Delete one-off backup file

```powershell
Remove-Item .\testgen-runner\backup_before_dependency_change.txt
```

## 4. (Optional) Decide on `original/`

`original/` is a 35 MB pre-ANSI-fix snapshot of the same code. README points
to it as a reproducibility reference for Section 4.1 numbers, but it doubles
the repo size. Two options:

- **Keep** if examiners may want to inspect the pre-fix code path.
- **Delete** with `Remove-Item -Recurse -Force .\original` if size matters.

Either way, also clean `original/testgen-runner/.venv` and its
`__pycache__` (step 1 already covers them).

## 5. (Optional) Trim `archive/Dataset_V1`

`testgen-runner/archive/Dataset_V1/` is ~5 MB of historical dataset files. If
you are keeping the archive folder, leave it; if you want a leaner submission
zip, remove it.

## 6. Verify before zipping

After cleanup the top-level repo should be roughly:

```
llm-testgen-project/
├── .git/                     (kept; carries history)
├── .gitignore
├── README.md                 (refreshed)
├── CLEANUP_BEFORE_PUSH.md    (this file — feel free to delete after running)
├── LAB_PC_SETUP_AND_RUN_GUIDE.md
├── testgen-runner/
│   ├── requirements.txt      (newly added)
│   ├── runner.py
│   ├── batch_runner.py
│   ├── ... (other .py and .ps1)
│   ├── prompts/
│   ├── config/config.json    (now portable)
│   ├── tests/
│   └── output/README.md only
├── testgen-lab/
└── original/                 (kept or deleted per step 4)
```

Expected total size after step 1+2+3: well under 10 MB excluding `.git/`.

## 7. School submission ZIP

When you produce the school submission package (per supervisor instructions),
copy only `testgen-runner/` and `testgen-lab/` into a fresh folder, then zip
that folder. Do not copy `.git/`, `original/`, or any of the artefacts cleaned
in steps 1–3.
