# Theory Audit Pass 1

This document records the first manual theory audit of the current draft:

- [paper/calibration_aware_autoscaling_paper.tex](/D:/UMASS%20AMHERST/Study/Sophomore/Research/Self%20Research/autoscaling-for-cloud/paper/calibration_aware_autoscaling_paper.tex)

It should be read together with:

- [theory_audit_checklist.md](/D:/UMASS%20AMHERST/Study/Sophomore/Research/Self%20Research/autoscaling-for-cloud/docs/theory_audit_checklist.md)
- [claim_evidence_map.md](/D:/UMASS%20AMHERST/Study/Sophomore/Research/Self%20Research/autoscaling-for-cloud/docs/claim_evidence_map.md)

## Executive Verdict

The theory section is now structurally sound enough for a serious draft. It is no longer in the "proposal" stage. However, the paper is not yet theory-clean enough for submission without a final tightening pass on headline claims.

Main conclusion of Pass 1:

- keep all current formal statements;
- do not upgrade any current remark/proposition into a stronger theorem;
- weaken a few prose claims in the abstract and introduction so they match the current evidence exactly;
- keep the strongest claims centered on calibration, fixed-quantile interpretation, and burst-only evaluation.

## Formal Statement Verdicts

### 1. Definition: Autoscaling policy and violation rate

- Verdict: `KEEP`
- Reason:
  This is foundational notation, directly connected to the empirical SLA violation metric.
- Risk:
  Low.
- Action:
  None.

### 2. Definition: Upper calibration and calibration gap

- Verdict: `KEEP`
- Reason:
  It is necessary for the calibration-to-SLA theorem and for the calibration metrics section.
- Risk:
  Low, as long as it remains explicitly population-level.
- Action:
  Keep wording as is.

### 3. Assumption: Residual transferability within an application

- Verdict: `KEEP, BUT FLAG AS FRAGILE`
- Reason:
  The implemented residual method needs this assumption to connect calibration-split residuals to deployment-time behavior.
- Risk:
  Medium. Reviewers may ask whether this assumption is realistic under non-stationary bursts.
- Action:
  Keep it explicit. Do not hide it in prose. If challenged later, defend it as a modeling assumption for a first public trace study, not as an empirical law.

### 4. Theorem: Quantile rule in the static case

- Verdict: `KEEP`
- Reason:
  This is one of the cleanest statements in the paper. It justifies the fixed-quantile baseline theoretically and is narrower than the dynamic deployed method.
- Risk:
  Low.
- What must not be said:
  Do not describe this theorem as if it proves the optimality of the dynamic policy with oscillation.
- Action:
  None.

### 5. Theorem: Calibration transfers directly to SLA control

- Verdict: `KEEP`
- Reason:
  This is the core theorem that links the paper's calibration story to downstream decisions.
- Risk:
  Medium, because the implementation is residual-based rather than fully conformalized.
- What must not be said:
  Do not say the deployed residual method has an exact finite-sample coverage guarantee.
- Action:
  Keep the theorem exactly at the `epsilon`-upper-calibrated level and keep the scope remark in the main paper.

### 6. Proposition: Miscalibration produces excess violations

- Verdict: `KEEP`
- Reason:
  Although simple, it cleanly connects calibration error to the empirical SLA metric and reinforces the paper's main claim.
- Risk:
  Low.
- Action:
  None.

### 7. Remark: Conditional calibration matters

- Verdict: `KEEP, BUT BODY-ONLY`
- Reason:
  This remark is conceptually correct and aligns with per-application deployment.
- Risk:
  Medium-to-high, because app-specific calibration is not yet a full headline result in the experiments.
- What must not be said:
  Do not elevate app-specific calibration into the abstract unless a dedicated ablation is added.
- Action:
  Keep in theory and body discussion only.

### 8. Proposition: Burst-guard envelope guarantee

- Verdict: `KEEP, BUT ONLY AS ABLATION THEORY`
- Reason:
  It explains why the hybrid guard can help once a burst is partially revealed.
- Risk:
  Medium. It is easy to overread as a theorem for the final method.
- What must not be said:
  Do not present the hybrid guard as the paper's final proposed policy.
- Action:
  Keep the proposition, but always pair it with "exploratory" or "diagnostic ablation" language.

### 9. Remark: Role of the oscillation penalty

- Verdict: `KEEP`
- Reason:
  It is small but useful. It clarifies why the dynamic policy is not reducible to a static quantile rule.
- Risk:
  Low.
- Action:
  None.

### 10. Remark: Scope of the theoretical claims

- Verdict: `KEEP`
- Reason:
  This is a protective remark. It prevents overclaim and will help in review.
- Risk:
  Low.
- Action:
  None.

## Abstract and Introduction Audit

### Claims that are already safe

These should remain the backbone of the abstract and introduction:

- forecast accuracy alone is not enough for robust autoscaling;
- calibration quality matters for downstream scaling decisions;
- fixed quantiles are interpretable but insufficient;
- burst-only evaluation reveals a harder failure regime than aggregate metrics suggest.

### Claims that should stay below headline level

- app-specific calibration matters in deployment;
- the decision layer is the main bottleneck;
- the hybrid guard points to a promising next policy.

These are plausible, but right now they are better treated as body-level conclusions rather than title/abstract-level selling points.

### Suggested wording discipline

Prefer:

- "the results suggest"
- "the evidence indicates"
- "the current implementation shows"
- "the ablation supports the interpretation that"

Avoid:

- "the method guarantees"
- "the policy is provably robust"
- "the proposed method clearly outperforms point forecasting"

## Immediate Paper Edits Suggested by Pass 1

### Edit Group A: Abstract

Current abstract is mostly acceptable. Keep it, but preserve the current soft phrasing:

- "In the current implementation..."
- "clarifies where calibration-aware decisions must improve further"

Do not rewrite it into stronger victory language yet.

### Edit Group B: Introduction

The introduction is already aligned with the green claims. It does not need structural change.

One thing to watch:

- if later drafts add stronger language about app-specific calibration or the hybrid guard, keep those additions out of the introduction unless new dedicated evidence is added.

### Edit Group C: Results interpretation

Results should continue to distinguish clearly between:

- main method results,
- diagnostic ablations,
- negative-result ablations.

Recommended mapping:

- main result: aggregate + burst tables
- diagnostic ablation: hybrid guard
- negative-result ablation: peak proxy

## What Pass 1 Says About Submission Readiness

The theory section itself is no longer the blocker.

Current blockers before submission are:

- final headline-claim tightening;
- one more proofreading pass to ensure no sentence overstates a yellow claim;
- venue fit and page-limit fit;
- PDF build and formatting pass.

## Pass 2 Recommendation

The next theory pass should be narrower:

1. read only the abstract, introduction, and conclusion;
2. mark any sentence that depends on a yellow claim;
3. weaken or move those sentences into the body if needed;
4. confirm that the abstract uses only green-light claims from the claim-evidence map.

That pass should be much shorter than Pass 1 and should happen immediately before venue selection.
