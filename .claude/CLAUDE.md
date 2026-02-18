# pyboj (monorepo)

Two-package monorepo for the Bank of Japan Time-Series Statistics API.

## Quick Start

```bash
uv sync --all-extras                              # Install all deps
uv run pytest --tb=short                          # Run all tests
uv run ruff check packages/                       # Lint all packages
uv run pytest packages/boj-ts-api/tests --tb=short  # Test boj-ts-api only
uv run pytest packages/pyboj/tests --tb=short        # Test pyboj only
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
    │   ├── __init__.py          #   re-exports from boj_ts_api + helpers
    │   └── _helpers/            #   utility tools
    │       └── csv.py           #     DataFrame conversion
    └── tests/
```

**Dependency:** `pyboj → boj-ts-api` (enforced by pip)

**Core principle: Fetch vs Parse separation.**
- `_transport.py` does I/O (returns raw httpx.Response)
- `_parse.py` transforms data (returns Pydantic models)
- `_base_client.py` builds params and validates
- Client modules compose all three (thin wrappers)

## Key Files

- `pyproject.toml` — workspace root (uv workspace config, shared tool settings)
- `packages/boj-ts-api/pyproject.toml` — low-level package config
- `packages/pyboj/pyproject.toml` — high-level package config
- `packages/boj-ts-api/tests/fixtures/` — recorded JSON/CSV responses (no network in tests)

## Testing

All tests use `respx` to mock httpx calls. No network access in tests.

```bash
uv run pytest --tb=short -v
```

## Dependencies

- boj-ts-api: `httpx`, `pydantic>=2.0`
- pyboj: `boj-ts-api`, optional `pandas`
- Dev: `pytest`, `pytest-asyncio`, `respx`, `ruff`, `mkdocs`
