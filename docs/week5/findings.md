# Week 5 — Static analysis findings (`legacy_fees.py`)

Pair: Mohamed Samy (gso1232) · Hamza Khaled (hamza0114)
Tools: Ruff 0.17.6 with the lab's `pyproject.toml`, Pylint 4.1.4. Full output in `before.txt`.

## Summary

| Tool | Result |
|---|---|
| Ruff | **17 problems**. The handout lists 16; our newer Ruff also reports `PLR0917 too-many-positional-arguments` for the same 6-argument `calc`. |
| Pylint | **4.86 / 10**, 15 messages, including `E0606 possibly-used-before-assignment` for `fee` in `ProcessAll`, which points straight at the hidden bug below. |

## C1. Findings table

| Rule | Count | Smell (lecture name) | Refactoring |
|---|---|---|---|
| F401 | 2 | Dead code (unused imports `os`, `math`) | Delete the imports |
| PLR2004 | 6 | Magic numbers (`1`, `2`, `350`, `6000`…) | Replace with named constants / an enum |
| C901 | 1 | Long method / complex conditional: `calc` has complexity 9 (limit 5) | Replace the `if/elif` chain with a rate table; split the function |
| PLR0913 (+ PLR0917) | 1 (+1) | Long parameter list: `calc` takes 6 positional arguments | Remove the unused one, give the rest keyword defaults, group course data in a `Course` object |
| ARG001 | 1 | Dead code (unused parameter `y`, the year) | Remove the parameter |
| B006 | 1 | Mutable default argument `extra=[]`, shared between every call | Use an immutable default `extras=()` |
| E711 / E712 | 1 / 1 | Clumsy comparisons `disc != None`, `s == True` | `if discount:` / `if summer:`, with a default of 0 for the discount |
| F841 | 1 | Dead code (variable `tmp` is computed and never used) | Delete it |
| N802 | 1 | Bad naming: `ProcessAll` is not snake_case | Rename to `process_all` |

## C2. Smells the tools did not report

1. **Mysterious names.** `d`, `t`, `y`, `s`, `disc`, `c`, `x`, `st` say nothing; you need the comment on line 5 to know that `t` is a student type. Ruff only checks the *style* of a name, not its meaning.
2. **Type codes instead of a type.** Student types are bare numbers `1/2/3` with a comment as the only explanation (primitive obsession). Nothing stops a caller passing `4`.
3. **Duplicated code.** `ProcessAll` has two almost identical `calc(...)` calls that differ only in the type number, and `report` repeats the type checks that `calc` already did.
4. **Mixed responsibilities.** `report` and `ProcessAll` both calculate *and* print, so their results cannot be tested without capturing the screen output.
5. **Primitive obsession for courses.** A course is a dictionary `{"h": 3}`; a typo such as `{"hours": 3}` only fails at run time with a `KeyError`.

## The hidden bug in `ProcessAll`

We ran the snippet from the handout:

```text
>>> ProcessAll([{... "Sara", "type": 1 ...}, {... "Omar", "type": 3 ...}])
Sara 1050
Omar 1050
>>> ProcessAll([{... "Omar", "type": 3 ...}])
UnboundLocalError: cannot access local variable 'fee' where it is not associated with a value
```

`ProcessAll` only has `if` branches for types 1 and 2, so for a scholarship student (type 3) neither branch runs and `fee` is never set for him. Omar therefore prints **the previous student's fee** (Sara's 1050) instead of 0, which is silently wrong, and if Omar is the *first* student in the list there is no earlier value at all and the program crashes with `UnboundLocalError`. Pylint's `E0606 possibly-used-before-assignment` warned about exactly this line; the fix is to calculate the fee for **every** student type.
