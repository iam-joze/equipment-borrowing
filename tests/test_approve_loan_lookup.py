from equipment_borrowing.application.dtos import ApproveLoanRequest, ApproveLoanStatus
from equipment_borrowing.domain.borrower_account import BorrowerAccount


def test_T6_unknown_equipment_is_reported_and_no_loan_is_created_BR6(wiring):
    wiring.account_repository.save(BorrowerAccount(borrower_id="B1"))
    # no equipment saved: nothing exists

    result = wiring.service.execute(
        ApproveLoanRequest(borrower_id="B1", equipment_id="E404", days=3, loan_id="L1")
    )

    assert result.status == ApproveLoanStatus.EQUIPMENT_NOT_FOUND
    assert result.loan_id is None
    assert result.deposit is None
    # The failed lookup stopped the use case before touching the account
    assert wiring.account_repository.get("B1").loans == ()