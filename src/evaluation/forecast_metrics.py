from __future__ import annotations

import numpy as np
import pandas as pd


def attach_forecast_metrics(
    frame: pd.DataFrame,
    *,
    target_column: str = "required_capacity",
    prediction_column: str = "forecast_capacity",
) -> pd.DataFrame:
    evaluated = frame.copy()
    error = evaluated[prediction_column] - evaluated[target_column]
    evaluated["forecast_error"] = error
    evaluated["abs_error"] = error.abs()
    evaluated["squared_error"] = error.pow(2)
    return evaluated


def attach_quantile_metrics(
    frame: pd.DataFrame,
    *,
    quantile: float,
    target_column: str = "required_capacity",
    prediction_column: str = "forecast_capacity",
) -> pd.DataFrame:
    evaluated = frame.copy()
    target = evaluated[target_column]
    prediction = evaluated[prediction_column]
    residual = target - prediction

    evaluated["pinball_loss"] = np.where(
        residual >= 0,
        quantile * residual,
        (1.0 - quantile) * (-residual),
    )
    evaluated["forecast_quantile"] = quantile
    return evaluated


def summarize_forecast_metrics(
    frame: pd.DataFrame,
    *,
    app_column: str = "app",
) -> pd.DataFrame:
    summary = (
        frame.groupby(app_column, as_index=False)
        .agg(
            forecast_steps=("minute", "size"),
            mae=("abs_error", "mean"),
            rmse=("squared_error", lambda x: float(np.sqrt(x.mean()))),
            mean_forecast_error=("forecast_error", "mean"),
        )
        .sort_values("mae", ascending=False, ignore_index=True)
    )
    return summary


def summarize_quantile_metrics(
    frame: pd.DataFrame,
    *,
    app_column: str = "app",
) -> pd.DataFrame:
    if "pinball_loss" not in frame.columns:
        raise ValueError("pinball_loss column is required for quantile metric summary.")

    summary = (
        frame.groupby(app_column, as_index=False)
        .agg(
            forecast_steps=("minute", "size"),
            pinball_loss=("pinball_loss", "mean"),
        )
        .sort_values("pinball_loss", ascending=False, ignore_index=True)
    )
    return summary


def summarize_overall_forecast(frame: pd.DataFrame) -> pd.Series:
    return pd.Series(
        {
            "forecast_steps": int(len(frame)),
            "mae": float(frame["abs_error"].mean()),
            "rmse": float(np.sqrt(frame["squared_error"].mean())),
            "mean_forecast_error": float(frame["forecast_error"].mean()),
        }
    )


def summarize_overall_quantile(frame: pd.DataFrame) -> pd.Series:
    if "pinball_loss" not in frame.columns:
        raise ValueError("pinball_loss column is required for quantile summary.")

    return pd.Series(
        {
            "forecast_steps": int(len(frame)),
            "pinball_loss": float(frame["pinball_loss"].mean()),
            "forecast_quantile": float(frame["forecast_quantile"].iloc[0]),
        }
    )
