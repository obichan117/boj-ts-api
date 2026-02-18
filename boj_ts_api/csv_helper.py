"""Optional pandas helper for converting CSV text to DataFrames."""

from __future__ import annotations

import io


def csv_to_dataframe(csv_text: str):
    """Convert CSV text from the BOJ API into a pandas DataFrame.

    Requires pandas to be installed (``pip install boj-ts-api[pandas]``).

    Parameters
    ----------
    csv_text : str
        Raw CSV text returned by a ``*_csv()`` client method.

    Returns
    -------
    pandas.DataFrame
    """
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            "pandas is required for csv_to_dataframe(). "
            "Install it with: pip install boj-ts-api[pandas]"
        ) from exc

    return pd.read_csv(io.StringIO(csv_text))
