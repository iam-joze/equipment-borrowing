from equipment_borrowing.domain.errors import LoanLimitExceeded, LoanNotFound
from equipment_borrowing.domain.events import LoanApproved
from equipment_borrowing.domain.loan import Loan
from equipment_borrowing.domain.loan_period import LoanPeriod

MAX_ACTIVE_LOANS = 3


class BorrowerAccount:
    """Aggregate Root A. Protects BR3 (at most 3 active loans) and
    records the LoanApproved event for BR5."""

    def __init__(self, borrower_id: str) -> None:
        self.borrower_id = borrower_id
        self._loans: list[Loan] = []
        self._events: list[LoanApproved] = []

    @property
    def loans(self) -> tuple[Loan, ...]:
        # A copy: callers can read the loans but cannot add or remove them
        return tuple(self._loans)

    def active_loan_count(self) -> int:
        return sum(1 for loan in self._loans if loan.is_active)

    def request_loan(self, loan_id: str, equipment_id: str, period: LoanPeriod) -> Loan:
        if self.active_loan_count() >= MAX_ACTIVE_LOANS:
            raise LoanLimitExceeded(
                f"Borrower {self.borrower_id} already has {MAX_ACTIVE_LOANS} active loans"
            )
        loan = Loan(loan_id, equipment_id, period)
        self._loans.append(loan)
        return loan

    def approve_loan(self, loan_id: str) -> None:
        loan = self.get_loan(loan_id)
        loan.approve()  # BR2 is enforced here; if it raises, no event is recorded
        self._events.append(
            LoanApproved(
                loan_id=loan.loan_id,
                borrower_id=self.borrower_id,
                equipment_id=loan.equipment_id,
            )
        )

    def cancel_loan(self, loan_id: str) -> None:
        self.get_loan(loan_id).cancel()  # BR2: only an approved loan can be cancelled

    def pull_events(self) -> list[LoanApproved]:
        """Hand over the recorded events and clear them, so each is published once."""
        events, self._events = self._events, []
        return events

    def get_loan(self, loan_id: str) -> Loan:
        for loan in self._loans:
            if loan.loan_id == loan_id:
                return loan
        raise LoanNotFound(f"Borrower {self.borrower_id} has no loan {loan_id}")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BorrowerAccount) and self.borrower_id == other.borrower_id

    def __hash__(self) -> int:
        return hash(self.borrower_id)