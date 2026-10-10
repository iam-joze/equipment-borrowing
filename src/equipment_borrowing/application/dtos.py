from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class ApproveLoanRequest:
    """Input DTO."""

    borrower_id: str
    equipment_id: str
    days: int
    loan_id: str


class ApproveLoanStatus(Enum):
    APPROVED = "APPROVED"
    EQUIPMENT_NOT_FOUND = "EQUIPMENT_NOT_FOUND"


@dataclass(frozen=True)
class ApproveLoanResult:
    """Output DTO."""

    status: ApproveLoanStatus
    loan_id: str | None = None
    deposit: int | None = None
    message: str = ""