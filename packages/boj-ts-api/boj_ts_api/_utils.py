"""Shared internal utilities for parameter handling."""

from __future__ import annotations

from typing import Any

from boj_ts_api._types.exceptions import BOJValidationError


def _validate_required(**kwargs: str | None) -> None:
    for name, value in kwargs.items():
        if value is None or value == "":
            raise BOJValidationError(f"Parameter '{name}' is required and cannot be empty.")


def _set_optional(params: dict[str, Any], **kwargs: Any) -> None:
    for key, value in kwargs.items():
        if value is not None:
            params[key] = value
