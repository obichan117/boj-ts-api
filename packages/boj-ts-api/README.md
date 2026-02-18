# boj-ts-api

Generic Python client for the [Bank of Japan Time-Series Statistics API](https://www.stat-search.boj.or.jp/).

Low-level, typed wrapper around the BOJ API endpoints. For a beginner-friendly interface, see [pyboj](https://github.com/obichan117/pyboj).

## Installation

```bash
pip install boj-ts-api
```

## Usage

```python
from boj_ts_api import Client

with Client(lang="en") as client:
    resp = client.get_data_code(db="CO", code="TK99F1000601GCQ01000")
    for series in resp.RESULTSET:
        print(series.SERIES_CODE, series.VALUES.VALUES)
```

## License

MIT
