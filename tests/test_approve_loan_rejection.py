from equipment_borrowing.application.dtos import ApproveLoanRequest, ApproveLoanStatus
from equipment_borrowing.domain.borrower_account import BorrowerAccount
from equipment_borrowing.domain.equipment import Equipment, EquipmentStatus
from equipment_borrowing.domain.loan import LoanStatus


def test_T8_equipment_rejects_follow_up_and_loan_is_cancelled_BR5(wiring):
    # Equipment is already on loan to someone else
    wiring.equipment_repository.save(
        Equipment("E1", daily_deposit_rate=5000, status=EquipmentStatus.CHECKED_OUT)
    )
    wiring.account_repository.save(BorrowerAccount(borrower_id="B1"))

    result = wiring.service.execute(
        ApproveLoanRequest(borrower_id="B1", equipment_id="E1", days=3, loan_id="L1")
    )

    # Returned outcome: the follow-up was rejected, no deposit is charged
    assert result.status == ApproveLoanStatus.EQUIPMENT_UNAVAILABLE
    assert result.loan_id == "L1"
    assert result.deposit is None

    # Final state of Aggregate A: the loan was cancelled and no longer counts (BR3)
    account = wiring.account_repository.get("B1")
    assert account.get_loan("L1").status == LoanStatus.CANCELLED
    assert account.active_loan_count() == 0

    # Final state of Aggregate B: unchanged
    assert wiring.equipment_repository.get("E1").status == EquipmentStatus.CHECKED_OUT