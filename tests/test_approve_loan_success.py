from equipment_borrowing.application.dtos import ApproveLoanRequest, ApproveLoanStatus
from equipment_borrowing.domain.borrower_account import BorrowerAccount
from equipment_borrowing.domain.equipment import Equipment, EquipmentStatus
from equipment_borrowing.domain.loan import LoanStatus


def test_T7_successful_approval_is_handled_and_equipment_is_checked_out_BR5(wiring):
    wiring.equipment_repository.save(Equipment("E1", daily_deposit_rate=5000))
    wiring.account_repository.save(BorrowerAccount(borrower_id="B1"))

    result = wiring.service.execute(
        ApproveLoanRequest(borrower_id="B1", equipment_id="E1", days=3, loan_id="L1")
    )

    # Returned outcome (output DTO), including the BR4 deposit: 3 days x 5,000
    assert result.status == ApproveLoanStatus.APPROVED
    assert result.loan_id == "L1"
    assert result.deposit == 15000

    # Aggregate A: the loan was approved and saved
    account = wiring.account_repository.get("B1")
    assert account.get_loan("L1").status == LoanStatus.APPROVED

    # The event was published (nothing left waiting) ...
    assert account.pull_events() == []
    # ... and handled: Aggregate B changed because of it
    assert wiring.equipment_repository.get("E1").status == EquipmentStatus.CHECKED_OUT