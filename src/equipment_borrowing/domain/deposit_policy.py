from equipment_borrowing.domain.loan_period import LoanPeriod


class DepositPolicy:
    def calculate(self, period: LoanPeriod, daily_rate: int) -> int:
        return period.days * daily_rate