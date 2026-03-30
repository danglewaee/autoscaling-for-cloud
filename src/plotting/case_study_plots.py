from __future__ import annotations

from pathlib import Path
from typing import Mapping

import matplotlib.pyplot as plt
import pandas as pd


def plot_capacity_case_study(
    frame: pd.DataFrame,
    *,
    output_path: str | Path,
    title: str | None = None,
    max_points: int = 300,
) -> Path:
    plot_frame = frame.sort_values("minute").reset_index(drop=True).copy()
    if max_points and len(plot_frame) > max_points:
        plot_frame = plot_frame.tail(max_points).copy()

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(
        plot_frame["minute"],
        plot_frame["required_capacity"],
        label="Required Capacity",
        linewidth=2.0,
    )

    if "forecast_capacity" in plot_frame.columns:
        ax.plot(
            plot_frame["minute"],
            plot_frame["forecast_capacity"],
            label="Forecast",
            linewidth=1.8,
            alpha=0.9,
        )

    if "provisioned_capacity" in plot_frame.columns:
        ax.step(
            plot_frame["minute"],
            plot_frame["provisioned_capacity"],
            label="Provisioned Capacity",
            where="post",
            linewidth=1.8,
        )

    ax.set_xlabel("Minute Bucket")
    ax.set_ylabel("Capacity")
    ax.set_title(title or "Autoscaling Case Study")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


METHOD_LABELS = {
    "reactive": "Reactive",
    "point_forecast": "Point Forecast",
    "risk_calibrated": "Risk-Calibrated",
}

METHOD_COLORS = {
    "reactive": "#d62728",
    "point_forecast": "#1f77b4",
    "risk_calibrated": "#2ca02c",
}


def plot_burst_case_study(
    method_frames: Mapping[str, pd.DataFrame],
    *,
    output_path: str | Path,
    burst_start_minute: int,
    burst_end_minute: int,
    context_minutes: int = 10,
    title: str | None = None,
) -> Path:
    if not method_frames:
        raise ValueError("method_frames must not be empty.")

    window_start = int(burst_start_minute) - int(context_minutes)
    window_end = int(burst_end_minute) + int(context_minutes)

    windowed: dict[str, pd.DataFrame] = {}
    for method_name, frame in method_frames.items():
        ordered = frame.sort_values("minute").reset_index(drop=True).copy()
        subset = ordered[
            (ordered["minute"] >= window_start) & (ordered["minute"] <= window_end)
        ].copy()
        if subset.empty:
            raise ValueError(
                f"No rows found for method '{method_name}' in minute window "
                f"[{window_start}, {window_end}]."
            )
        windowed[method_name] = subset

    reference_method = (
        "risk_calibrated"
        if "risk_calibrated" in windowed
        else next(iter(windowed.keys()))
    )
    reference = windowed[reference_method]

    fig, (ax_top, ax_bottom) = plt.subplots(
        2,
        1,
        figsize=(12, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [2.2, 1.4]},
    )

    for axis in (ax_top, ax_bottom):
        axis.axvspan(
            burst_start_minute,
            burst_end_minute + 1,
            color="#ffdd57",
            alpha=0.18,
            linewidth=0,
        )

    ax_top.plot(
        reference["minute"],
        reference["required_capacity"],
        color="black",
        linewidth=2.2,
        label="Required Capacity",
        zorder=5,
    )

    for method_name in ["reactive", "point_forecast", "risk_calibrated"]:
        if method_name not in windowed:
            continue
        method_frame = windowed[method_name]
        total_under = float(method_frame.get("underprovision", pd.Series(dtype=float)).sum())
        label = f"{METHOD_LABELS.get(method_name, method_name)} (under={total_under:.0f})"
        ax_top.step(
            method_frame["minute"],
            method_frame["provisioned_capacity"],
            where="post",
            linewidth=1.8,
            alpha=0.95,
            color=METHOD_COLORS.get(method_name),
            label=label,
        )

    risk_frame = windowed.get("risk_calibrated", reference)
    ax_bottom.plot(
        risk_frame["minute"],
        risk_frame["required_capacity"],
        color="black",
        linewidth=2.0,
        label="Required Capacity",
        zorder=5,
    )

    if {"interval_low", "interval_high"}.issubset(risk_frame.columns):
        ax_bottom.fill_between(
            risk_frame["minute"],
            risk_frame["interval_low"],
            risk_frame["interval_high"],
            color=METHOD_COLORS["risk_calibrated"],
            alpha=0.22,
            label="Risk-Calibrated Interval",
        )

    if "forecast_capacity" in risk_frame.columns:
        ax_bottom.plot(
            risk_frame["minute"],
            risk_frame["forecast_capacity"],
            color="#ff7f0e",
            linewidth=1.8,
            linestyle="--",
            label="Risk-Calibrated Forecast",
        )

    ax_bottom.step(
        risk_frame["minute"],
        risk_frame["provisioned_capacity"],
        where="post",
        linewidth=1.6,
        color=METHOD_COLORS["risk_calibrated"],
        label="Risk-Calibrated Provisioned",
    )

    ax_top.set_ylabel("Capacity")
    ax_bottom.set_ylabel("Capacity")
    ax_bottom.set_xlabel("Minute Bucket")
    ax_top.set_title("Policy Comparison Around a Selected Burst")
    ax_bottom.set_title("Risk-Calibrated Forecast Interval on the Same Episode")

    for axis in (ax_top, ax_bottom):
        axis.grid(alpha=0.25)
        axis.legend(loc="upper left", ncol=2 if axis is ax_top else 1)

    fig.suptitle(title or "Burst Case Study", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.97))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=220)
    plt.close(fig)
    return output_path
