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

        # The rest of the use case is driven by T7
        raise NotImplementedError("Success path is added when T7 is written")