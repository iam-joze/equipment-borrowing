from equipment_borrowing.application.repositories import (
    BorrowerAccountRepository,
    EquipmentRepository,
)
from equipment_borrowing.domain.borrower_account import BorrowerAccount
from equipment_borrowing.domain.equipment import Equipment


class InMemoryEquipmentRepository(EquipmentRepository):
    def __init__(self) -> None:
        self._items: dict[str, Equipment] = {}

    def get(self, equipment_id: str) -> Equipment | None:
        return self._items.get(equipment_id)

    def save(self, equipment: Equipment) -> None:
        self._items[equipment.equipment_id] = equipment


class InMemoryBorrowerAccountRepository(BorrowerAccountRepository):
    def __init__(self) -> None:
        self._items: dict[str, BorrowerAccount] = {}

    def get(self, borrower_id: str) -> BorrowerAccount | None:
        return self._items.get(borrower_id)

    def save(self, account: BorrowerAccount) -> None:
        self._items[account.borrower_id] = account

    