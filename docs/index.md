# boj-ts-api

Python client for the [Bank of Japan Time-Series Statistics API](https://www.stat-search.boj.or.jp/).

This library wraps the official BOJ API announced on [February 18, 2026](https://www.boj.or.jp/statistics/outline/notice_2026/not260218a.htm), which provides machine-readable access (JSON/CSV) to the Bank of Japan's time-series statistical data.

## Features

- **Sync & async** clients with identical API surface (`Client` / `AsyncClient`)
- **Pydantic v2** models for type-safe, validated responses
- **Auto-pagination** via `iter_data_code()` / `iter_data_layer()` generators
- **CSV support** with optional pandas DataFrame conversion
- **PEP 561** typed package

## Packages

This project is a monorepo with two pip-installable packages:

| Package | Audience | Install |
|---------|----------|---------|
| **boj-ts-api** | Advanced users who want direct, typed API access | `pip install boj-ts-api` |
| **pyboj** | Beginners who want convenience helpers (e.g. pandas) | `pip install pyboj` |

`pyboj` depends on `boj-ts-api` and re-exports everything, plus adds utilities like `csv_to_dataframe()`.

## Quick Example

```python
from boj_ts_api import Client

with Client(lang="en") as client:
    resp = client.get_data_code(
        db="CO",
        code="TK99F1000601GCQ01000",
        start_date="202401",
        end_date="202404",
    )
    for series in resp.RESULTSET:
        print(series.SERIES_CODE, series.VALUES.VALUES)
```

## Official BOJ Resources

- [BOJ API Announcement (2026-02-18)](https://www.boj.or.jp/statistics/outline/notice_2026/not260218a.htm)
- [BOJ Time-Series Search Site](https://www.stat-search.boj.or.jp/)
- [Upstream API Reference](boj-api.md) — full endpoint/parameter documentation
- [OpenAPI Specification](https://github.com/obichan117/boj-ts-api/blob/main/openapi.yaml)
