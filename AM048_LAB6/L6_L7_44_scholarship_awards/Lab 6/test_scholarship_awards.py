"""Complete line and branch coverage test suite for scholarship_awards.py."""

import pytest
from scholarship_awards import award_amount, is_eligible, application_status


def test_award_validation_branches():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("music", 80, "low", False)
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -1, "low", False)


def test_award_cutoff_and_renewal_branches():
    assert award_amount("merit", 75, "low", False) == 0
    assert award_amount("merit", 70, "low", False) == 0
    assert award_amount("merit", 95, "low", True) == 4000
    assert award_amount("sports", 70, "high", True) == 600
    assert award_amount("sports", 60, "low", True) == 0


def test_award_income_and_bonus_rate_branches():
    assert award_amount("merit", 90, "low", False) == 1500
    assert award_amount("arts", 75, "middle", False) == 600
    assert award_amount("sports", 80, "high", False) == 2000


def test_is_eligible_all_branches():
    assert is_eligible(40, 2, True) is True
    assert is_eligible(95, 3, True) is False
    assert is_eligible(74, 0, False) is False
    assert is_eligible(75, 1, False) is True
    assert is_eligible(85, 2, False) is False


def test_application_status_all_branches():
    assert application_status(40, True, True) == "open"
    assert application_status(25, True, True) == "closing"
    assert application_status(24, True, True) == "closed"
    assert application_status(20, False, False) == "open"
    assert application_status(30, False, True) == "open"
    assert application_status(15, True, False) == "closing"
    assert application_status(14, True, False) == "closed"
    assert application_status(5, False, False) == "closing"
    assert application_status(4, False, False) == "closed"
