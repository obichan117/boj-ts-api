# boj-ts-api

Python client for the Bank of Japan Time-Series Statistics API.

## Quick Start

```bash
uv sync --all-extras          # Install all deps
uv run pytest --tb=short      # Run tests
uv run ruff check boj_ts_api/ # Lint
uv run mkdocs build --strict  # Build docs
uv run mkdocs serve           # Serve docs locally
```

## Architecture

```
boj_ts_api/
├── config.py          # BASE_URL, enums (Frequency, Lang, Format), limits
├── exceptions.py      # BOJError → BOJAPIError, BOJRequestError, BOJValidationError
├── models/            # Pydantic v2 response models
│   ├── base.py        # Shared base model config
│   ├── response.py    # DataResponse, MetadataResponse (envelopes)
│   ├── series.py      # SeriesResult, SeriesValues
│   └── metadata.py    # MetadataRecord
├── client/
│   ├── _transport.py  # httpx GET wrapper (SyncTransport + AsyncTransport)
│   ├── _parse.py      # JSON → model validation, error detection
│   ├── sync_client.py # BOJClient
│   └── async_client.py# AsyncBOJClient
├── csv_helper.py      # csv_to_dataframe() (optional pandas)
└── cli.py             # Click CLI: bojts
```

**Core principle: Fetch vs Parse separation.**
- `_transport.py` does I/O (returns raw httpx.Response)
- `_parse.py` transforms data (returns Pydantic models)
- Client modules compose both

## Key Files

- `pyproject.toml` — project config, deps, tool settings
- `tests/conftest.py` — shared fixtures, fixture loading
- `tests/fixtures/` — recorded JSON/CSV responses (no network in tests)

## Testing

All tests use `respx` to mock httpx calls. No network access in tests.

```bash
uv run pytest --tb=short -v
```

## Dependencies

- Core: `httpx`, `pydantic>=2.0`
- Optional: `pandas` (`[pandas]`), `click` (`[cli]`)
- Dev: `pytest`, `pytest-asyncio`, `respx`, `ruff`, `mkdocs`
