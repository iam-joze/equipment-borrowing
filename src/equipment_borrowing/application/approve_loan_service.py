from equipment_borrowing.application.dtos import (
    ApproveLoanRequest,
    ApproveLoanResult,
    ApproveLoanStatus,
)
from equipment_borrowing.application.event_dispatcher import EventDispatcher
from equipment_borrowing.application.repositories import (
    BorrowerAccountRepository,
    EquipmentRepository,
)
from equipment_borrowing.domain.deposit_policy import DepositPolicy
from equipment_borrowing.domain.errors import EquipmentUnavailable
from equipment_borrowing.domain.loan_period import LoanPeriod


class ApproveLoanService:
    """Application Service for the main use case. It coordinates; the business
    rules live in the domain objects it calls."""

    def __init__(
        self,
        equipment_repository: EquipmentRepository,
        account_repository: BorrowerAccountRepository,
        deposit_policy: DepositPolicy,
        event_dispatcher: EventDispatcher,
    ) -> None:
        self._equipment_repository = equipment_repository
        self._account_repository = account_repository
        self._deposit_policy = deposit_policy
        self._event_dispatcher = event_dispatcher

    def execute(self, request: ApproveLoanRequest) -> ApproveLoanResult:
        # BR6: the equipment must exist before anything else happens
        equipment = self._equipment_repository.get(request.equipment_id)
        if equipment is None:
            return ApproveLoanResult(
                status=ApproveLoanStatus.EQUIPMENT_NOT_FOUND,
                message=f"Equipment {request.equipment_id} does not exist",
            )

        account = self._account_repository.get(request.borrower_id)

        # Checks that change nothing come first
        period = LoanPeriod(request.days)  # BR1
        deposit = self._deposit_policy.calculate(  # BR4
            period, equipment.daily_deposit_rate
        )

        # Changes to Aggregate A
        account.request_loan(request.loan_id, request.equipment_id, period)  # BR3
        account.approve_loan(request.loan_id)  # BR2, records LoanApproved
        self._account_repository.save(account)

        # Publish only after A is saved (BR5)
        try:
            for event in account.pull_events():
                self._event_dispatcher.publish(event)
        except EquipmentUnavailable as rejection:
            # Aggregate B refused the follow-up: compensate by cancelling the loan
            account = self._account_repository.get(request.borrower_id)
            account.cancel_loan(request.loan_id)
            self._account_repository.save(account)
            return ApproveLoanResult(
                status=ApproveLoanStatus.EQUIPMENT_UNAVAILABLE,
                loan_id=request.loan_id,
                message=str(rejection),
            )

        return ApproveLoanResult(
            status=ApproveLoanStatus.APPROVED,
            loan_id=request.loan_id,
            deposit=deposit,
            message="Loan approved",
        )