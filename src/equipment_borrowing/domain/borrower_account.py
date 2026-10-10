from equipment_borrowing.domain.errors import LoanLimitExceeded
from equipment_borrowing.domain.loan import Loan
from equipment_borrowing.domain.loan_period import LoanPeriod

MAX_ACTIVE_LOANS = 3


class BorrowerAccount:
    """Aggregate Root A. Protects BR3: at most 3 active loans."""

    def __init__(self, borrower_id: str) -> None:
        self.borrower_id = borrower_id
        self._loans: list[Loan] = []

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

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BorrowerAccount) and self.borrower_id == other.borrower_id

    def __hash__(self) -> int:
        return hash(self.borrower_id)