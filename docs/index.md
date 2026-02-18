# pyboj

Python client for the [Bank of Japan Time-Series Statistics API](https://www.stat-search.boj.or.jp/).

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/obichan117/pyboj/blob/main/examples/quickstart.ipynb)

This library wraps the official BOJ API announced on [February 18, 2026](https://www.boj.or.jp/statistics/outline/notice_2026/not260218a.htm), which provides machine-readable access (JSON/CSV) to the Bank of Japan's time-series statistical data.

## Features

- **`BOJ` client** — typed domain methods for all 13 BOJ categories (43 databases), no magic strings
- **Enum-driven filtering** — `Currency`, `RateType`, `TankanIndustry`, `BopAccount`, `IndustrySector`, etc.
- **Domain wrappers** — `ExchangeRate`, `InterestRate`, `PriceIndex`, `Tankan`, `BalanceOfPayments`, `MoneyDeposit`, `Loan`, and more
- **Metadata-driven** — auto-fetches metadata and filters series by your criteria
- **Sync & async** low-level clients with identical API surface (`Client` / `AsyncClient`)
- **Pydantic v2** models for type-safe, validated responses
- **Auto-pagination** via `iter_data_code()` / `iter_data_layer()` generators
- **CSV + pandas** support with `to_dataframe()` and `csv_to_dataframe()`
- **Database enum** — named constants for all BOJ database codes (`Database.EXCHANGE_RATES` instead of `"FM08"`)
- **PEP 561** typed package

## Packages

This project is a monorepo with two pip-installable packages:

| Package | Audience | Install |
|---------|----------|---------|
| **pyboj** | Everyone — high-level client with domain wrappers | `pip install pyboj` |
| **boj-ts-api** | Advanced users who want direct, typed API access | `pip install boj-ts-api` |

`pyboj` depends on `boj-ts-api` and re-exports everything, plus adds:

- `BOJ` client with typed domain methods
- `Currency`, `TankanIndustry`, `BopAccount` and other filter enums
- `ExchangeRate`, `InterestRate`, `Tankan` and other domain wrappers
- `Database` enum for all BOJ database codes
- `csv_to_dataframe()` for pandas conversion

## Quick Example

```python
from pyboj import BOJ, Currency, Frequency

boj = BOJ()

# Exchange rates — typed, no magic strings
rates = boj.exchange_rates(
    currency=Currency.USD_JPY,
    frequency=Frequency.D,
    start_date="202401",
)
for r in rates:
    print(r.currency_pair, r.rate_type, r.values[:3])
    df = r.to_dataframe()  # pandas DataFrame
```

## Official BOJ Resources

- [BOJ API Announcement (2026-02-18)](https://www.boj.or.jp/statistics/outline/notice_2026/not260218a.htm)
- [BOJ Time-Series Search Site](https://www.stat-search.boj.or.jp/)
- [Upstream API Reference](boj-api.md) — full endpoint/parameter documentation
- [OpenAPI Specification](openapi-spec.md) — interactive Swagger-like API explorer
