from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.calibration.interval_calibration import ResidualIntervalCalibrator
from src.policy.decision_objective import choose_capacity


@dataclass
class RiskCalibratedConfig:
    initial_capacity: int = 1
    min_capacity: int = 0
    cost_weight: float = 1.0
    underprovision_weight: float = 8.0
    oscillation_weight: float = 0.25
    candidate_buffer: int = 5


def simulate_risk_calibrated_policy(
    frame: pd.DataFrame,
    *,
    calibrator: ResidualIntervalCalibrator,
    config: RiskCalibratedConfig | None = None,
    prediction_column: str = "forecast_capacity",
) -> pd.DataFrame:
    if config is None:
        config = RiskCalibratedConfig()

    app_frame = frame.sort_values("minute").reset_index(drop=True).copy()

    previous_capacity = max(config.initial_capacity, config.min_capacity)
    capacities: list[int] = []
    objectives: list[float] = []
    interval_low: list[float] = []
    interval_high: list[float] = []

    for row in app_frame.itertuples(index=False):
        prediction = float(getattr(row, prediction_column))
        samples = calibrator.sample_demand(prediction)
        low, high = calibrator.interval(prediction)
        chosen_capacity, objective_value = choose_capacity(
            samples,
            previous_capacity=previous_capacity,
            min_capacity=config.min_capacity,
            cost_weight=config.cost_weight,
            underprovision_weight=config.underprovision_weight,
            oscillation_weight=config.oscillation_weight,
            candidate_buffer=config.candidate_buffer,
        )

        capacities.append(chosen_capacity)
        objectives.append(objective_value)
        interval_low.append(low)
        interval_high.append(high)
        previous_capacity = chosen_capacity

    app_frame["interval_low"] = interval_low
    app_frame["interval_high"] = interval_high
    app_frame["provisioned_capacity"] = capacities
    app_frame["decision_objective"] = objectives
    return app_frame
