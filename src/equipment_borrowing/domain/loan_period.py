from dataclasses import dataclass

from equipment_borrowing.domain.errors import InvalidLoanPeriod 

MIN_DAYS = 1
MAX_DAYS = 7

@dataclass(frozen=True)
class LoanPeriod:
    days: int

    def __post_init__(self) -> None:
        if not MIN_DAYS <= self.days <= MAX_DAYS:
            raise InvalidLoanPeriod(
                f"Loan period must be between {MIN_DAYS} and {MAX_DAYS} days, got {self.days}"
            )