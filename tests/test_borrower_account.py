import pytest

from equipment_borrowing.domain.borrower_account import BorrowerAccount
from equipment_borrowing.domain.errors import LoanLimitExceeded
from equipment_borrowing.domain.loan_period import LoanPeriod


def test_T3_borrower_cannot_hold_more_than_three_active_loans_BR3():
    account = BorrowerAccount(borrower_id="B1")

    # Boundary: the 3rd loan (the last allowed one) is accepted
    for number in (1, 2, 3):
        account.request_loan(f"L{number}", "E1", LoanPeriod(2))
    assert account.active_loan_count() == 3

    # Rejection: the 4th loan breaks the invariant
    with pytest.raises(LoanLimitExceeded):
        account.request_loan("L4", "E2", LoanPeriod(2))

    # A rejected request changes nothing
    assert account.active_loan_count() == 3
    assert len(account.loans) == 3