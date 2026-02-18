# boj-ts-api

Python client for the [Bank of Japan Time-Series Statistics API](https://www.stat-search.boj.or.jp/).

## Features

- **Sync & async** clients with identical API surface
- **Pydantic v2** models for type-safe responses
- **Auto-pagination** via `iter_data_code()` / `iter_data_layer()`
- **CSV support** with optional pandas integration
- **CLI** for quick terminal access (`bojts`)

## Installation

```bash
pip install boj-ts-api
```

Optional extras:

```bash
pip install boj-ts-api[pandas]  # pandas DataFrame support
pip install boj-ts-api[cli]     # CLI tool
```

## Quick Start

```python
from boj_ts_api import BOJClient

with BOJClient(lang="en") as client:
    resp = client.get_data_code(
        db="CO",
        code="TK99F1000601GCQ01000",
        start_date="202401",
        end_date="202404",
    )
    for series in resp.RESULTSET:
        print(series.SERIES_CODE, series.VALUES.VALUES)
```
