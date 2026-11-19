"""Code (statement/line) coverage tests for scholarship_awards.py."""

import pytest
from scholarship_awards import award_amount, is_eligible, application_status


def test_below_cutoff_marks():
    assert award_amount("merit", 70, "low", False) == 0


def test_unknown_category_raises():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("music", 80, "low", False)


def test_negative_marks_raises():
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -5, "low", False)


def test_renewal_low_income_high_above():
    # merit cutoff 75 -> 70 on renewal; above = 25 (> 15); rate = 100 + 40 + 20 = 160
    assert award_amount("merit", 95, "low", True) == 4000


def test_non_low_income_moderate_above():
    # arts cutoff 65; above = 10 (<= 15); rate = 60
    assert award_amount("arts", 75, "middle", False) == 600


def test_is_eligible_regular():
    assert is_eligible(90, 0, False) is True


def test_is_eligible_special_quota():
    assert is_eligible(50, 2, True) is True


def test_is_eligible_low_attendance():
    assert is_eligible(70, 0, False) is False


def test_application_status_open():
    # renewal (30) + paper (10) -> cutoff = 40
    assert application_status(40, True, True) == "open"


def test_application_status_closing():
    # non-renewal (20), non-paper -> cutoff = 20; 10 >= 5
    assert application_status(10, False, False) == "closing"


def test_application_status_closed():
    assert application_status(2, False, False) == "closed"
