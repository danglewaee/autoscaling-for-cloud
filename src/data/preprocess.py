from __future__ import annotations

import argparse
import math
from pathlib import Path

import pandas as pd

from src.data.load_trace import load_azure_trace


def select_top_apps(
    frame: pd.DataFrame,
    *,
    top_k: int = 10,
    min_invocations: int = 1000,
) -> pd.DataFrame:
    counts = (
        frame.groupby("app")
        .size()
        .rename("invocations")
        .reset_index()
        .query("invocations >= @min_invocations")
        .sort_values("invocations", ascending=False)
    )
    keep = counts.head(top_k)["app"].tolist()
    return frame[frame["app"].isin(keep)].copy()


def _expand_invocation_overlaps(frame: pd.DataFrame, bucket_seconds: int) -> pd.DataFrame:
    rows: list[dict[str, float | str | int]] = []

    for record in frame.itertuples(index=False):
        start = float(record.start_timestamp)
        end = float(record.end_timestamp)

        first_bucket = int(math.floor(start / bucket_seconds))
        last_bucket = int(math.floor(max(end - 1e-12, start) / bucket_seconds))

        for minute in range(first_bucket, last_bucket + 1):
            bucket_start = minute * bucket_seconds
            bucket_end = bucket_start + bucket_seconds
            overlap = max(0.0, min(end, bucket_end) - max(start, bucket_start))
            if overlap <= 0.0:
                continue

            rows.append(
                {
                    "app": record.app,
                    "minute": minute,
                    "active_seconds": overlap,
                }
            )

    return pd.DataFrame(rows)


def _compute_peak_concurrency(frame: pd.DataFrame, bucket_seconds: int) -> pd.DataFrame:
    events: list[dict[str, float | str | int]] = []

    for record in frame.itertuples(index=False):
        start = float(record.start_timestamp)
        end = float(record.end_timestamp)

        first_bucket = int(math.floor(start / bucket_seconds))
        last_bucket = int(math.floor(max(end - 1e-12, start) / bucket_seconds))

        for minute in range(first_bucket, last_bucket + 1):
            bucket_start = minute * bucket_seconds
            bucket_end = bucket_start + bucket_seconds
            local_start = max(start, bucket_start)
            local_end = min(end, bucket_end)
            if local_end <= local_start:
                continue

            events.append(
                {
                    "app": record.app,
                    "minute": minute,
                    "timestamp": local_start,
                    "delta": 1,
                }
            )
            events.append(
                {
                    "app": record.app,
                    "minute": minute,
                    "timestamp": local_end,
                    "delta": -1,
                }
            )

    if not events:
        return pd.DataFrame(columns=["app", "minute", "peak_concurrency"])

    event_frame = pd.DataFrame(events)
    grouped_events = (
        event_frame.groupby(["app", "minute", "timestamp"], as_index=False)["delta"].sum()
        .sort_values(["app", "minute", "timestamp"], ignore_index=True)
    )

    peaks: list[dict[str, float | str | int]] = []
    for (app, minute), minute_events in grouped_events.groupby(["app", "minute"], sort=False):
        running = 0
        peak = 0
        for event in minute_events.itertuples(index=False):
            running += int(event.delta)
            peak = max(peak, running)

        peaks.append(
            {
                "app": app,
                "minute": minute,
                "peak_concurrency": peak,
            }
        )

    return pd.DataFrame(peaks)


