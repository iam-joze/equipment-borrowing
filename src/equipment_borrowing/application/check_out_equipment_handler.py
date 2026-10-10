from equipment_borrowing.application.repositories import EquipmentRepository
from equipment_borrowing.domain.events import LoanApproved


class CheckOutEquipmentHandler:
    """Use case 2 (BR5): reacts to LoanApproved by checking out the equipment.

    It coordinates only: load Aggregate B, ask it to act, save it. The rule
    about *when* check-out is allowed belongs to Equipment itself.
    """

    def __init__(self, equipment_repository: EquipmentRepository) -> None:
        self._equipment_repository = equipment_repository

    def handle(self, event: LoanApproved) -> None:
        # BR6 already guaranteed this equipment exists
        equipment = self._equipment_repository.get(event.equipment_id)
        equipment.check_out()
        self._equipment_repository.save(equipment)