# Lab 5 Reflection — Static Code Analysis

## 1. Roles of Bandit, Pylint, and Flake8 (and Why All Three Matter)
Each static analysis tool targets a distinct quality dimension:
- **Bandit** scans the Python Abstract Syntax Tree (AST) specifically for security vulnerabilities (CWE patterns) such as shell command injection (`B605`), dynamic code execution (`B307`), weak hashes (`B324`), predictable PRNGs (`B311`), and swallowed exceptions (`B110`).
- **Pylint** evaluates deeper code quality, semantic bugs, design smells, and maintainability (mutable default arguments `W0102`, leaked file handles `R1732`, unspecified file encoding `W1514`, unused variables `W0612`, naming conventions `C0103`, missing docstrings `C0116`), producing an overall score out of 10.
- **Flake8** enforces strict PEP 8 formatting consistency and fast syntax/lint checks (`E501` <= 79-character lines, `F401` unused imports, `E711` `is None`, `W292` trailing newline).

Using only one tool leaves blind spots: Flake8 passes code that calls `eval()` or `hashlib.md5()`, while Bandit passes code with mutable default lists or missing docstrings.

## 2. Addressing High-Severity Security & Reliability Risks First
Fixing Bandit's High and Medium findings first eliminated the most severe attack vectors before refactoring code structure:
- Removing `os.system(...)` (`B605`) prevented arbitrary OS shell execution from untrusted filenames.
- Replacing `eval(deduction_expr)` (`B307`) with `ast.parse(..., mode="eval")` and an explicit AST allowlist (`_eval_ast_node`) preserved arithmetic payroll formulas like `"base * 0.85"` while blocking code injection such as `__import__("os")`.
- Upgrading MD5 (`B324`) to SHA-256 and `random.randint` (`B311`) to `secrets.randbelow` eliminated weak cryptographic primitives.
- Replacing bare `except: pass` (`B110`/`W0702`) exposed real error states instead of silently ignoring failures.

## 3. Issues Static Analysis Missed (Detected Through Manual & Runtime Inspection)
Static tools operate largely syntactically and cannot infer domain invariants or deployment intent:
- **Hardcoded secret & stdout exposure**: `payroll_key = "HR_PAYROLL_MASTER_SECRET_2026"` used a non-standard variable name that Bandit's hardcoded-password check missed, and `print("Payroll key loaded:", payroll_key)` leaked credentials to logs. Moving to `os.environ.get("PAYROLL_KEY")` and logging only `"configured"` / `"not set"` eliminated secret leakage.
- **Domain logic bugs on amounts**: No static analyzer flagged that `deduct_penalty("EMP102", -500)` would *increase* an employee's salary or exceed `base_salary`. Adding `_is_valid_amount()` (rejecting negatives, `NaN`, `inf`, and `bool`) enforced domain integrity.
- **Import-time execution**: Calling `main()` unconditionally at module bottom caused payroll mutations and file writes during simple `import` statements; adding `if __name__ == "__main__":` fixed module testability.

## 4. Limitations of Static Analysis and Practical Workflow Integration
Static analysis flags syntactic patterns without executing business workflows or guaranteeing functional correctness—over-zealous fixes can break runtime behavior unless backed by tests, and rules like `unused variable` do not reveal whether a variable (`statutory_buffer`) indicates an unimplemented requirement. Conversely, enforcing PEP 8 line limits and docstrings improves reviewability across team commits. In real engineering workflows, running **Bandit**, **Pylint** (with a minimum score gate such as >= 9.5), **Flake8**, and unit tests automatically inside pre-commit hooks and CI pull-request checks catches security regressions and quality drift before code reaches production.
