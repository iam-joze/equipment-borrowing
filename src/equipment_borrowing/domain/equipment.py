from enum import Enum
from equipment_borrowing.domain.errors import EquipmentUnavailable

class EquipmentStatus(Enum):
    AVAILABLE = "AVAILABLE"
    CHECKED_OUT = "CHECKED_OUT"


class Equipment:
    """Aggregate Root B. Identified by equipment_id."""

    def __init__(
        self,
        equipment_id: str,
        daily_deposit_rate: int,
        status: EquipmentStatus = EquipmentStatus.AVAILABLE,
    ) -> None:
        self.equipment_id = equipment_id
        self.daily_deposit_rate = daily_deposit_rate
        self._status = status

    @property
    def status(self) -> EquipmentStatus:
        return self._status

    def check_out(self) -> None:
        if self._status != EquipmentStatus.AVAILABLE:
            raise EquipmentUnavailable(
                f"Equipment {self.equipment_id} is not available (status: {self._status.value})"
            )
        self._status = EquipmentStatus.CHECKED_OUT

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Equipment) and self.equipment_id == other.equipment_id

    def __hash__(self) -> int:
        return hash(self.equipment_id)