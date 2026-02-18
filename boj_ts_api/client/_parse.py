"""Response parsing — JSON to Pydantic models with error detection."""

from __future__ import annotations

from typing import Any

import httpx

from boj_ts_api.exceptions import BOJAPIError, BOJRequestError
from boj_ts_api.models.response import DataResponse, MetadataResponse


def parse_data_response(response: httpx.Response) -> DataResponse:
    """Parse a Code/Layer API JSON response into a DataResponse model."""
    data = _extract_json(response)
    resp = DataResponse.model_validate(data)
    _check_status(resp.STATUS, resp.MESSAGEID, resp.MESSAGE)
    return resp


def parse_metadata_response(response: httpx.Response) -> MetadataResponse:
    """Parse a Metadata API JSON response into a MetadataResponse model."""
    data = _extract_json(response)
    resp = MetadataResponse.model_validate(data)
    _check_status(resp.STATUS, resp.MESSAGEID, resp.MESSAGE)
    return resp


def _extract_json(response: httpx.Response) -> dict[str, Any]:
    """Extract JSON body from httpx response."""
    try:
        return response.json()
    except Exception as exc:
        raise BOJRequestError(
            f"Failed to decode JSON response: {exc}", cause=exc
        ) from exc


def _check_status(status: int, message_id: str, message: str) -> None:
    """Raise BOJAPIError if the API STATUS is not 200."""
    if status != 200:
        raise BOJAPIError(status=status, message_id=message_id, message=message)
