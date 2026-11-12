# Static Analysis Findings

The original `shuttle_system.py` was analyzed before editing with Pylint 4.1.3,
Bandit 1.9.4, and Flake8 7.5.0. The line numbers below refer to that original
file.

## Pylint findings

| Issue | Category | Line(s) | Description | Severity | Solution |
|---|---|---:|---|---|---|
| `W0102` dangerous default value | State / correctness | 11 | `logs=[]` reused the same list across calls that omitted `logs`. | Medium | Use `None` as the default and allocate a fresh list in the function. |
| `W0702` bare exception | Error handling | 29 | `except:` hid every failure while checking route averages, including data errors. | Medium | Handle empty routes in `average_load` and remove the catch-all. |
| `W0603` global statement | State management | 38 | `sync_fleet_data` replaced the module-level `routes` mapping after reading the file. | Low | Serialize and return the saved data without rebinding global state. |
| `W1514` and `R1732` file handling | Resource management | 39, 42 | Files were opened without an explicit encoding or context managers. | Medium | Use `Path.open` with UTF-8 and `with` blocks. |
| `C0103` invalid function name; `W0613` unused argument | Naming / dead code | 33 | `assignDriver` did not use snake_case, and `route_id` was ignored. | Low | Rename it `assign_driver` and validate the route ID. |
| `C0114`, `C0116` missing docstrings | Maintainability | 1, 11, 16, 19, 23, 33, 37, 45 | The module and public functions lacked explanations. | Low | Add a module docstring and concise function docstrings. |
| `C0209` percent formatting | Readability | 13 | A `%`-formatted string could be an f-string. | Low | Use an f-string for the trip log entry. |

The initial Pylint score was **6.25/10**. The original run also exposed runtime
problems that static analysis did not fully describe: negative and text
passenger counts were stored, empty routes could divide by zero, and the demo
looked up `R3` after deleting it, raising `KeyError`.

## Bandit findings

| Issue | Category | Line(s) | Description | Severity | Solution |
|---|---|---:|---|---|---|
| `B110` try/except/pass | Error handling | 29 | The bare exception silently discarded failures. | Low | Removed the catch-all and made empty-route averages return `0.0`. |
| `B311` standard pseudo-random generator | Randomness | 35 | `random.choice` was flagged as unsuitable for security-sensitive selection. | Low | Use `secrets.choice` and keep the route validation. |

Bandit reported **2 low-severity findings** before the fixes and **0 findings**
after them. No security checks were disabled or suppressed.

## Flake8 findings

| Issue | Category | Line(s) | Description | Severity | Solution |
|---|---|---:|---|---|---|
| `E722` bare `except` | Error handling / style | 29 | The bare exception could conceal unrelated failures and violated the style checks. | Medium | Remove the broad catch and handle empty trip lists explicitly. |
| `E302` and `E305` blank-line spacing | PEP 8 formatting | 11, 16, 19, 23, 33, 37, 45, 60 | Top-level definitions did not have the required spacing. | Low | Use two blank lines between top-level definitions. |
| `E501` line too long | PEP 8 formatting | 13 | A source line exceeded Flake8's 79-character limit. | Low | Break long expressions and messages across lines. |

Flake8 reported **10 style findings** in the original file. The final run
reported none.

## Additional runtime issues found by running the program

| Issue | Category | Line(s) | Description | Severity | Solution |
|---|---|---:|---|---|---|
| Invalid passenger counts | Input validation | 49-50 | The demo stored `-6` and the string `"full"` as passenger counts. | Medium | Accept only non-negative integers and use valid demo values. |
| Empty trip average | Runtime correctness | 19-21 | An empty route could cause division by zero. | Medium | Return `0.0` when no trips have been recorded. |
| Lookup after route deletion | Runtime correctness | 55, 58 | The demo deleted `R3` and then requested its average, causing `KeyError`. | Medium | Keep the demo routes available and validate route IDs before lookup. |

## Final verification

- Pylint: **10.00/10**.
- Bandit: **0 findings**.
- Flake8: **0 findings**.
- **16 direct checks passed**, covering valid counts, negative/string/decimal/
  boolean counts, unknown routes, invalid log values, empty averages, driver
  assignment, JSON write/read, and deletion handling.
- The command-line program completed with the default route and with valid `R1`
  input. An unknown route printed a clear message and exited without a traceback.
