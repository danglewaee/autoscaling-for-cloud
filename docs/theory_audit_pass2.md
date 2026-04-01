# Theory Audit Pass 2

This document records the second theory-focused prose audit of the current draft:

- [paper/calibration_aware_autoscaling_paper.tex](/D:/UMASS%20AMHERST/Study/Sophomore/Research/Self%20Research/autoscaling-for-cloud/paper/calibration_aware_autoscaling_paper.tex)

It follows:

- [theory_audit_pass1.md](/D:/UMASS%20AMHERST/Study/Sophomore/Research/Self%20Research/autoscaling-for-cloud/docs/theory_audit_pass1.md)
- [claim_evidence_map.md](/D:/UMASS%20AMHERST/Study/Sophomore/Research/Self%20Research/autoscaling-for-cloud/docs/claim_evidence_map.md)

## Scope

Pass 2 is intentionally narrow. It audits only the headline prose in:

- the abstract,
- the introduction,
- the conclusion,

with one supporting wording change in `Related Work` to keep the narrative consistent.

The purpose is not to add new theory. The purpose is to ensure that top-level selling points depend only on claims that are already theory-clean and empirically supported.

## Executive Verdict

After this pass, the paper's headline narrative is materially safer for submission.

Main conclusion of Pass 2:

- the abstract can remain essentially unchanged;
- the introduction needed one structural softening and one claim downgrade;
- the conclusion needed one headline claim downgraded from a `yellow` interpretation to a `green` empirical statement;
- the paper should now sell itself primarily through calibration-sensitive decision making and burst-only evaluation, not through stronger statements about app-specific calibration or the decision layer.

## Sentence-Level Decisions

### 1. Abstract

- Verdict: `KEEP`
- Reason:
  The abstract already relies on `green` claims:
  calibration matters, predictive methods improve aggregate SLA relative to reactive scaling, and burst-only windows remain difficult.
- Action:
  No wording change required in this pass.

### 2. Introduction: thesis paragraph

- Previous issue:
  The old thesis sentence read too much like a direct success claim:
  calibration-aware autoscaling "can reduce SLA violations and improve the cost-reliability trade-off".
- Risk:
  Medium. That wording was stronger than what the current empirical section cleanly supports at headline level.
- Change made:
  Replaced `\paragraph{Thesis.}` with `\paragraph{Central claim.}` and rewrote the sentence to frame the paper as testing whether uncertainty quality changes the cost-reliability trade-off.
- Verdict:
  `FIXED`

### 3. Introduction: contributions paragraph

- Previous issue:
  The old contribution text said burst-only evaluation "reveals a decision-layer failure mode".
- Risk:
  Medium, because this leans on claim `C6`, which is still `yellow`.
- Change made:
  Replaced that phrase with a weaker and cleaner statement:
  burst-only evaluation reveals a harder failure regime than average metrics suggest.
- Verdict:
  `FIXED`

### 4. Related Work: hybrid-guard motivation sentence

- Previous issue:
  The old sentence said the main unresolved difficulty lies in the decision layer.
- Risk:
  Medium. This was a stronger interpretation than needed in a framing paragraph.
- Change made:
  Softened it to:
  part of the remaining difficulty may lie in the downstream decision rule.
- Verdict:
  `FIXED`

### 5. Conclusion

- Previous issue:
  The old conclusion stated that burst-only evaluation reveals that the main remaining bottleneck lies in the decision layer.
- Risk:
  Medium-to-high for a conclusion sentence, because it turned a diagnostic interpretation into a headline claim.
- Change made:
  Replaced it with a `green` empirical statement:
  burst-only evaluation shows that average metrics understate the difficulty of rare demand spikes.
- Verdict:
  `FIXED`

## Headline Claim Status After Pass 2

### Safe to emphasize

- calibration quality affects downstream scaling quality;
- fixed-quantile scaling has a clean decision-theoretic interpretation;
- burst-only evaluation exposes failures hidden by aggregate metrics;
- the current calibration-aware policy is competitive on aggregate metrics but still incomplete on bursts.

### Keep below headline level

- app-specific calibration matters in deployment;
- part of the remaining difficulty may lie in the decision layer;
- the hybrid guard is diagnostically useful but not yet the final policy.

### Still forbidden

- exact finite-sample guarantee for the implemented residual method;
- distribution-free guarantee for the deployed policy;
- claim that the method clearly dominates point forecasting across all important metrics;
- claim that the hybrid guard is already the final proposed method.

## Submission Guidance After Pass 2

If the paper were submitted soon, the headline pitch should now stay close to:

- calibration matters for autoscaling decisions;
- fixed quantiles are interpretable but insufficient;
- burst-only evaluation reveals the real failure regime;
- the current method is competitive on average but still incomplete under bursts.

That pitch is narrower than a full systems paper with a final production policy, but it is much safer and more coherent for a first submission.
