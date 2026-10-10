from equipment_borrowing.application.approve_loan_service import ApproveLoanService
from equipment_borrowing.application.check_out_equipment_handler import (
    CheckOutEquipmentHandler,
)
from equipment_borrowing.application.dtos import ApproveLoanRequest
from equipment_borrowing.domain.borrower_account import BorrowerAccount
from equipment_borrowing.domain.deposit_policy import DepositPolicy
from equipment_borrowing.domain.equipment import Equipment
from equipment_borrowing.domain.errors import DomainError
from equipment_borrowing.domain.events import LoanApproved
from equipment_borrowing.infrastructure.in_memory_repositories import (
    InMemoryBorrowerAccountRepository,
    InMemoryEquipmentRepository,
)
from equipment_borrowing.infrastructure.in_process_dispatcher import (
    InProcessEventDispatcher,
)


def build_service(equipment_repository, account_repository) -> ApproveLoanService:
    """Composition root: the one place that knows the concrete classes and
    connects them. Everything is created here and injected from outside."""
    dispatcher = InProcessEventDispatcher()
    handler = CheckOutEquipmentHandler(equipment_repository)
    dispatcher.subscribe(LoanApproved, handler.handle)  # the BR5 wiring
    return ApproveLoanService(
        equipment_repository, account_repository, DepositPolicy(), dispatcher
    )


def main() -> None:
    equipment_repository = InMemoryEquipmentRepository()
    account_repository = InMemoryBorrowerAccountRepository()
    service = build_service(equipment_repository, account_repository)

    equipment_repository.save(Equipment("E1", daily_deposit_rate=5000))
    account_repository.save(BorrowerAccount("B1"))
    account_repository.save(BorrowerAccount("B2"))

    scenarios = [
        ("Happy path: B1 borrows E1 for 3 days",
         ApproveLoanRequest("B1", "E1", days=3, loan_id="L1")),
        ("Equipment already taken: B2 borrows E1",
         ApproveLoanRequest("B2", "E1", days=2, loan_id="L2")),
        ("Unknown equipment: B1 borrows E404",
         ApproveLoanRequest("B1", "E404", days=2, loan_id="L3")),
        ("Invalid period: B1 borrows E1 for 10 days",
         ApproveLoanRequest("B1", "E1", days=10, loan_id="L4")),
    ]

    for title, request in scenarios:
        print(title)
        try:
            result = service.execute(request)
            print(
                f"  -> {result.status.value} | loan={result.loan_id} "
                f"| deposit={result.deposit} | {result.message}"
            )
        except DomainError as error:
            print(f"  -> REJECTED by domain rule: {error}")


if __name__ == "__main__":
    main()