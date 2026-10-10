import pytest

from equipment_borrowing.domain.borrower_account import BorrowerAccount
from equipment_borrowing.domain.errors import InvalidLoanTransition
from equipment_borrowing.domain.events import LoanApproved
from equipment_borrowing.domain.loan_period import LoanPeriod


def test_T5_approving_a_loan_records_loan_approved_event_BR5():
    account = BorrowerAccount(borrower_id="B1")
    account.request_loan("L1", "E1", LoanPeriod(3))

    # Requesting alone is not important enough to raise the event
    assert account.pull_events() == []

    account.approve_loan("L1")

    # Exactly one event, carrying the right IDs
    assert account.pull_events() == [
        LoanApproved(loan_id="L1", borrower_id="B1", equipment_id="E1")
    ]

    # Events are handed over once; a second pull is empty
    assert account.pull_events() == []

    # A rejected approval (BR2) must not record any event
    with pytest.raises(InvalidLoanTransition):
        account.approve_loan("L1")
    assert account.pull_events() == []