"""Tests focused on executing the library-fines application code."""

import pytest

from library_fines import can_borrow, late_fine, renewal_status


@pytest.mark.parametrize(
    ("member", "days_kept"),
    [("student", 14), ("faculty", 30), ("guest", 14)],
)
def test_on_time_returns_have_no_fine(member, days_kept):
    assert late_fine(member, days_kept, False) == 0


def test_student_late_return_uses_student_daily_rate():
    assert late_fine("student", 20, False) == 12


def test_faculty_late_return_uses_faculty_loan_period_and_rate():
    assert late_fine("faculty", 35, False) == 5


def test_guest_late_return_uses_guest_daily_rate():
    assert late_fine("guest", 16, False) == 10


def test_damaged_book_adds_damage_charge_even_when_returned_on_time():
    assert late_fine("student", 10, True) == 150


def test_overdue_fine_is_capped_before_damage_charge():
    assert late_fine("guest", 100, True) == 350


def test_unknown_member_type_raises_value_error():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("visitor", 10, False)


def test_negative_days_kept_raises_value_error():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)


def test_student_can_borrow_below_limit():
    assert can_borrow(2, 0, "student") is True


def test_student_at_borrowing_limit_cannot_borrow():
    assert can_borrow(3, 0, "student") is False


def test_faculty_can_borrow_below_limit():
    assert can_borrow(9, 0, "faculty") is True


def test_faculty_at_borrowing_limit_cannot_borrow():
    assert can_borrow(10, 0, "faculty") is False


def test_pending_fine_above_100_blocks_borrowing():
    assert can_borrow(0, 101, "faculty") is False


def test_pending_fine_of_100_and_zero_books_is_allowed():
    assert can_borrow(0, 100, "student") is True


def test_renewal_succeeds_when_eligible():
    assert renewal_status(0, False, 5) == "renewed"


def test_reservation_denies_renewal():
    assert renewal_status(0, True, 5) == "denied"


def test_renewal_limit_is_enforced():
    assert renewal_status(2, False, 5) == "limit reached"


def test_overdue_book_cannot_be_renewed():
    assert renewal_status(1, False, -1) == "overdue"


def test_nonnegative_days_remaining_allow_normal_renewal():
    assert renewal_status(1, False, 0) == "renewed"
