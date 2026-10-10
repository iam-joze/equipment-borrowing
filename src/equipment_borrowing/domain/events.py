from dataclasses import dataclass


@dataclass(frozen=True)
class LoanApproved:
    """Fact: a loan was approved. Raised by BorrowerAccount (BR5)."""

    loan_id: str
    borrower_id: str
    equipment_id: str