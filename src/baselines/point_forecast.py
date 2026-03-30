from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
import pandas as pd

from src.data.make_windows import build_windows


@dataclass
class PointForecastConfig:
    history_window: int = 30
    horizon: int = 5
    initial_capacity: int = 1
    min_capacity: int = 0
    target_column: str = "required_capacity"


@dataclass
class LinearAutoregressiveModel:
    weights: np.ndarray
    bias: float
    history_window: int
    horizon: int
    target_column: str

    def predict_array(self, features: np.ndarray) -> np.ndarray:
        return features @ self.weights + self.bias

    def predict_one(self, history: np.ndarray) -> float:
        return float(self.predict_array(history.reshape(1, -1))[0])


def fit_linear_autoregressive_model(
    frame: pd.DataFrame,
    *,
    config: PointForecastConfig | None = None,
) -> LinearAutoregressiveModel:
    if config is None:
        config = PointForecastConfig()

    datasets = build_windows(
        frame,
        history_minutes=config.history_window,
        horizons=(config.horizon,),
        target_column=config.target_column,
    )
    dataset = datasets[config.horizon]

    if len(dataset.features) == 0:
        raise ValueError("Not enough training windows to fit the point forecast model.")

    x = dataset.features
    y = dataset.targets
    x_design = np.hstack([x, np.ones((len(x), 1), dtype=float)])
    coeffs, _, _, _ = np.linalg.lstsq(x_design, y, rcond=None)

    return LinearAutoregressiveModel(
        weights=coeffs[:-1],
        bias=float(coeffs[-1]),
        history_window=config.history_window,
        horizon=config.horizon,
        target_column=config.target_column,
    )


def simulate_point_forecast_policy(
    frame: pd.DataFrame,
    model: LinearAutoregressiveModel,
    *,
    initial_capacity: int = 1,
    min_capacity: int = 0,
) -> pd.DataFrame:
    """Predict current demand using history available horizon steps earlier."""

    app_frame = frame.sort_values("minute").reset_index(drop=True).copy()
    values = app_frame[model.target_column].to_numpy(dtype=float)

    forecasts: list[float] = []
    capacities: list[int] = []
    used_fallback: list[int] = []

    min_target_idx = model.history_window + model.horizon - 1

    for target_idx in range(len(app_frame)):
        if target_idx < min_target_idx:
            forecast = float(initial_capacity)
            fallback = 1
        else:
            history_end = target_idx - model.horizon
            history_start = history_end - model.history_window + 1
            history = values[history_start : history_end + 1]
            forecast = model.predict_one(history)
            fallback = 0

        capacity = max(math.ceil(max(forecast, 0.0)), min_capacity)
        forecasts.append(forecast)
        capacities.append(capacity)
        used_fallback.append(fallback)

    app_frame["forecast_capacity"] = forecasts
    app_frame["provisioned_capacity"] = capacities
    app_frame["used_fallback_forecast"] = used_fallback
    return app_frame
