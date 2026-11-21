# Lab 6 — TDD, BDD & Refactoring

Mohamed Samy (gso1232) · Team 12 *Lamma* · branch `lab6` · code in [`lab6/`](../../lab6)

| Deliverable | Where |
|---|---|
| Git log, one commit per TDD cycle (red → green/refactor) | [`git-log.txt`](git-log.txt) and the section below |
| Coverage report at 100% (Task A1) + one-sentence answer | [`coverage-100.png`](coverage-100.png), [`coverage.txt`](coverage.txt) |
| `registration.feature` with the drop scenario (Task B1), behave all green | [`lab6/features/registration.feature`](../../lab6/features/registration.feature), [`behave-output.txt`](behave-output.txt) |
| Smells table (Task C1) and `invoice.py` with `SiblingPolicy` (Task C2) | below, [`lab6/invoice.py`](../../lab6/invoice.py) |
| Three Gherkin scenarios for our team story (Part D) | below, [`lamma_waiting_list.feature`](lamma_waiting_list.feature) |

How to run (from `lab6/`):

```bash
python -m venv .venv
.venv\Scripts\python -m pip install pytest pytest-cov behave ruff
.venv\Scripts\python -m pytest -q                      # 10 passed
.venv\Scripts\python -m pytest --cov=registration --cov-report=term-missing
.venv\Scripts\python -m behave                         # 7 scenarios, 28 steps passed
```

## Part A — TDD kata

Each business rule was one cycle: the **red** commit holds only the new test (pytest fails or errors for the right reason), the **green** commit holds the least code that passes it, cleaned up before committing.

| Rule | Red (test only) | Green (code) |
|---|---|---|
| 1. Registering adds the course's hours | `cf0f3e9` · 1 error (no `registration` module) | `c9999ee` · 1 passed |
| 2. Total may not go over 18 hours | `ad3cd3c` · 1 error (no `RegistrationError`) | `1fe8f25` · 2 passed |
| 3. Same course cannot be registered twice | `c74c79b` · 1 failed, 2 passed | `d3490a4` · 3 passed |
| 4. A registered course can be dropped | `b7b7cc5` · 1 failed, 3 passed | `2ea43de` · 4 passed |

### Task A1 — coverage

With the four tests the report showed **95%**, missing line 26 (the error for dropping a course that is not registered). The fifth test `test_cannot_drop_a_course_that_is_not_registered` drops `SET472` while only `SET312` is registered, expects `RegistrationError("SET472 is not registered")`, and checks the student still has 3 hours. Coverage is now **100%** (`20ad10e`).

```text
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
registration.py      20      0   100%
5 passed
```

**Does 100% coverage prove the code is correct?** No — it only proves every line ran during the tests, not that the tests checked the right results or covered every rule and edge case (for example, registering a negative number of hours still runs every line and is accepted).

## Part B — BDD

The six scenarios from the handout passed first (`d3e076d`). For **Task B1** the drop scenario was added on its own (`a8b9db0`): behave reported `When the student drops "SET312"` as **undefined**. The new step reuses the existing `Given` and `Then` steps; only one `@when` was written (`a53b9de`):

```python
@when('the student drops "{code}"')
def step_drop(context, code):
    try:
        context.student.drop(code)
    except RegistrationError as e:
        context.error = str(e)
```

```text
1 feature passed, 0 failed, 0 skipped
7 scenarios passed, 0 failed, 0 skipped
28 steps passed, 0 failed, 0 skipped
```

## Part C — Refactoring `legacy_invoice.py` with SOLID

### Task C1 — smells found before touching the code

| Smell | Where | Principle it breaks |
|---|---|---|
| Long `if/elif` chain on `kind` | loop body + the `if` after the loop | **OCP**: a new student type means editing this function in two places |
| One function calculates, formats the text, writes a file **and** prints | whole `make_invoice` | **SRP**: four reasons to change in one function |
| Opens the file directly (`open("invoice_…txt")`) | end of the function | **DIP**: depends on the real disk, so a test cannot run without writing files |
| Magic numbers `1200`, `0.5`, `2000`, `5000` | inside the chain | Readability: nothing says what the numbers are, and `1200` is repeated |
| File opened without `with` | `f = open(...)` … `f.close()` | Resource safety: if `write` fails the file is never closed |
| Fee worked out per course although only total hours matter; `h` is a one-letter name | the `for` loop | Readability / needless complexity: the loop only adds up hours |

