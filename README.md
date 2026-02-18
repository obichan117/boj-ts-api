# pyboj

Python client for the [Bank of Japan Time-Series Statistics API](https://www.stat-search.boj.or.jp/).

[![PyPI](https://img.shields.io/pypi/v/pyboj)](https://pypi.org/project/pyboj/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Wraps the official BOJ API ([announced 2026-02-18](https://www.boj.or.jp/statistics/outline/notice_2026/not260218a.htm)) for machine-readable access to Japan's central bank time-series data.

## Features

- **Sync & async** clients with identical API surface (`Client` / `AsyncClient`)
- **Pydantic v2** models for type-safe, validated responses
- **Auto-pagination** via `iter_data_code()` / `iter_data_layer()` generators
- **CSV support** with optional pandas DataFrame conversion
- **Domain wrappers** — `ExchangeRate`, `InterestRate`, `PriceIndex` with parsed dates and domain-specific properties
- **Database enum** — named constants for all BOJ database codes
- **PEP 561** typed package

## Packages

| Package | Install | Description |
|---------|---------|-------------|
| **boj-ts-api** | `pip install boj-ts-api` | Low-level typed API client |
| **pyboj** | `pip install pyboj` | Beginner-friendly wrapper with domain objects and pandas support |

## Quick Start

```python
from boj_ts_api import Client, Lang

with Client(lang=Lang.EN) as client:
    # Fetch CPI data for Tokyo
    resp = client.get_data_code(
        db="CO",
        code="TK99F1000601GCQ01000",
        start_date="202401",
        end_date="202404",
    )
    for series in resp.RESULTSET:
        print(series.SERIES_CODE, series.VALUES.VALUES)

    # Auto-paginate all results
    for series in client.iter_data_code(db="CO", code="TK99F1000601GCQ01000"):
        print(series.SERIES_CODE, len(series.VALUES.SURVEY_DATES), "periods")

    # Metadata
    meta = client.get_metadata(db="FM08")
    for rec in meta.RESULTSET[:3]:
        print(rec.SERIES_CODE, rec.NAME_OF_TIME_SERIES)
```

### Domain Wrappers (pyboj)

```python
from pyboj import Client, Lang, Database, ExchangeRate

with Client(lang=Lang.EN) as client:
    resp = client.get_data_code(
        db=Database.EXCHANGE_RATES,
        code="FM08'MAINAVG",
    )
    rate = ExchangeRate(resp.RESULTSET[0])

    print(rate.currency_pair)   # "USD/JPY"
    print(rate.rate_type)       # RateType.AVERAGE
    print(rate.dates[:3])       # [datetime.date(...), ...]
    print(rate.values[:3])      # [148.12, 149.56, 151.34]
    df = rate.to_dataframe()    # pandas DataFrame
```

### Async

```python
import asyncio
from boj_ts_api import AsyncClient, Lang

async def main():
    async with AsyncClient(lang=Lang.EN) as client:
        resp = await client.get_data_code(db="CO", code="TK99F1000601GCQ01000")
        print(resp.RESULTSET[0].VALUES.VALUES)

asyncio.run(main())
```

### CSV + pandas

```python
from pyboj import Client, Lang, csv_to_dataframe

with Client(lang=Lang.EN) as client:
    csv_text = client.get_data_code_csv(db="CO", code="TK99F1000601GCQ01000")
    df = csv_to_dataframe(csv_text)
    print(df.head())
```

## API Endpoints

| Endpoint | Client Method | Description |
|----------|---------------|-------------|
| `/api/v1/getDataCode` | `get_data_code()`, `iter_data_code()`, `get_data_code_csv()` | Fetch data by series code |
| `/api/v1/getDataLayer` | `get_data_layer()`, `iter_data_layer()`, `get_data_layer_csv()` | Fetch data by category hierarchy |
| `/api/v1/getMetadata` | `get_metadata()`, `get_metadata_csv()` | Fetch series catalogue |

## Documentation

- [Getting Started](https://obichan117.github.io/pyboj/getting-started/)
- [API Reference](https://obichan117.github.io/pyboj/api-reference/)
- [Upstream BOJ API Reference](https://obichan117.github.io/pyboj/boj-api/)
- [OpenAPI Specification (Interactive)](https://obichan117.github.io/pyboj/openapi-spec/)
- [OpenAPI Specification (YAML)](openapi.yaml)

## Official BOJ Resources

- [BOJ API Announcement (2026-02-18)](https://www.boj.or.jp/statistics/outline/notice_2026/not260218a.htm)
- [BOJ Time-Series Search Site](https://www.stat-search.boj.or.jp/)

## License

MIT
