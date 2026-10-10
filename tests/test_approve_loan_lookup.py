from equipment_borrowing.application.approve_loan_service import ApproveLoanService
from equipment_borrowing.application.dtos import ApproveLoanRequest, ApproveLoanStatus
from equipment_borrowing.domain.borrower_account import BorrowerAccount
from equipment_borrowing.infrastructure.in_memory_repositories import (
    InMemoryBorrowerAccountRepository,
    InMemoryEquipmentRepository,
)


def test_T6_unknown_equipment_is_reported_and_no_loan_is_created_BR6():
    equipment_repository = InMemoryEquipmentRepository()  # empty: no equipment exists
    account_repository = InMemoryBorrowerAccountRepository()
    account_repository.save(BorrowerAccount(borrower_id="B1"))

    # Dependency injection: repositories are supplied from outside
    service = ApproveLoanService(equipment_repository, account_repository)

    result = service.execute(
        ApproveLoanRequest(borrower_id="B1", equipment_id="E404", days=3, loan_id="L1")
    )

    assert result.status == ApproveLoanStatus.EQUIPMENT_NOT_FOUND
    assert result.loan_id is None
    assert result.deposit is None
    # The failed lookup stopped the use case before touching the account
    assert account_repository.get("B1").loans == ()