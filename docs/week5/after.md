# Week 5 — Before / after and pairing reflection

Pair: Mohamed Samy (gso1232) · Hamza Khaled (hamza0114) · branch `week5-quality`

## D3. Before / after

Commands run after the last step: `pytest -v`, `ruff check .`, `ruff format`, `pylint fees.py`.

| Measure | Before (`legacy_fees.py`) | After (`fees.py`) |
|---|---|---|
| Ruff issues (total) | 17 (the handout's 16 + `PLR0917`, which our newer Ruff adds) | **0** — "All checks passed!" |
| Highest cyclomatic complexity | 9 (`calc`) | **3** (`tuition_fee`) |
| Arguments of the main function | 6, all positional (`d, t, y, s, disc, extra`) | **5**, three with defaults (`courses, kind, summer=False, discount=0, extras=()`) |
| Pylint score (/10) | 4.86 | **10.00** |
| Tests passing | 0 (no tests) | **6 / 6** in `test_fees.py` (16 / 16 with `test_grades.py`) |

`ruff check .` still lists 17 problems, all in `legacy_fees.py`. That file is kept **unchanged on purpose**: the characterization tests import its `calc` to prove the new `tuition_fee` gives the same results. For the same reason `ruff format` was run on the four files we wrote and not on the legacy file.

## What each step changed

| Commit | Step | Ruff problems left in `fees.py` |
|---|---|---|
| Add characterization tests and copy legacy code to fees.py | tests first | 17 |
| Refactor step 1 | dead code removed (F401, F841, ARG001) | 11 |
| Refactor step 2 | renamed (N802 and mysterious names) | 10 |
| Refactor step 3 | constants and `StudentType` enum (PLR2004) | 6 |
| Refactor step 4 | `FEE_SHARE` rate table, `if summer:` (C901, E711, E712) | 3 |
| Refactor step 5 | `extras=()` and a `Course` data class (B006) | 2 |
| Refactor step 6 | calculation separated from printing | 2 |
| Refactor step 7 | hidden bug fixed; the last test turns green | 0 |

The tests could not import `fees.py` until step 5 created `Course`; from step 5 on, 5 of 6 tests passed, and `test_scholarship_student_is_not_skipped` failed until step 7 fixed the bug, as the handout expects.

## Pairing reflection

‹3–4 sentences written together: how switching driver and navigator every 12 minutes went, one thing the navigator caught that the driver missed, and whether pairing felt slower or faster than working alone.›

- **Mohamed Samy:** ‹one line in your own words›
- **Hamza Khaled:** ‹one line in your own words›
