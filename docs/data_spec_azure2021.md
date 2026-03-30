# Azure Functions 2021 Data Specification

## 1. Official source

Primary source:
- https://github.com/Azure/AzurePublicDataset/blob/master/AzureFunctionsInvocationTrace2021.md

Azure describes the dataset as a trace of Azure Functions invocations for two weeks starting on 2021-01-31. The documented schema is:

- `app`: encrypted application id
- `func`: encrypted function id, unique within an application
- `end_timestamp`: invocation end timestamp in seconds
- `duration`: invocation duration in seconds

## 2. Why this dataset fits the paper

This project needs a public trace that supports:

- bursty workload behavior,
- short-horizon forecasting,
- a capacity decision proxy,
- reproducible evaluation.

Azure Functions 2021 is a good fit because it gives event-level invocation timing plus duration. That is enough to derive both arrival signals and concurrency-based capacity proxies without requiring private infrastructure logs.

## 3. Research framing

The paper should be framed as `systems + applied ML`, not as a pure forecasting paper and not as a cloud production claim.

Working claim:

> Calibration quality matters for autoscaling decisions under bursty workloads, even when point forecast accuracy alone looks strong.

## 4. Unit of analysis

For the first paper, use:

- scaling entity: `application`
- aggregation level: `1 minute`
- prediction horizons: `5`, `10`, and `15` minutes

Why application-level:

- the dataset explicitly defines applications as the deployment unit,
- application-level aggregation reduces noise from tiny functions,
- it keeps the decision problem close to an autoscaling interpretation.

## 5. Derived timestamps

For each invocation `i`:

- `start_timestamp_i = end_timestamp_i - duration_i`

Because the trace exposes end time and duration, start time can be reconstructed exactly under the dataset's timing model.

## 6. Derived per-minute series

For each application `a` and minute bucket `t`, derive:

### 6.1 Arrival count

`arrivals[a, t]`

- number of invocations whose reconstructed start time falls inside minute `t`

This is useful for sanity checks and workload visualization.

### 6.2 Active service seconds

`active_seconds[a, t]`

- total invocation-seconds overlapping minute `t`

If an invocation spans multiple minutes, distribute its overlap exactly across those buckets.

### 6.3 Average concurrency

`avg_concurrency[a, t] = active_seconds[a, t] / 60`

This is the phase-1 target because it maps directly to capacity and is derivable exactly from the available fields.

### 6.4 Required capacity

`required_capacity[a, t] = ceil(avg_concurrency[a, t] / u_target)`

For the first milestone, set `u_target = 1.0`.

Interpretation:

- one capacity unit can sustain one concurrent invocation on average within the minute,
- this is a controlled research proxy, not a claim about Azure's internal scheduler.

### 6.5 Optional phase-2 refinement

Later, add:

- `peak_concurrency[a, t]`

computed by a sweep-line algorithm over invocation start and end events. That refinement is useful if the first baseline results suggest the average-concurrency proxy is too smooth.

## 7. Forecasting task

Primary target for milestone 1:

- forecast `required_capacity[a, t + h]` for `h in {5, 10, 15}`

Auxiliary target:

- forecast `arrivals[a, t + h]` for plotting and interpretability checks

Recommended history window:

- `60` minutes of past context

## 8. Candidate app filtering

Do not use every app at first. Filter to active apps only.

Starter rule:

- keep the top `K` applications by total invocation count,
- require at least `1000` invocations in the extracted window.

This avoids wasting time on mostly idle traces that make forecasting and scaling look artificially easy.

## 9. Data split

Split strictly by time, never randomly.

Starter split:

- train: first 70 percent of minutes
- validation: next 15 percent
- test: last 15 percent

All windows must respect chronology.

## 10. Scaling evaluation proxies

For a predicted capacity `c_t` and required capacity `r_t`:

- cost: `c_t`
- underprovision amount: `max(r_t - c_t, 0)`
- SLA violation indicator: `1[r_t > c_t]`
- oscillation: `abs(c_t - c_{t-1})`

These are the first paper's operational metrics. They are clear, reproducible, and directly tied to the decision objective.

## 11. Baselines to support first

Implement in this order:

1. reactive scaling from current observed demand
2. moving-average forecast baseline
3. point-forecast baseline
4. fixed-quantile scaling baseline
5. calibration-aware risk-sensitive policy

Do not add reinforcement learning in the first paper.

## 12. First success criterion

Before any advanced method, the repo should be able to:

1. load one raw trace file,
2. produce one clean minute-level CSV,
3. build train/validation/test windows,
4. run one simple baseline,
5. save one sanity-check plot.
