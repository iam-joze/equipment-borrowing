class Equipment:
    """Aggregate Root B (rules added in T7/T8). Identified by equipment_id."""

    def __init__(self, equipment_id: str, daily_deposit_rate: int) -> None:
        self.equipment_id = equipment_id
        self.daily_deposit_rate = daily_deposit_rate

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Equipment) and self.equipment_id == other.equipment_id

    def __hash__(self) -> int:
        return hash(self.equipment_id)