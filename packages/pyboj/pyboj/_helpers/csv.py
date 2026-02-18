"""Optional pandas helper for converting CSV text to DataFrames."""

from __future__ import annotations

import io


def csv_to_dataframe(csv_text: str | bytes, *, encoding: str = "utf-8"):
    """Convert CSV text from the BOJ API into a pandas DataFrame.

    Requires pandas to be installed (``pip install pyboj[pandas]``).

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
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            "pandas is required for csv_to_dataframe(). "
            "Install it with: pip install pyboj[pandas]"
        ) from exc

    if isinstance(csv_text, bytes):
        csv_text = csv_text.decode(encoding)

    return pd.read_csv(io.StringIO(csv_text))
