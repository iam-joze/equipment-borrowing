from equipment_borrowing.application.dtos import ApproveLoanRequest, ApproveLoanResult
from equipment_borrowing.application.repositories import (
    BorrowerAccountRepository,
    EquipmentRepository,
)


class ApproveLoanService:
    def __init__(
        self,
        equipment_repository: EquipmentRepository,
        account_repository: BorrowerAccountRepository,
    ) -> None:
        self._equipment_repository = equipment_repository
        self._account_repository = account_repository

    def execute(self, request: ApproveLoanRequest) -> ApproveLoanResult:
        raise NotImplementedError