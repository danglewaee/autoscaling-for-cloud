from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class ResidualIntervalCalibrator:
    residual_samples: np.ndarray
    alpha: float
    lower_residual: float
    upper_residual: float

    def interval(self, prediction: float) -> tuple[float, float]:
        lower = max(0.0, prediction + self.lower_residual)
        upper = max(0.0, prediction + self.upper_residual)
        return lower, upper

    def sample_demand(self, prediction: float) -> np.ndarray:
        return np.maximum(prediction + self.residual_samples, 0.0)


def fit_residual_interval_calibrator(
    frame: pd.DataFrame,
    *,
    alpha: float = 0.10,
    target_column: str = "required_capacity",
    prediction_column: str = "forecast_capacity",
) -> ResidualIntervalCalibrator:
    residuals = (
        frame[target_column].astype(float).to_numpy()
        - frame[prediction_column].astype(float).to_numpy()
    )

    if len(residuals) == 0:
        raise ValueError("At least one residual is required for calibration.")

    lower_q = alpha / 2.0
    upper_q = 1.0 - alpha / 2.0
    lower_residual = float(np.quantile(residuals, lower_q))
    upper_residual = float(np.quantile(residuals, upper_q))

    return ResidualIntervalCalibrator(
        residual_samples=residuals,
        alpha=alpha,
        lower_residual=lower_residual,
        upper_residual=upper_residual,
    )


def fit_grouped_residual_interval_calibrators(
    frame: pd.DataFrame,
    *,
    group_column: str = "app",
    min_samples: int = 200,
    alpha: float = 0.10,
    target_column: str = "required_capacity",
    prediction_column: str = "forecast_capacity",
) -> tuple[dict[str, ResidualIntervalCalibrator], ResidualIntervalCalibrator]:
    global_calibrator = fit_residual_interval_calibrator(
        frame,
        alpha=alpha,
        target_column=target_column,
        prediction_column=prediction_column,
    )

    calibrators: dict[str, ResidualIntervalCalibrator] = {}
    for group_value, group_frame in frame.groupby(group_column, sort=False):
        if len(group_frame) < min_samples:
            continue

        calibrators[str(group_value)] = fit_residual_interval_calibrator(
            group_frame,
            alpha=alpha,
            target_column=target_column,
            prediction_column=prediction_column,
        )

    return calibrators, global_calibrator
