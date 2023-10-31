from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional, Any

from pandas import DataFrame, read_csv
from pansql import sqldf


def query_csv(
    *,
    input_file_path: Path,
    pandas_kwargs: Dict[str, Any],
    sql_query: Optional[str],
    escape_formulas: bool,
) -> DataFrame:
    defaults: Dict[str, Any] = {
        "index_col": False,
    }

    def _read_csv(encoding: Optional[str] = None) -> DataFrame:
        return read_csv(
            filepath_or_buffer=input_file_path,
            **{
                **defaults,
                **pandas_kwargs,
                **({"encoding": encoding} if encoding else {}),
            },
        )

    if pandas_kwargs.get("encoding", None) == "auto":
        try:
            df = _read_csv("utf-8")
        except UnicodeDecodeError:
            df = _read_csv("latin1")
    else:
        df = _read_csv()

    if sql_query is not None:
        df = sqldf(sql_query, {"df": df})

    if escape_formulas:

        def f(value: Any) -> Any:
            if isinstance(value, str) and value[0] == "=":
                return f"'{value}"
            return value

        df = df.applymap(f)

    return df
