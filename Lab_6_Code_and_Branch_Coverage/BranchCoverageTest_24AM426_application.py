"""Targeted tests for both outcomes of each application decision."""

import pytest

from library_fines import can_borrow, late_fine, renewal_status


@pytest.mark.parametrize("member", ["student", "faculty", "guest"])
def test_valid_member_type_takes_the_fine_calculation_path(member):
    assert late_fine(member, 0, False) == 0


def test_invalid_member_type_takes_the_validation_error_path():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("alumni", 40, False)


def test_negative_days_take_the_validation_error_path():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("guest", -2, False)


def test_faculty_and_nonfaculty_use_different_loan_periods():
    assert late_fine("faculty", 31, False) == 1
    assert late_fine("student", 15, False) == 2


def test_nonoverdue_return_skips_fine_and_positive_overdue_return_calculates_it():
    assert late_fine("guest", 14, False) == 0
    assert late_fine("guest", 15, False) == 5


def test_fine_cap_has_both_below_cap_and_above_cap_outcomes():
    assert late_fine("guest", 50, False) == 180
    assert late_fine("guest", 60, False) == 200


def test_damage_charge_condition_has_true_and_false_outcomes():
    assert late_fine("faculty", 30, False) == 0
    assert late_fine("faculty", 30, True) == 150


def test_pending_fine_boundary_allows_100_and_rejects_more():
    assert can_borrow(1, 100, "faculty") is True
    assert can_borrow(1, 101, "faculty") is False


def test_faculty_limit_has_true_and_false_outcomes():
    assert can_borrow(8, 0, "faculty") is True
    assert can_borrow(11, 0, "faculty") is False


def test_nonfaculty_limit_has_true_and_false_outcomes():
    assert can_borrow(1, 0, "guest") is True
    assert can_borrow(4, 0, "guest") is False


def test_reservation_present_or_absent_selects_denial_or_eligibility_checks():
    assert renewal_status(1, True, 2) == "denied"
    assert renewal_status(0, False, 2) == "renewed"


def test_renewal_count_boundary_selects_limit_or_days_check():
    assert renewal_status(2, False, 2) == "limit reached"
    assert renewal_status(1, False, 2) == "renewed"


def test_days_left_sign_selects_overdue_or_renewed():
    assert renewal_status(1, False, -2) == "overdue"
    assert renewal_status(1, False, 1) == "renewed"
