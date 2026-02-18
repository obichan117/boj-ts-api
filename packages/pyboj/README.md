# pyboj

Beginner-friendly Python client for the [Bank of Japan Time-Series Statistics API](https://www.stat-search.boj.or.jp/).

Built on top of [boj-ts-api](https://pypi.org/project/boj-ts-api/) for advanced users who need direct API access.

## Installation

```bash
pip install pyboj
```

With pandas support:

```bash
pip install pyboj[pandas]
```

## Usage

```python
from pyboj import Client, csv_to_dataframe

with Client(lang="en") as client:
    resp = client.get_data_code(db="CO", code="TK99F1000601GCQ01000")
    for series in resp.RESULTSET:
        print(series.SERIES_CODE, series.VALUES.VALUES)

    # CSV + pandas
    csv_text = client.get_data_code_csv(db="CO", code="TK99F1000601GCQ01000")
    df = csv_to_dataframe(csv_text)
    print(df.head())
```

## License

MIT
