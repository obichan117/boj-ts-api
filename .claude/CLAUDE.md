# pyboj (monorepo)

Two-package monorepo for the Bank of Japan Time-Series Statistics API.

## Quick Start

```bash
uv sync --all-extras                              # Install all deps
uv run python -m pytest --tb=short                # Run all tests
uv run ruff check packages/                       # Lint all packages
uv run python -m pytest packages/boj-ts-api/tests --tb=short  # Test boj-ts-api only
uv run python -m pytest packages/pyboj/tests --tb=short        # Test pyboj only
```

## Architecture (Monorepo)

```
packages/
├── boj-ts-api/                  # LOW-LEVEL: generic API client (pip install boj-ts-api)
│   ├── boj_ts_api/
│   │   ├── __init__.py          #   exports Client, AsyncClient, models, enums, exceptions
│   │   ├── _base_client.py      #   shared param-building logic for sync/async clients
│   │   ├── _types/              #   data contracts
│   │   │   ├── config.py        #     BASE_URL, endpoints, enums (Lang, Frequency, Format), limits
│   │   │   ├── exceptions.py    #     BOJError hierarchy
│   │   │   └── models/          #     Pydantic response schemas (ResponseEnvelope base)
│   │   ├── _transport.py        #   httpx wrappers (SyncTransport, AsyncTransport)
│   │   ├── _parse.py            #   JSON → Pydantic
│   │   ├── _utils.py            #   shared parameter validation
│   │   ├── client.py            #   Client (sync), inherits _BaseClient
│   │   └── async_client.py      #   AsyncClient, inherits _BaseClient
│   └── tests/
│
└── pyboj/                       # HIGH-LEVEL: friendly wrapper (pip install pyboj)
    ├── pyboj/
    │   ├── __init__.py          #   re-exports BOJ, Series, all enums, low-level types
    │   ├── _boj.py              #   BOJ client — 13 typed domain methods
    │   ├── _config.py           #   Database enum (43 databases)
    │   ├── _utils.py            #   frequency_matches helper
    │   ├── _domains/            #   domain wrapper objects
    │   │   ├── _base.py         #     Series base class (dates, values, to_dataframe)
    │   │   ├── exchange_rate.py #     ExchangeRate, Currency, RateType
    │   │   ├── interest_rate.py #     InterestRate, RateCategory, Collateralization
    │   │   ├── price_index.py   #     PriceIndex, IndexType
    │   │   ├── tankan.py        #     Tankan, TankanIndustry/Size/Item/SeriesType/Timing
    │   │   ├── balance_of_payments.py  # BalanceOfPayments, BopAccount
    │   │   ├── money_deposit.py #     MoneyDeposit, MonetaryComponent, Adjustment
    │   │   └── loan.py          #     Loan, IndustrySector
    │   ├── _parsing/            #   date parsing
    │   └── _helpers/            #   utility tools
    │       └── csv.py           #     DataFrame conversion
    └── tests/
```

**Dependency:** `pyboj → boj-ts-api` (enforced by pip)

**Core principles:**
- Fetch vs Parse separation (transport → parse → client)
- Metadata-driven filtering: BOJ client fetches metadata, filters by enums, batches codes
- Detection functions: standalone `_detect_*()` functions used by both wrappers and filters
- `Database` enum str() returns "Database.X" in Python 3.11+; use `.value` for API calls

## Key Files

- `pyproject.toml` — workspace root (uv workspace config, shared tool settings)
- `packages/boj-ts-api/pyproject.toml` — low-level package config
- `packages/pyboj/pyproject.toml` — high-level package config
- `packages/pyboj/pyboj/_boj.py` — **BOJ high-level client** (main entry point)
- `packages/boj-ts-api/tests/fixtures/` — recorded JSON/CSV responses (no network in tests)

## Testing

All tests use `respx` to mock httpx calls. No network access in tests.
**Important:** Use `uv run python -m pytest` (not `uv run pytest`) for correct module resolution.

```bash
uv run python -m pytest --tb=short -v
```

## Dependencies

- boj-ts-api: `httpx`, `pydantic>=2.0`
- pyboj: `boj-ts-api`, `pandas`
- Dev: `pytest`, `pytest-asyncio`, `respx`, `ruff`, `mkdocs`
