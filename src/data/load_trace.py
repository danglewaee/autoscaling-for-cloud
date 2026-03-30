from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import pandas as pd

EXPECTED_COLUMNS = ["app", "func", "end_timestamp", "duration"]


def _normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    renamed = {column: column.strip().lower() for column in frame.columns}
    frame = frame.rename(columns=renamed)

    if list(frame.columns) == EXPECTED_COLUMNS:
        return frame

    if len(frame.columns) == len(EXPECTED_COLUMNS):
        frame.columns = EXPECTED_COLUMNS
        return frame

    raise ValueError(
        f"Unexpected columns: {list(frame.columns)}. Expected {EXPECTED_COLUMNS}."
    )


def load_azure_trace(
    path: str | Path,
    *,
    nrows: int | None = None,
    app_ids: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Load the Azure Functions 2021 invocation trace."""

    frame = pd.read_csv(path, sep=r"\s+", engine="python", nrows=nrows)
    frame = _normalize_columns(frame)

    frame["app"] = frame["app"].astype(str)
    frame["func"] = frame["func"].astype(str)
    frame["end_timestamp"] = frame["end_timestamp"].astype(float)
    frame["duration"] = frame["duration"].astype(float)
    frame["start_timestamp"] = frame["end_timestamp"] - frame["duration"]

    if app_ids is not None:
        app_ids = set(app_ids)
        frame = frame[frame["app"].isin(app_ids)].copy()

    frame = frame.sort_values(["app", "start_timestamp", "end_timestamp"]).reset_index(
        drop=True
    )
    return frame


def summarize_trace(frame: pd.DataFrame) -> pd.Series:
    return pd.Series(
        {
            "rows": int(len(frame)),
            "apps": int(frame["app"].nunique()),
            "functions": int(frame[["app", "func"]].drop_duplicates().shape[0]),
            "start_s_min": float(frame["start_timestamp"].min()),
            "end_s_max": float(frame["end_timestamp"].max()),
            "duration_mean_s": float(frame["duration"].mean()),
            "duration_p95_s": float(frame["duration"].quantile(0.95)),
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Load and summarize Azure trace data.")
    parser.add_argument("--input", required=True, help="Path to the raw trace file.")
    parser.add_argument("--nrows", type=int, default=None, help="Optional row limit.")
    args = parser.parse_args()

    frame = load_azure_trace(args.input, nrows=args.nrows)
    summary = summarize_trace(frame)
    print(summary.to_string())


if __name__ == "__main__":
    main()
