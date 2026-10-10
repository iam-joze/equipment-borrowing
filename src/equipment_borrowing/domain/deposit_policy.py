from equipment_borrowing.domain.errors import InvalidDepositRate
from equipment_borrowing.domain.loan_period import LoanPeriod


class DepositPolicy:
    """Domain Service for BR4: deposit = daily rate x loan days.

    Stateless: it holds no data and touches no repository. The application
    service looks up the equipment and passes the rate in.
    """

    def calculate(self, period: LoanPeriod, daily_rate: int) -> int:
        if daily_rate <= 0:
            raise InvalidDepositRate(
                f"Daily deposit rate must be positive, got {daily_rate}"
            )
        return period.days * daily_rate