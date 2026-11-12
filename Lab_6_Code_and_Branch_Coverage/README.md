#  SE Lab 6: Code and Branch Coverage

This project tests the supplied `library_fines.py` functions for calculating late fines, checking borrowing eligibility, and deciding renewal status. The application logic is unchanged from the assigned source project.

## Why measure coverage?

Code (line) coverage reports which executable lines tests reach. Branch coverage also checks both outcomes of decisions such as `if` and `elif`, helping reveal untested paths even when a line has executed.

## Setup

From this directory, create and activate a virtual environment, then install the dependencies:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Initial starter-test results

The supplied `test_library_fines.py` passed 2 tests. The initial report for `library_fines.py` showed 50% line coverage. With branch measurement enabled, the coverage report showed 43% combined coverage, with 16 statements missed and 7 partially covered branches out of 22.

## Code coverage

Run the code coverage suite and report only the application module:

```powershell
coverage run -m pytest CodeCoverageTest_24AM426_application.py
coverage report -m library_fines.py
```

Result: **100% line coverage** for `library_fines.py` (32 statements, none missed). The suite passes 21 test cases, including validation errors and the fine cap.

## Branch coverage

Run the dedicated branch suite independently:

```powershell
coverage run --branch -m pytest BranchCoverageTest_24AM426_application.py
coverage report -m library_fines.py
```

Result: **100% combined coverage** for `library_fines.py`, with all 22 branch opportunities covered and no partial branches. The branch suite passes 15 test cases.

## Screenshots

The lab handout requests terminal screenshots for each final coverage run. Genuine PNG screenshots were not captured in this environment; capture the two command outputs above in a terminal and add them as `Code_Coverage_Result.png` and `Branch_Coverage_Result.png` before submission.
