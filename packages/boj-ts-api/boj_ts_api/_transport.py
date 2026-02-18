"""HTTP transport layer — sync and async wrappers around httpx."""

from __future__ import annotations

from typing import Any

import httpx

from boj_ts_api._types.config import BASE_URL, DEFAULT_TIMEOUT
from boj_ts_api._types.exceptions import BOJRequestError


class SyncTransport:
    """Synchronous HTTP transport using httpx.Client."""

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        client: httpx.Client | None = None,
    ) -> None:
        self._owns_client = client is None
        self._client = client or httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers={"Accept-Encoding": "gzip"},
        )

    def get(self, path: str, params: dict[str, Any]) -> httpx.Response:
        """Send GET request and return the raw httpx.Response."""
        try:
            resp = self._client.get(path, params=params)
            resp.raise_for_status()
            return resp
        except httpx.HTTPStatusError as exc:
            raise BOJRequestError(
                f"HTTP {exc.response.status_code} from {exc.request.url}", cause=exc
            ) from exc
        except httpx.HTTPError as exc:
            raise BOJRequestError(str(exc), cause=exc) from exc

    def close(self) -> None:
        if self._owns_client:
            self._client.close()


class AsyncTransport:
    """Asynchronous HTTP transport using httpx.AsyncClient."""

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers={"Accept-Encoding": "gzip"},
        )

    async def get(self, path: str, params: dict[str, Any]) -> httpx.Response:
        """Send GET request and return the raw httpx.Response."""
        try:
            resp = await self._client.get(path, params=params)
            resp.raise_for_status()
            return resp
        except httpx.HTTPStatusError as exc:
            raise BOJRequestError(
                f"HTTP {exc.response.status_code} from {exc.request.url}", cause=exc
            ) from exc
        except httpx.HTTPError as exc:
            raise BOJRequestError(str(exc), cause=exc) from exc

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()
