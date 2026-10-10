from abc import ABC, abstractmethod

from equipment_borrowing.domain.borrower_account import BorrowerAccount
from equipment_borrowing.domain.equipment import Equipment


class EquipmentRepository(ABC):
    @abstractmethod
    def get(self, equipment_id: str) -> Equipment | None:
        """Return the equipment, or None if it does not exist."""

    @abstractmethod
    def save(self, equipment: Equipment) -> None: ...


class BorrowerAccountRepository(ABC):
    @abstractmethod
    def get(self, borrower_id: str) -> BorrowerAccount | None:
        """Return the account, or None if it does not exist."""

    @abstractmethod
    def save(self, account: BorrowerAccount) -> None: ...