### Steps (tests run after every move)

| Commit | Step | Principle | Tests |
|---|---|---|---|
| `7e58648` | 1. Characterization tests on the **unchanged** code: regular 7200, scholarship 3600, international 17000 | safety net | 8 passed |
| `cf394e3` | 2. Name the magic numbers | readability | 8 passed |
| `700522d` | 3. One policy class per fee rule with `fee(hours)` | SRP | 8 passed |
| `2cf8010` | 4. `POLICIES` lookup replaces the `if/elif` chain | OCP | 8 passed |
| `0ca3587` | 5. Writer passed in (`FileWriter` by default); `print` removed; `FakeWriter` test added | DIP | 9 passed |

### Task C2 — `SiblingPolicy`, test first

`03bed6c` added `test_sibling_gets_25_percent_off_the_regular_fee` (6 hours × 1200 = 7200, minus 25% = **5400**) and it failed. `16da7ff` made it pass by adding **one class and one dictionary entry**; `git diff` of that commit adds 8 lines and does not touch `make_invoice`.

```python
class SiblingPolicy:
    DISCOUNT = 0.25

    def fee(self, hours):
        return RegularPolicy().fee(hours) * (1 - self.DISCOUNT)
```

### Before and after (measured)

| Measure | Before | After |
|---|---|---|
| Cyclomatic complexity of `make_invoice` (`ruff check --select C901 --config "lint.mccabe.max-complexity=1"`) | 6 | **1** |
| Tests passing (`python -m pytest -q`) | 8 (5 registration + 3 characterization) | **10** (+ fake writer, + sibling) |
| Add a "sibling discount" type | edit two `if/elif` chains | **add one class + one dict entry** |
| Test without writing files | not possible | **yes, with `FakeWriter`** |
| `ruff check .` | — | All checks passed |

## Part D — Link to our team project (Lamma)

**Story (Sprint 1 backlog, SCRUM-21 / S14, the project's key rule):**
*As a student on the waiting list, I want to be moved into a seat automatically when one frees up, so that I don't have to keep checking.*

Also saved as [`lamma_waiting_list.feature`](lamma_waiting_list.feature).

| | Scenario |
|---|---|
| **1 · happy path** | A seat frees up and the first person waiting gets it |
| **2 · refused / error** | A student who already holds a seat cannot join the waiting list again |
| **3 · edge / outline** | Seats left after a cancellation, for different waiting-list lengths |

```gherkin
Feature: Automatic promotion from the waiting list
  As a student on the waiting list
  I want to be moved into a seat automatically when one frees up
  So that I don't have to keep checking

  Background:
    Given an approved event "Arduino Workshop" with 2 seats

  Scenario: A seat frees up and the first person waiting gets it
    Given "Sara" and "Omar" hold the 2 seats
    And "Mona" is first and "Youssef" is second on the waiting list
    When "Sara" cancels her seat
    Then "Mona" holds a seat
    And "Youssef" is first on the waiting list
    And the event has 0 seats left

  Scenario: A student cannot take a second place in the same event
    Given "Sara" and "Omar" hold the 2 seats
    When "Sara" tries to join the waiting list
    Then the request is refused with "already has a place in this event"
    And the waiting list is empty

  Scenario Outline: Seats left after a cancellation
    Given "Sara" and "Omar" hold the 2 seats
    And <waiting> students are on the waiting list
    When "Sara" cancels her seat
    Then the event has <seats_left> seats left
    And <still_waiting> students are still waiting

    Examples:
      | waiting | seats_left | still_waiting |
      | 0       | 1          | 0             |
      | 1       | 0          | 0             |
      | 3       | 0          | 2             |
```
