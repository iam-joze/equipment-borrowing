from dataclasses import dataclass

@dataclass(frozen=True)
class LoanPeriod:
    days: int