"""Hardened scholarship awards parser, average, and payout calculator."""

import math


def _parse_finite_nonneg_float(raw):
    """Parse a finite non-negative float from string, or return None."""
    if not isinstance(raw, str):
        return None
    stripped = raw.strip()
    if not stripped:
        return None
    try:
        value = float(stripped)
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(value) or value < 0.0:
        return None
    return value


def parse_applicant(text):
    """Parse 'category:marks' into (TitleCategory, float_marks) or None."""
    if not isinstance(text, str):
        return None
    parts = text.split(":")
    if len(parts) != 2:
        return None
    category = parts[0].strip()
    if not category:
        return None
    normalized = category.title()
    if not normalized.strip():
        return None
    marks = _parse_finite_nonneg_float(parts[1])
    if marks is None:
        return None
    return normalized, marks


def marks_average(marks_csv):
    """Compute integer floor average of comma-separated non-negative ints."""
    if not isinstance(marks_csv, str) or not marks_csv.strip():
        return None
    tokens = [part.strip() for part in marks_csv.split(",")]
    if not tokens or any(not tok for tok in tokens):
        return None
    values = []
    for tok in tokens:
        try:
            num = int(tok)
        except ValueError:
            return None
        if num < 0:
            return None
        values.append(num)
    return sum(values) // len(values)


def payable_award(text):
    """Parse 'award|deduction' and compute GST-adjusted payable award or None."""
    if not isinstance(text, str):
        return None
    parts = text.split("|")
    if len(parts) != 2:
        return None
    award = _parse_finite_nonneg_float(parts[0])
    deduction = _parse_finite_nonneg_float(parts[1])
    if award is None or deduction is None:
        return None
    total = award * 1.18 - deduction
    if not math.isfinite(total):
        return None
    return round(max(total, 0.0), 2)


def main():
    """Interactive demo runner for scholarship_awards utilities."""
    print("==== Running parse_applicant ====")
    user_input = input("Enter category:marks (e.g. merit:82): ")
    result = parse_applicant(user_input)
    print("Category and Marks:", result if result is not None else "Invalid input")

    print("\n==== Running marks_average ====")
    user_input = input("Enter marks as CSV (e.g. 72,85,90): ")
    result = marks_average(user_input)
    print("Average Marks:", result if result is not None else "Invalid input")

    print("\n==== Running payable_award ====")
    user_input = input("Enter award|deduction (e.g. 5000|500): ")
    result = payable_award(user_input)
    print("Payable Award:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
