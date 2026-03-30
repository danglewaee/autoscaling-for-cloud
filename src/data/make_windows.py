from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass
class WindowedDataset:
    features: np.ndarray
    targets: np.ndarray
    apps: np.ndarray
    anchor_minutes: np.ndarray


def split_minutes(
    frame: pd.DataFrame,
    *,
    train_fraction: float = 0.70,
    val_fraction: float = 0.15,
) -> tuple[int, int]:
    minute_min = int(frame["minute"].min())
    minute_max = int(frame["minute"].max())
    total = minute_max - minute_min + 1

    train_cut = minute_min + int(total * train_fraction)
    val_cut = train_cut + int(total * val_fraction)
    return train_cut, val_cut


def build_windows(
    frame: pd.DataFrame,
    *,
    history_minutes: int = 60,
    horizons: Iterable[int] = (5, 10, 15),
    target_column: str = "required_capacity",
) -> dict[int, WindowedDataset]:
    horizons = tuple(sorted(set(int(h) for h in horizons)))
    outputs: dict[int, WindowedDataset] = {}

    for horizon in horizons:
        features: list[np.ndarray] = []
        targets: list[float] = []
        apps: list[str] = []
        anchor_minutes: list[int] = []

        for app, app_frame in frame.groupby("app", sort=False):
            values = app_frame[target_column].to_numpy(dtype=float)
            minutes = app_frame["minute"].to_numpy(dtype=int)

            if len(values) < history_minutes + horizon:
                continue

            for end_idx in range(history_minutes - 1, len(values) - horizon):
                start_idx = end_idx - history_minutes + 1
                features.append(values[start_idx : end_idx + 1])
                targets.append(values[end_idx + horizon])
                apps.append(app)
                anchor_minutes.append(int(minutes[end_idx]))

        outputs[horizon] = WindowedDataset(
            features=np.asarray(features, dtype=float),
            targets=np.asarray(targets, dtype=float),
            apps=np.asarray(apps),
            anchor_minutes=np.asarray(anchor_minutes, dtype=int),
        )

    return outputs
