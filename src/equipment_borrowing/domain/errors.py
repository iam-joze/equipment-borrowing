class DomainError(Exception):
    """Base class for every business-rule violation in the domain."""

class InvalidLoanPeriod(DomainError):
    """Raised when a loan period breaks BR1 (must be 1 to 7 days)."""