from dataclasses import dataclass

import pytest

from equipment_borrowing.application.approve_loan_service import ApproveLoanService
from equipment_borrowing.application.check_out_equipment_handler import (
    CheckOutEquipmentHandler,
)
from equipment_borrowing.domain.deposit_policy import DepositPolicy
from equipment_borrowing.domain.events import LoanApproved
from equipment_borrowing.infrastructure.in_memory_repositories import (
    InMemoryBorrowerAccountRepository,
    InMemoryEquipmentRepository,
)
from equipment_borrowing.infrastructure.in_process_dispatcher import (
    InProcessEventDispatcher,
)


@dataclass
class Wiring:
    service: ApproveLoanService
    equipment_repository: InMemoryEquipmentRepository
    account_repository: InMemoryBorrowerAccountRepository


@pytest.fixture
def wiring() -> Wiring:
    """Builds the whole object graph with fresh, empty in-memory repositories.
    This is dependency injection: everything is created outside the service
    and handed to it."""
    equipment_repository = InMemoryEquipmentRepository()
    account_repository = InMemoryBorrowerAccountRepository()

    dispatcher = InProcessEventDispatcher()
    handler = CheckOutEquipmentHandler(equipment_repository)
    dispatcher.subscribe(LoanApproved, handler.handle)

    service = ApproveLoanService(
        equipment_repository, account_repository, DepositPolicy(), dispatcher
    )
    return Wiring(service, equipment_repository, account_repository)