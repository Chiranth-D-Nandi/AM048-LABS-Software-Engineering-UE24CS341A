"""Employee payroll computation and salary disbursement module."""

import ast
import hashlib
import json
import operator
import os
import secrets

payroll_records = {
    "EMP101": {"name": "David", "base_salary": 4500.0, "tax_rate": 0.15},
    "EMP102": {"name": "Elena", "base_salary": 5200.0, "tax_rate": 0.20},
    "EMP103": {"name": "Frank", "base_salary": 3800.0, "tax_rate": 0.12},
}

_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _is_number(value):
    """Return True for int or float values, excluding booleans."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_valid_amount(value):
    """Return True if value is finite and non-negative (not bool)."""
    return _is_number(value) and 0 <= value < float("inf")


def _eval_ast_node(node, variables):
    """Evaluate restricted AST arithmetic nodes with allowed vars."""
    if isinstance(node, ast.Expression):
        return _eval_ast_node(node.body, variables)
    if isinstance(node, ast.Constant):
        if _is_number(node.value):
            return float(node.value)
        raise ValueError(f"Unsupported constant: {node.value!r}")
    if isinstance(node, ast.Name) and node.id in variables:
        return float(variables[node.id])
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPS:
        left = _eval_ast_node(node.left, variables)
        right = _eval_ast_node(node.right, variables)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ValueError("Division by zero in deduction expression")
        return _BINARY_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        operand = _eval_ast_node(node.operand, variables)
        return _UNARY_OPS[type(node.op)](operand)
    raise ValueError(f"Unsupported expression node: {ast.dump(node)}")


def process_salary(emp_id, bonus, transaction_logs=None):
    """Credit a non-negative bonus and record an audit log entry."""
    if transaction_logs is None:
        transaction_logs = []
    if emp_id not in payroll_records or not _is_valid_amount(bonus):
        return False
    payroll_records[emp_id]["base_salary"] += bonus
    transaction_logs.append(
        f"Credited bonus {bonus:g} to employee id {emp_id}"
    )
    return True


def deduct_penalty(emp_id, penalty):
    """Deduct a valid penalty from base salary when funds suffice."""
    if emp_id not in payroll_records or not _is_valid_amount(penalty):
        return False
    if penalty > payroll_records[emp_id]["base_salary"]:
        return False
    payroll_records[emp_id]["base_salary"] -= penalty
    return True


def check_bonus_eligibility(emp_id, min_base=4000.0):
    """Return True if employee exists and meets min_base salary."""
    record = payroll_records.get(emp_id)
    if record is None:
        return False
    return record["base_salary"] >= min_base


def compute_net_salary(emp_id, deduction_expr):
    """Compute net salary using a safely parsed arithmetic expression."""
    if emp_id not in payroll_records:
        raise KeyError(f"Unknown employee id: {emp_id}")
    record = payroll_records[emp_id]
    if _is_number(deduction_expr):
        return float(deduction_expr)
    if not isinstance(deduction_expr, str):
        raise ValueError(
            "deduction_expr must be a string arithmetic expression"
        )
    tree = ast.parse(deduction_expr, mode="eval")
    variables = {"base": record["base_salary"], "tax_rate": record["tax_rate"]}
    return _eval_ast_node(tree, variables)


def generate_employee_hash(emp_id):
    """Return a SHA-256 hex digest identifier for the given employee ID."""
    return hashlib.sha256(emp_id.encode("utf-8")).hexdigest()


def generate_payroll_token():
    """Generate a cryptographically random 4-digit payroll token."""
    return 1000 + secrets.randbelow(9000)


def export_payroll_sheet(filename="payroll_sheet.txt"):
    """Export current payroll records cleanly as UTF-8 JSON to filename."""
    with open(filename, "w", encoding="utf-8") as payroll_file:
        payroll_file.write(json.dumps(payroll_records, indent=2) + "\n")
    print(f"Payroll summary exported to: {filename}")


def main():
    """Run sample payroll operations and print summary metrics."""
    payroll_key = os.environ.get("PAYROLL_KEY")
    process_salary("EMP101", 350)
    deduct_penalty("EMP102", 100)
    print("Is EMP101 eligible:", check_bonus_eligibility("EMP101"))
    print("Net salary:", compute_net_salary("EMP101", "base * 0.85"))
    print("Employee Hash:", generate_employee_hash("EMP101"))
    print("Payroll Token:", generate_payroll_token())
    export_payroll_sheet()
    key_status = "configured" if payroll_key else "not set"
    print("Payroll key status:", key_status)


if __name__ == "__main__":
    main()
