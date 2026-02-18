"""Pandas helper for converting CSV text to DataFrames."""

from __future__ import annotations

import io

import pandas as pd


def csv_to_dataframe(csv_text: str | bytes, *, encoding: str = "utf-8") -> pd.DataFrame:
    """Convert CSV text from the BOJ API into a pandas DataFrame.

    Parameters
    ----------
    csv_text:
        Raw CSV text returned by a ``*_csv()`` client method. Accepts ``str``
        (already decoded) or ``bytes`` (decoded using *encoding*).
    encoding:
        Encoding for *csv_text* when it is ``bytes``. The BOJ API uses UTF-8
        for English (``lang=en``) and Shift-JIS for Japanese (``lang=jp``).
        Use ``encoding="shift_jis"`` for Japanese CSV responses.

    Returns
    -------
    pandas.DataFrame
    """
    if isinstance(csv_text, bytes):
        csv_text = csv_text.decode(encoding)

    return pd.read_csv(io.StringIO(csv_text))
