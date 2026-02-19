"""BOJ operations domain wrapper (OB01-OB02 databases)."""

from __future__ import annotations

import re
from enum import Enum

from pyboj._domains._base import Series


class OperationType(str, Enum):
    """BOJ operation type classification."""

    GOVT_RECEIPTS = "govt_receipts"
    GOVT_PAYMENTS = "govt_payments"
    JGB_OPERATIONS = "jgb_operations"
    LENDING = "lending"
    REPO_OPERATIONS = "repo_operations"
    OUTRIGHT_PURCHASE = "outright_purchase"
    COLLATERAL = "collateral"
    TOTAL = "total"
    OTHER = "other"


_OPERATION_PATTERNS: list[tuple[str, OperationType]] = [
    (r"[Rr]eceipt.*[Gg]ovt|[Gg]ovt.*[Rr]eceipt|[Tt]reasury.*[Rr]eceipt",
     OperationType.GOVT_RECEIPTS),
    (r"[Pp]ayment.*[Gg]ovt|[Gg]ovt.*[Pp]ayment|[Tt]reasury.*[Pp]ayment",
     OperationType.GOVT_PAYMENTS),
    (r"JGB|[Gg]overnment\s*[Bb]ond|[Gg]ovt.*[Bb]ond", OperationType.JGB_OPERATIONS),
    (r"[Ll]ending|[Ll]oan\s*[Ss]upply", OperationType.LENDING),
    (r"[Rr]epo|[Gg]ensaki", OperationType.REPO_OPERATIONS),
    (r"[Oo]utright\s*[Pp]urchase", OperationType.OUTRIGHT_PURCHASE),
    (r"[Cc]ollateral", OperationType.COLLATERAL),
    (r"[Tt]otal", OperationType.TOTAL),
]


def _detect_operation(name: str) -> OperationType:
    """Detect the operation type from a BOJ series name."""
    for pattern, op in _OPERATION_PATTERNS:
        if re.search(pattern, name):
            return op
    return OperationType.OTHER


class BOJOperation(Series):
    """Domain wrapper for BOJ operations series (OB01-OB02)."""

    @property
    def operation_type(self) -> OperationType:
        """Detected operation type."""
        return _detect_operation(self.name or "")
