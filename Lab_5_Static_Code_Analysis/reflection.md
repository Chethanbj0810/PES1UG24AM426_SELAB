# Lab 5 Reflection

The supplied three-page handout requests a reflection but does not list four
separate reflection questions. These four prompts address the requested
reflection points.

## 1. What did I learn from using Pylint, Bandit, and Flake8?

Each tool checks a different part of the code. Pylint found maintainability and
correctness risks such as a mutable default, weak exception handling, and
resource-management problems. Bandit highlighted security-sensitive coding
patterns. Flake8 identified PEP 8 and whitespace issues. Using all three gave a
broader review than relying on one report.

## 2. Which issues mattered most, and why?

The invalid passenger values and the lookup of a deleted route caused incorrect
runtime behavior. The empty-route average could divide by zero, while the broad
exception hid failures instead of explaining them. The mutable default could
share log state between calls. These correctness problems mattered more to the
shuttle tracker than the low-severity style findings.

## 3. How did the fixes improve the program?

Trip logging now rejects negative counts, booleans, non-integers, unknown route
IDs, and malformed log lists. Empty routes return an average of `0.0`, and the
demo no longer removes a route before looking it up. Fleet JSON uses UTF-8 and
context-managed file access. Driver selection uses `secrets.choice`, and the
function names, docstrings, and formatting are consistent with Python style.

## 4. What did comparison and testing teach me about static analysis?

The original run exposed a `KeyError` that the tools could not demonstrate on
their own, and direct input checks were needed to verify passenger validation.
Static analysis can point to risky patterns and confirm those patterns are no
longer present, but it does not prove that the whole application behaves
correctly. Running the program with valid and invalid cases alongside the three
reports gives stronger evidence.
