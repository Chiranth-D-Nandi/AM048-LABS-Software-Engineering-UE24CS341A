"""Branch and boundary coverage tests for scholarship_awards.py."""

import pytest
from scholarship_awards import award_amount, is_eligible, application_status


def test_award_validation_branches():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("music", 80, "low", False)
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -1, "low", False)


def test_award_cutoff_and_renewal_branches():
    # above <= 0 branch (equal to cutoff and below cutoff)
    assert award_amount("merit", 75, "low", False) == 0
    assert award_amount("merit", 70, "low", False) == 0
    # is_renewal=True AND category != "sports" -> True branch (cutoff 75 -> 70)
    assert award_amount("merit", 95, "low", True) == 4000
    # is_renewal=True AND category == "sports" -> False branch (cutoff stays 60)
    assert award_amount("sports", 70, "high", True) == 600
    assert award_amount("sports", 60, "low", True) == 0


def test_award_income_and_bonus_rate_branches():
    # above <= 15 (False branch of `above > 15`) with low and non-low income
    assert award_amount("merit", 90, "low", False) == 1500
    assert award_amount("arts", 75, "middle", False) == 600
    # above > 15 (True branch) with income_level != "low" (False branch of line 21)
    assert award_amount("sports", 80, "high", False) == 2000


def test_is_eligible_all_branches():
    # Special quota True/False outcomes
    assert is_eligible(40, 2, True) is True
    assert is_eligible(95, 3, True) is False
    # Regular quota: attendance < 75 True vs False
    assert is_eligible(74, 0, False) is False
    assert is_eligible(75, 1, False) is True
    assert is_eligible(85, 2, False) is False


def test_application_status_all_branches():
    # is_renewal True/False x is_paper True/False and open/closing/closed boundaries
    assert application_status(40, True, True) == "open"
    assert application_status(25, True, True) == "closing"
    assert application_status(24, True, True) == "closed"
    assert application_status(20, False, False) == "open"
    assert application_status(30, False, True) == "open"
    assert application_status(15, True, False) == "closing"
    assert application_status(14, True, False) == "closed"
    assert application_status(5, False, False) == "closing"
    assert application_status(4, False, False) == "closed"
