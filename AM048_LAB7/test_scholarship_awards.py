"""Property-based fuzz tests (Hypothesis) and edge-case tests for Lab 7."""

import math
from hypothesis import given, strategies as st
from scholarship_awards import parse_applicant, marks_average, payable_award


@given(st.text() | st.none())
def test_parse_applicant_no_crash(s):
    try:
        res = parse_applicant(s)
    except Exception as exc:  # pragma: no cover - fuzz failure path
        raise AssertionError(f"parse_applicant crashed on {s!r}: {exc}") from exc
    if res is not None:
        assert isinstance(res, tuple) and len(res) == 2
        category, marks = res
        assert isinstance(category, str) and len(category.strip()) > 0
        assert isinstance(marks, float) and math.isfinite(marks) and marks >= 0


@given(st.text() | st.none())
def test_marks_average_no_crash(s):
    try:
        res = marks_average(s)
    except Exception as exc:  # pragma: no cover - fuzz failure path
        raise AssertionError(f"marks_average crashed on {s!r}: {exc}") from exc
    if res is not None:
        assert isinstance(res, int) and not isinstance(res, bool) and res >= 0


@given(st.text() | st.none())
def test_payable_award_no_crash(s):
    try:
        res = payable_award(s)
    except Exception as exc:  # pragma: no cover - fuzz failure path
        raise AssertionError(f"payable_award crashed on {s!r}: {exc}") from exc
    if res is not None:
        assert isinstance(res, (int, float)) and not isinstance(res, bool)
        assert math.isfinite(res) and res >= 0


def test_valid_happy_paths():
    assert parse_applicant("merit:82") == ("Merit", 82.0)
    assert marks_average("72,85,90") == 82
    assert payable_award("5000|500") == 5400.0
    assert payable_award("100|500") == 0


def test_malformed_and_edge_cases():
    for bad in [None, "", "   ", "merit", "a:b:c", ":82", "merit:nan", "merit:inf", "merit:-10"]:
        assert parse_applicant(bad) is None

    for bad in [None, "", "   ", "1,,3", "one,two", "10,-5"]:
        assert marks_average(bad) is None

    for bad in [None, "", "   ", "5000", "1|2|3", "nan|0", "inf|0", "-100|50", "100|-50", "1.7e308|0"]:
        assert payable_award(bad) is None
