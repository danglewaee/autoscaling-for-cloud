# Claim-Evidence Map for the Autoscaling Paper

This document maps each major claim in the current draft to:

- its theory support,
- its empirical support,
- its current reviewer risk,
- and whether it is safe for the abstract or only for the body.

Primary paper:

- [paper/calibration_aware_autoscaling_paper.tex](/D:/UMASS%20AMHERST/Study/Sophomore/Research/Self%20Research/autoscaling-for-cloud/paper/calibration_aware_autoscaling_paper.tex)

## Claim Table

| ID | Claim | Theory Support | Empirical Support | Current Strength | Abstract-Safe? | Reviewer Risk | Action Before Submission |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | Forecast accuracy alone is not enough; calibration quality affects downstream scaling quality. | `Theorem thm:calibration-to-sla`, `Proposition prop:miscalibration` | calibration metrics subsection, aggregate comparison, burst comparison | Medium-to-strong | Yes | Medium | Keep wording careful; avoid claiming causal proof beyond the decision argument. |
| C2 | Fixed-quantile scaling is a simplified decision rule, not an arbitrary heuristic. | `Theorem thm:quantile-rule` | fixed-quantile baseline in aggregate and burst tables | Strong | Yes | Low | Keep theorem scope static; do not describe it as the deployed policy. |
| C3 | Burst-only evaluation reveals failures hidden by aggregate metrics. | no single theorem needed; supported by overall decision framing | `tab:burst-results`, `fig:burst-case-study`, comparison against aggregate table | Strong | Yes | Low | Keep this as a central narrative claim. |
| C4 | The current calibration-aware policy is competitive on aggregate metrics but still weak on bursts. | theory gives motivation, not dominance | `tab:aggregate-results`, `tab:burst-results` | Strong | Yes | Low | Keep language empirical and direct. |
| C5 | Conditional or app-specific calibration matters because decisions are made per app. | `Remark` on conditional calibration | app-specific calibration only appears indirectly via hybrid-guard variant | Medium | No | Medium-to-high | Add a dedicated app-specific calibration ablation if you want this claim to move above body-level. |
| C6 | The main unresolved bottleneck under bursts lies in the decision layer. | `Proposition prop:burst-guard` motivates why a guard can help after partial burst revelation | `tab:hybrid-guard`, `fig:burst-case-study` | Medium | No | Medium | Keep as "evidence suggests", not "paper proves". |
| C7 | The hybrid guard improves burst-only SLA but at the cost of instability. | `Proposition prop:burst-guard` | `tab:hybrid-guard` | Strong | No | Low | Safe as an ablation claim; do not market it as the final method. |
| C8 | Peak concurrency is a harsher target and does not help the current policy. | no theorem required | `tab:proxy-ablation` | Strong | No | Low | Keep as an ablation/negative-result claim. |

## Green / Yellow / Red Summary

### Green: Safe to emphasize

- C1: calibration quality affects downstream scaling quality
- C2: fixed quantiles have a clean decision-theoretic interpretation
- C3: burst-only evaluation reveals hidden failures
- C4: the current method is reasonable on aggregate metrics but still weak on bursts
- C7: the hybrid guard improves burst SLA while increasing instability
- C8: peak proxy is a negative-result ablation

### Yellow: Keep, but below headline level

- C5: app-specific calibration matters
- C6: the decision layer is the main bottleneck

These are plausible and supported, but they are not yet as cleanly defended as the green claims.

### Red: Do not claim in the current version

- any finite-sample coverage guarantee for the implemented residual method
- any distribution-free guarantee for the deployed policy
- any claim that the hybrid guard is already the final policy
- any claim that the method clearly dominates point-forecast scaling in all important metrics

## Claim-to-Artifact Mapping

### Abstract / Introduction should rely on

- `thm:calibration-to-sla`
- `thm:quantile-rule`
- `tab:aggregate-results`
- `tab:burst-results`
- `fig:burst-case-study`

### Results section should rely on

- `tab:aggregate-results`
- `tab:burst-results`
- `tab:hybrid-guard`
- `tab:proxy-ablation`
- `fig:burst-case-study`

### Appendix should support

- proof sketch for `thm:quantile-rule`
- proof sketch for `thm:calibration-to-sla`
- implementation mapping from code to method

## Submission Use

Before choosing a venue, use this table to do three cuts:

1. Remove any abstract sentence that depends on a yellow or red claim.
2. Keep all green claims, but ensure each one points to a concrete table or figure.
3. If a yellow claim is important for the venue pitch, add one more experiment before submission.

## Current Recommendation

If the paper were submitted soon, the cleanest pitch would be:

- calibration matters for autoscaling decisions,
- fixed quantiles are interpretable but insufficient,
- burst-only evaluation exposes the real failure regime,
- the current method is competitive on average but still incomplete on bursts.

That pitch is coherent, honest, and supported by the current draft.
