# Calibration-Aware Autoscaling

This repo is the execution workspace for a first paper in `systems + applied ML`.

The scope is intentionally narrow:

- Dataset: Azure Functions Invocation Trace 2021
- Unit of analysis: application-level demand traces
- Bucket size: 1 minute
- Forecast horizons: 5, 10, 15 minutes
- Phase-1 target: average concurrent demand per minute
- Primary downstream metrics: cost, SLA violation rate, underprovision ratio, oscillation

## Why this framing

This project is not trying to win by inventing a large new model. The contribution is:

- calibrated uncertainty for scaling decisions,
- decision-aware evaluation beyond MAE or RMSE,
- reproducible comparison on a public workload trace.

## Repo layout

```text
calibration-aware-autoscaling/
  README.md
  requirements.txt
  .gitignore
  configs/
    data.yaml
  docs/
    data_spec_azure2021.md
  src/
    baselines/
      fixed_quantile.py
      moving_average.py
      point_forecast.py
      reactive.py
    calibration/
      interval_calibration.py
      metrics.py
    data/
      load_trace.py
      preprocess.py
      make_windows.py
    evaluation/
      forecast_metrics.py
      scaling_metrics.py
    policy/
      decision_objective.py
      risk_calibrated_scaling.py
    plotting/
      case_study_plots.py
  experiments/
    run_fixed_quantile.py
    plot_sanity_check.py
    run_point_forecast.py
    run_risk_calibrated.py
    run_moving_average.py
    run_preprocess.py
    run_reactive.py
```

## Current milestone

The first milestone is to build one clean end-to-end data pipeline before touching any advanced model:

1. load the raw Azure trace,
2. derive per-minute application series,
3. split train/validation/test by time,
4. build sliding windows,
5. run a simple reactive or moving-average baseline.

## Dataset note

The Azure dataset is not bundled here. Download it manually from the official Azure Public Dataset page and place the extracted invocation trace under `data/raw/azure2021/`.

Reference:
- https://github.com/Azure/AzurePublicDataset/blob/master/AzureFunctionsInvocationTrace2021.md

## Quick start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the preprocessing pipeline on a local trace file:

```bash
python experiments/run_preprocess.py ^
  --input data/raw/azure2021/invocations.tsv ^
  --output data/processed/azure2021/minute_series.csv ^
  --top-k-apps 10 ^
  --min-invocations 1000 ^
  --capacity-proxy avg
```

Then build sliding windows with `src/data/make_windows.py` for horizons `5, 10, 15`.

Run the first reactive baseline on the processed CSV:

```bash
python experiments/run_reactive.py ^
  --input data/processed/azure2021/minute_series.csv ^
  --summary-out results/reactive_summary.csv ^
  --decisions-out results/reactive_decisions.csv ^
  --split test
```

Run the first predictive baseline with a moving average forecast:

```bash
python experiments/run_moving_average.py ^
  --input data/processed/azure2021/minute_series.csv ^
  --summary-out results/moving_average_summary.csv ^
  --decisions-out results/moving_average_decisions.csv ^
  --split test ^
  --history-window 15 ^
  --horizon 5
```

Run a simple autoregressive point-forecast baseline:

```bash
python experiments/run_point_forecast.py ^
  --input data/processed/azure2021/minute_series.csv ^
  --summary-out results/point_forecast_summary.csv ^
  --decisions-out results/point_forecast_decisions.csv ^
  --split test ^
  --history-window 30 ^
  --horizon 5
```

Run the fixed-quantile scaling baseline:

```bash
python experiments/run_fixed_quantile.py ^
  --input data/processed/azure2021/minute_series.csv ^
  --summary-out results/fixed_quantile_summary.csv ^
  --decisions-out results/fixed_quantile_decisions.csv ^
  --split test ^
  --history-window 30 ^
  --horizon 5 ^
  --quantile 0.95
```

Run the first calibration-aware policy:

```bash
python experiments/run_risk_calibrated.py ^
  --input data/processed/azure2021/minute_series.csv ^
  --summary-out results/risk_calibrated_summary.csv ^
  --decisions-out results/risk_calibrated_decisions.csv ^
  --split test ^
  --history-window 30 ^
  --horizon 5 ^
  --alpha 0.10
```

Generate a sanity-check plot from any decisions CSV:

```bash
python experiments/plot_sanity_check.py ^
  --input results/point_forecast_decisions.csv ^
  --output results/point_forecast_case_study.png ^
  --app APP_ID ^
  --max-points 300
```

Aggregate all baseline decision files into one comparison table:

```bash
python experiments/summarize_results.py ^
  --result-dir results
```

Run burst-only comparison across all saved baselines:

```bash
python experiments/run_burst_analysis.py ^
  --result-dir results ^
  --split test
```

Run a focused sweep for the calibration-aware policy:

```bash
python experiments/run_risk_sweep.py ^
  --input data/processed/azure2021/minute_series.csv ^
  --split test ^
  --alphas 0.10 ^
  --underprovision-weights 6,8 ^
  --oscillation-weights 0.10,0.25 ^
  --output-csv results/risk_sweep.csv
```
