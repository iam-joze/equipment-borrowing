import pytest

from equipment_borrowing.domain.errors import InvalidLoanTransition
from equipment_borrowing.domain.loan import Loan, LoanStatus
from equipment_borrowing.domain.loan_period import LoanPeriod

def make_loan() -> Loan:
    return Loan(
        loan_id="L1",
        equipment_id="E1",
        period=LoanPeriod(3)
    )

def test_T2_loan_follows_allowed_state_transitions_and_rejects_others_BR2():
    loan = make_loan()
    assert loan.status == LoanStatus.REQUESTED

    # Rejection: a loan that was never approved cannot be returned
    with pytest.raises(InvalidLoanTransition):
        loan.mark_returned()
    assert loan.status == LoanStatus.REQUESTED # a rejected action changes nothing

    # Valid path: requested -> approved -> returned
    loan.approve()
    assert loan.status == LoanStatus.APPROVED

    # Rejection: approving twice is not allowed
    with pytest.raises(InvalidLoanTransition):
        loan.approve()

    loan.mark_returned()
    assert loan.status == LoanStatus.RETURNED

    # Valid path: Requested -> approved -> cancelled
    cancelled = make_loan()

    # Rejection: only an approved loan can be cancelled
    with pytest.raises(InvalidLoanTransition):
        cancelled.cancel()
    cancelled.approve()
    cancelled.cancel()
    assert cancelled.status == LoanStatus.CANCELLED 