def aggregate_minute_series(
    frame: pd.DataFrame,
    *,
    bucket_seconds: int = 60,
    utilization_target: float = 1.0,
    capacity_proxy: str = "avg",
) -> pd.DataFrame:
    arrivals = (
        frame.assign(minute=(frame["start_timestamp"] // bucket_seconds).astype(int))
        .groupby(["app", "minute"])
        .size()
        .rename("arrivals")
        .reset_index()
    )

    overlaps = _expand_invocation_overlaps(frame, bucket_seconds)
    active = (
        overlaps.groupby(["app", "minute"], as_index=False)["active_seconds"]
        .sum()
        .sort_values(["app", "minute"])
    )
    peaks = _compute_peak_concurrency(frame, bucket_seconds)

    merged = arrivals.merge(active, on=["app", "minute"], how="outer")
    merged = merged.merge(peaks, on=["app", "minute"], how="outer").fillna(
        {"arrivals": 0, "active_seconds": 0.0}
    )
    merged["arrivals"] = merged["arrivals"].astype(int)
    merged["peak_concurrency"] = merged["peak_concurrency"].fillna(0.0)
    merged["avg_concurrency"] = merged["active_seconds"] / float(bucket_seconds)
    merged["required_capacity_avg"] = (
        merged["avg_concurrency"] / utilization_target
    ).apply(math.ceil)
    merged["required_capacity_peak"] = (
        merged["peak_concurrency"] / utilization_target
    ).apply(math.ceil)
    if capacity_proxy == "avg":
        merged["required_capacity"] = merged["required_capacity_avg"]
    elif capacity_proxy == "peak":
        merged["required_capacity"] = merged["required_capacity_peak"]
    else:
        raise ValueError(f"Unsupported capacity proxy: {capacity_proxy}")

    filled: list[pd.DataFrame] = []
    for app, app_frame in merged.groupby("app", sort=False):
        minute_index = pd.RangeIndex(
            start=int(app_frame["minute"].min()),
            stop=int(app_frame["minute"].max()) + 1,
            step=1,
        )
        dense = (
            app_frame.set_index("minute")
            .reindex(minute_index)
            .rename_axis("minute")
            .reset_index()
        )
        dense["arrivals"] = dense["arrivals"].fillna(0).astype(int)
        dense["active_seconds"] = dense["active_seconds"].fillna(0.0)
        dense["peak_concurrency"] = dense["peak_concurrency"].fillna(0.0)
        dense["avg_concurrency"] = dense["active_seconds"] / float(bucket_seconds)
        dense["required_capacity_avg"] = (
            dense["avg_concurrency"] / utilization_target
        ).apply(math.ceil)
        dense["required_capacity_peak"] = (
            dense["peak_concurrency"] / utilization_target
        ).apply(math.ceil)
        if capacity_proxy == "avg":
            dense["required_capacity"] = dense["required_capacity_avg"]
        else:
            dense["required_capacity"] = dense["required_capacity_peak"]
        dense["app"] = app
        filled.append(dense)

    result = pd.concat(filled, ignore_index=True)
    result["start_time_s"] = result["minute"] * bucket_seconds
    result["end_time_s"] = result["start_time_s"] + bucket_seconds
    return result[
        [
            "app",
            "minute",
            "start_time_s",
            "end_time_s",
            "arrivals",
            "active_seconds",
            "avg_concurrency",
            "peak_concurrency",
            "required_capacity_avg",
            "required_capacity_peak",
            "required_capacity",
        ]
    ].sort_values(["app", "minute"], ignore_index=True)


def preprocess_trace(
    input_path: str | Path,
    output_path: str | Path,
    *,
    top_k_apps: int = 10,
    min_invocations: int = 1000,
    bucket_seconds: int = 60,
    utilization_target: float = 1.0,
    capacity_proxy: str = "avg",
    nrows: int | None = None,
) -> pd.DataFrame:
    frame = load_azure_trace(input_path, nrows=nrows)
    frame = select_top_apps(frame, top_k=top_k_apps, min_invocations=min_invocations)
    minute_series = aggregate_minute_series(
        frame,
        bucket_seconds=bucket_seconds,
        utilization_target=utilization_target,
        capacity_proxy=capacity_proxy,
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    minute_series.to_csv(output_path, index=False)
    return minute_series


def main() -> None:
    parser = argparse.ArgumentParser(description="Build minute-level Azure traces.")
    parser.add_argument("--input", required=True, help="Path to raw Azure trace.")
    parser.add_argument("--output", required=True, help="Where to write the CSV.")
    parser.add_argument("--top-k-apps", type=int, default=10)
    parser.add_argument("--min-invocations", type=int, default=1000)
    parser.add_argument("--bucket-seconds", type=int, default=60)
    parser.add_argument("--utilization-target", type=float, default=1.0)
    parser.add_argument(
        "--capacity-proxy",
        choices=["avg", "peak"],
        default="avg",
        help="Which capacity proxy to expose as required_capacity.",
    )
    parser.add_argument("--nrows", type=int, default=None)
    args = parser.parse_args()

    minute_series = preprocess_trace(
        args.input,
        args.output,
        top_k_apps=args.top_k_apps,
        min_invocations=args.min_invocations,
        bucket_seconds=args.bucket_seconds,
        utilization_target=args.utilization_target,
        capacity_proxy=args.capacity_proxy,
        nrows=args.nrows,
    )
    print(minute_series.head().to_string(index=False))
    print(f"\nSaved {len(minute_series)} rows to {args.output}")


if __name__ == "__main__":
    main()
