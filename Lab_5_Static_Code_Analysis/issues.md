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
