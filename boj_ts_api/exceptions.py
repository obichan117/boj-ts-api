"""Exception hierarchy for BOJ API errors."""

from __future__ import annotations


class BOJError(Exception):
    """Base exception for all BOJ API errors."""


class BOJAPIError(BOJError):
    """Raised when the API returns a non-200 STATUS."""

    def __init__(self, status: int, message_id: str, message: str) -> None:
        self.status = status
        self.message_id = message_id
        self.api_message = message
        super().__init__(f"[{status}] {message_id}: {message}")


class BOJRequestError(BOJError):
    """Raised on network / transport errors."""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        self.cause = cause
        super().__init__(message)


class BOJValidationError(BOJError):
    """Raised when request parameters fail local validation."""
