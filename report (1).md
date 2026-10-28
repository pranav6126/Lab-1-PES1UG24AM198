# Lab 5: Static Code Analysis

**Student Name:** Pranav
**SRN:** PES1UG24AM198
**Experiment:** Static Code Analysis using Pylint, Bandit and Flake8
**Repository:** SETAPESU26/L5_16_pet_shelter (https://github.com/SETAPESU26/L5_16_pet_shelter)

**Assigned file:** `pet_shelter.py`
**Tools:** Pylint 4.1.3, Bandit 1.9.4, Flake8 7.4.1 (Python venv)

## 1. Program
SQLite-backed animal shelter register: registers pets, processes adoptions, finds the oldest available pet, issues adoption codes, clears unadopted records. Original program ran and printed `Kiwi PET-#### active`; the fixed program prints the same format.

## 2. Results before and after

| Tool | Before | After |
|------|--------|-------|
| Pylint score | 3.95/10 (24 messages) | **10.00/10** |
| Bandit | 3 (1 Medium, 2 Low) | **0** |
| Flake8 | 5 (E501 x3, E722, E701) | **0** |

Reports: `pylint_report_before.txt` / `pylint_report_after.txt`, `bandit_report_before.txt` / `bandit_report_after.txt`, `flake8_report_before.txt` / `flake8_report_after.txt` (plus `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt` generated with the handout's commands on the final file).

## 3. Commits (one per tool)
1. `Fix Pylint code quality issues`: docstrings, snake_case names, mutable default, `global` removed, bare `except` fixed. Score 3.95 to 8.64.
2. `Fix Bandit security findings`: parameterized SQL (B608), `secrets` (B311), no more except/pass (B110). Score to 9.09, Bandit clean.
3. `Fix Flake8 style violations`: wrapped long lines (E501), split one-line `if` (E701). Flake8 clean, Pylint 10.00.

## 4. Issue table
See `issues.md` (11 rows, 10 distinct fixes; the handout requires at least 4).

## 5. Verification
- `python -m py_compile` passes; program runs.
- Old vs new behavior compared on: empty table returns `None`, oldest-available ordering, adoption counter and status, clearing unadopted rows, adoption codes always within 1000-9999.
- New behavior (intended): `tags` list no longer shared between calls; names containing quotes no longer break or inject SQL.
- Limitations: no pre-existing test suite; the module still runs `main()` on import, as in the original.

## 6. Reflection
See `reflection.md`.
