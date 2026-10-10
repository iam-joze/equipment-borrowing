from enum import Enum

from equipment_borrowing.domain.errors import InvalidLoanTransition
from equipment_borrowing.domain.loan_period import LoanPeriod


class LoanStatus(Enum):
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    RETURNED = "RETURNED"
    CANCELLED = "CANCELLED"


# BR2: the only legal moves. Anything not listed here is rejected.
_ALLOWED_TRANSITIONS: dict[LoanStatus, set[LoanStatus]] = {
    LoanStatus.REQUESTED: {LoanStatus.APPROVED},
    LoanStatus.APPROVED: {LoanStatus.RETURNED, LoanStatus.CANCELLED},
    LoanStatus.RETURNED: set(),
    LoanStatus.CANCELLED: set(),
}


class Loan:
    def __init__(self, loan_id: str, equipment_id: str, period: LoanPeriod) -> None:
        self.loan_id = loan_id
        self.equipment_id = equipment_id
        self.period = period
        self._status = LoanStatus.REQUESTED

    @property
    def status(self) -> LoanStatus:
        return self._status

    def approve(self) -> None:
        self._transition_to(LoanStatus.APPROVED)

    def mark_returned(self) -> None:
        self._transition_to(LoanStatus.RETURNED)

    def cancel(self) -> None:
        self._transition_to(LoanStatus.CANCELLED)

    def _transition_to(self, new_status: LoanStatus) -> None:
        if new_status not in _ALLOWED_TRANSITIONS[self._status]:
            raise InvalidLoanTransition(
                f"Loan {self.loan_id} cannot move from "
                f"{self._status.value} to {new_status.value}"
            )
        self._status = new_status

    # Identity: two Loan objects are the same loan if they share a loan_id
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Loan) and self.loan_id == other.loan_id

    def __hash__(self) -> int:
        return hash(self.loan_id)

    @property
    def is_active(self) -> bool:
        return self._status in {LoanStatus.REQUESTED, LoanStatus.APPROVED}
    