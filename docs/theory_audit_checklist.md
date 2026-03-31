# Theory Audit Checklist for the Autoscaling Paper

This document is the pre-submission theory audit for:

- [paper/calibration_aware_autoscaling_paper.tex](/D:/UMASS%20AMHERST/Study/Sophomore/Research/Self%20Research/autoscaling-for-cloud/paper/calibration_aware_autoscaling_paper.tex)

The goal is not to make the paper look more mathematical. The goal is to make every formal statement necessary, defensible, and aligned with the implemented method.

## Audit Objective

The theory section is acceptable for submission only if all of the following are true:

- every formal statement supports a real claim used later in the paper;
- every assumption is stated at the level actually needed;
- no theorem claims more than the implementation can justify;
- every theory claim is tied to at least one empirical artifact;
- every theorem that remains in the main paper has a proof sketch in the appendix.

## Current Theory Inventory

Current formal objects in the paper:

- `Definition`: autoscaling policy and violation rate
- `Definition`: upper calibration and calibration gap
- `Assumption`: residual transferability within an application
- `Theorem`: quantile rule in the static case
- `Theorem`: calibration transfers directly to SLA control
- `Proposition`: miscalibration produces excess violations
- `Proposition`: burst-guard envelope guarantee
- `Remark`: conditional calibration matters
- `Remark`: role of oscillation penalty
- `Remark`: scope of theoretical claims

## Theorem-by-Theorem Audit

| Item | Current Status | Risk | Keep for Submission? | What must be checked |
| --- | --- | --- | --- | --- |
| Autoscaling policy / violation-rate definition | Strong | Low | Yes | Keep notation consistent with the empirical SLA metric. |
| Upper-calibration definition | Strong | Low | Yes | Keep it population-level; do not blur it with finite-sample conformal validity. |
| Residual-transferability assumption | Necessary but fragile | Medium | Yes | State clearly that this is an app-level deployment assumption, not a proven property of the dataset. |
| Quantile-rule theorem | Strong | Low | Yes | Keep the static-case scope explicit; do not imply it covers the dynamic policy with oscillation. |
| Calibration-to-SLA theorem | Strong if scoped correctly | Medium | Yes | Keep the statement at the level of an `epsilon`-upper-calibrated bound; do not claim a finite-sample guarantee. |
| Miscalibration proposition | Strong | Low | Yes | Keep as a bridge from calibration error to empirical SLA error. |
| Burst-guard proposition | Useful but diagnostic | Medium | Yes, but only as ablation theory | Keep the interpretation narrow: it justifies the guard as a diagnostic envelope, not as the final method. |
| Conditional-calibration remark | Important | Medium | Yes | Make sure app-specific calibration remains an ablation, unless a dedicated experiment upgrades it to a headline result. |

## Required Logic Checks

Run the following checks line by line before submission.

### 1. Claim Lock

For each formal statement, ask:

- Which sentence in the abstract or introduction needs this statement?
- If this statement disappeared, would the paper lose a central claim or only lose decoration?

If the answer is "only decoration", remove or demote it.

### 2. Assumption Hygiene

For each assumption, ask:

- Is this assumption explicitly stated?
- Is it stronger than what the proof actually needs?
- Is it realistic enough for the paper's framing?
- Is it later contradicted by the experiments?

Current high-priority assumption to watch:

- residual transferability across calibration and deployment windows, within an application

### 3. Proof-Scope Discipline

Each theorem must pass this rule:

- the theorem statement must be narrower than or equal to what is proved;
- the prose interpretation may not be stronger than the theorem;
- the implementation may be weaker than the theorem, but never stronger.

In this paper:

- the quantile-rule theorem supports the fixed-quantile baseline interpretation;
- the calibration-to-SLA theorem supports the main conceptual claim;
- neither theorem should be described as a finite-sample guarantee for the implemented residual method.

### 4. Method-Theory Alignment

Check the following alignments explicitly:

- `Theorem: quantile rule` <-> `Fixed-quantile baseline`
- `Theorem: calibration to SLA control` <-> `Residual-calibrated interval + decision rule`
- `Remark: conditional calibration matters` <-> `App-specific calibration ablation`
- `Proposition: burst guard` <-> `Hybrid guard ablation`

If any of these links is missing in Results, either add the missing experiment or weaken the claim.

### 5. Abstract-Safe vs Body-Only Claims

A claim is abstract-safe only if:

- it has direct empirical support in the current draft;
- it is not dependent on a fragile ablation;
- it does not rely on a reviewer accepting a strong unstated assumption.

Current abstract-safe theory-linked claims:

- calibration error affects downstream scaling quality;
- fixed quantiles are interpretable as a simplified decision rule;
- burst-only evaluation reveals failures hidden by aggregate metrics.

Current body-only claims:

- app-specific calibration is preferable in deployment;
- the hybrid guard is a promising extension;
- the decision layer is the main bottleneck under bursts.

These are plausible, but they should stay below the abstract/title level unless the empirical support becomes stronger.

## Language Rules for the Main Paper

Do:

- use "shows", "implies", "suggests", and "motivates" carefully;
- say "population-level argument" when the theorem is not finite-sample;
- say "exploratory ablation" for the hybrid guard.

Do not:

- say "guaranteed" unless the exact conditions are in the theorem;
- say "distribution-free" unless a conformal result is actually implemented;
- say "provably improves" unless there is a theorem comparing policies.

## Appendix Requirements

Before submission, the appendix should contain:

- a clean proof sketch for the quantile-rule theorem;
- a clean proof sketch for the calibration-to-SLA theorem;
- a short note explaining why the burst-guard proposition is diagnostic rather than a full policy theorem;
- one paragraph clarifying the gap between residual calibration and full conformal prediction.

## Submission Gate

Do not submit until all of the following are true:

- no formal statement feels "nice to have" rather than necessary;
- no theorem is cited in prose more strongly than it is proved;
- every theory-backed claim is mapped to at least one table or figure;
- the appendix contains proof sketches for all remaining theorems/propositions;
- the abstract contains only green-light claims from the claim-evidence map.

## Recommended Order

1. Freeze the abstract-level claims.
2. Run this theory audit theorem by theorem.
3. Update the claim-evidence map.
4. Only then shortlist target venues and adapt the paper to page limits.
