import pytest

from equipment_borrowing.domain.errors import InvalidLoanPeriod
from equipment_borrowing.domain.loan_period import LoanPeriod

def test_T1_loan_period_accepts_1_to_7_days_and_rejects_others_BR1():
    # Boundary cases: the edges of the valid range must be accepted
    assert LoanPeriod(1).days == 1
    assert LoanPeriod(7).days == 7

    # Rejection cases: just outside each edge, and a nonsense value
    for invalid_days in (0, 8, -3):
        with pytest.raises(InvalidLoanPeriod):
            LoanPeriod(invalid_days)
            