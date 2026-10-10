import pytest

from equipment_borrowing.domain.deposit_policy import DepositPolicy
from equipment_borrowing.domain.errors import InvalidDepositRate
from equipment_borrowing.domain.loan_period import LoanPeriod


def test_T4_deposit_is_daily_rate_times_days_and_rejects_invalid_rate_BR4():
    policy = DepositPolicy()

    # Normal case: 3 days x 5,000 UGX
    assert policy.calculate(LoanPeriod(3), daily_rate=5000) == 15000

    # Boundaries: shortest and longest allowed periods
    assert policy.calculate(LoanPeriod(1), daily_rate=5000) == 5000
    assert policy.calculate(LoanPeriod(7), daily_rate=5000) == 35000

    # Rejection: a rate that is zero or negative is meaningless
    for bad_rate in (0, -100):
        with pytest.raises(InvalidDepositRate):
            policy.calculate(LoanPeriod(3), daily_rate=bad_rate)