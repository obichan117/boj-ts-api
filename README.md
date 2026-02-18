# pyboj

Python client for the [Bank of Japan Time-Series Statistics API](https://www.stat-search.boj.or.jp/).

[![PyPI](https://img.shields.io/pypi/v/pyboj)](https://pypi.org/project/pyboj/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Wraps the official BOJ API ([announced 2026-02-18](https://www.boj.or.jp/statistics/outline/notice_2026/not260218a.htm)) for machine-readable access to Japan's central bank time-series data.

## Quick Start

```python
from pyboj import BOJ, Currency, Frequency

boj = BOJ()

# Exchange rates — no magic strings
rates = boj.exchange_rates(
    currency=Currency.USD_JPY,
    frequency=Frequency.D,
    start_date="202401",
)
for r in rates:
    print(r.currency_pair, r.rate_type, r.values[:3])
    df = r.to_dataframe()  # pandas DataFrame

# Interest rates
rates = boj.interest_rates(frequency=Frequency.D)
for r in rates:
    print(r.rate_category, r.collateralization, r.tenor)

# TANKAN survey
from pyboj import TankanIndustry, TankanSize
results = boj.tankan(
    industry=TankanIndustry.MANUFACTURING,
    size=TankanSize.LARGE,
)

# Price indices
indices = boj.price_indices(start_date="202401")

# Balance of payments, Money/Deposits, Loans, and more
bop = boj.balance_of_payments()
money = boj.money_deposits()
loans = boj.loans()
```

## Features

- **`BOJ` client** — typed domain methods for all 13 BOJ categories (43 databases)
- **Enum-driven filtering** — `Currency`, `RateType`, `TankanIndustry`, `BopAccount`, etc.
- **Domain wrappers** — `ExchangeRate`, `InterestRate`, `PriceIndex`, `Tankan`, and more
- **Metadata-driven** — auto-fetches metadata and filters series by your criteria
- **Sync & async** low-level clients with identical API surface
- **Pydantic v2** models for type-safe, validated responses
- **Auto-pagination** via `iter_data_code()` / `iter_data_layer()` generators
- **CSV + pandas** support with `to_dataframe()` and `csv_to_dataframe()`
- **PEP 561** typed package

## Packages

| Package | Install | Description |
|---------|---------|-------------|
| **pyboj** | `pip install pyboj` | High-level client with domain wrappers and pandas support |
| **boj-ts-api** | `pip install boj-ts-api` | Low-level typed API client |

## Advanced: Low-Level API

```python
from boj_ts_api import Client, Lang

with Client(lang=Lang.EN) as client:
    # Fetch data by series code
    resp = client.get_data_code(db="CO", code="TK99F1000601GCQ01000")
    for series in resp.RESULTSET:
        print(series.SERIES_CODE, series.VALUES.VALUES)

    # Auto-paginate
    for series in client.iter_data_code(db="CO", code="TK99F1000601GCQ01000"):
        print(series.SERIES_CODE, len(series.VALUES.SURVEY_DATES), "periods")

    # Metadata
    meta = client.get_metadata(db="FM08")
    for rec in meta.RESULTSET[:3]:
        print(rec.SERIES_CODE, rec.NAME_OF_TIME_SERIES)
```

## Documentation

- [Getting Started](https://obichan117.github.io/pyboj/getting-started/)
- [API Reference](https://obichan117.github.io/pyboj/api-reference/)
- [Upstream BOJ API Reference](https://obichan117.github.io/pyboj/boj-api/)
- [OpenAPI Specification (Interactive)](https://obichan117.github.io/pyboj/openapi-spec/)

## Official BOJ Resources

- [BOJ API Announcement (2026-02-18)](https://www.boj.or.jp/statistics/outline/notice_2026/not260218a.htm)
- [BOJ Time-Series Search Site](https://www.stat-search.boj.or.jp/)

## License

MIT
