# pyboj

Beginner-friendly Python client for the [Bank of Japan Time-Series Statistics API](https://www.stat-search.boj.or.jp/).

[![PyPI](https://img.shields.io/pypi/v/pyboj)](https://pypi.org/project/pyboj/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Built on top of [boj-ts-api](https://pypi.org/project/boj-ts-api/) for advanced users who need direct API access.

## Installation

```bash
pip install pyboj
```

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

See the [full documentation](https://obichan117.github.io/pyboj/) for all 14 methods, filter enums, and domain wrapper properties.

## License

MIT
