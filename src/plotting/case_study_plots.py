from __future__ import annotations

from pathlib import Path

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
