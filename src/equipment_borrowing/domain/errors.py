class DomainError(Exception):
    """Base class for every business-rule violation in the domain."""

class InvalidLoanPeriod(DomainError):
    """Raised when a loan period breaks BR1 (must be 1 to 7 days)."""

class InvalidLoanTransition(DomainError):
    """Raised when a loan state change breaks BR2"""

class LoanLimitExceeded(DomainError):
    """Raised when a borrower would exceed 3 active loans (BR3)."""

class InvalidDepositRate(DomainError):
    """Raised when the daily deposit rate is not positive (BR4)."""

class LoanNotFound(DomainError):
    """Raised when an account is asked about a loan it does not hold."""

class EquipmentUnavailable(DomainError):
    """Raised when equipment that is not available is asked to check out (BR5)."""