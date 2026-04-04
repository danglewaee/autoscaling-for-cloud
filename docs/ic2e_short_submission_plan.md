# IC2E 2026 Short-Paper Submission Plan

Date of planning: **April 4, 2026**

Primary paper:

- [paper/calibration_aware_autoscaling_paper.tex](/D:/UMASS%20AMHERST/Study/Sophomore/Research/Self%20Research/autoscaling-for-cloud/paper/calibration_aware_autoscaling_paper.tex)

Primary venue:

- IC2E 2026 main CFP:
  <https://conferences.computer.org/IC2E/2026/cfp-main.html>
- IC2E 2026 homepage:
  <https://conferences.computer.org/IC2E/2026/index.html>

## Decision

The most feasible route to a **first publication** for the current paper is:

- **IC2E 2026 short paper**

This is the best choice as of **April 4, 2026**.

## Why IC2E Short Is the Best Fit

### 1. The paper is already good enough for a short cloud-engineering paper

The draft already has:

- a public dataset,
- a working codebase,
- a clear systems problem,
- a formal decision framing,
- an empirical story with aggregate and burst-only results,
- and a claim set that has already been tightened by theory audit.

That is enough for a short paper. It is not yet strong enough for a confident full-paper push at a harder venue.

### 2. The venue scope fits the topic directly

IC2E explicitly solicits work on cloud engineering, resource management, and serverless/cloud systems. This paper sits comfortably inside that space.

### 3. The paper's current shape matches a short-paper contribution

Right now the strongest part of the paper is:

- the framing of calibration-aware autoscaling,
- the theory-to-decision connection,
- and the burst-only evaluation story.

That is exactly the kind of contribution that can work as a short paper. The current method is still informative, but it is not yet a clear full-paper "final controller" story.

### 4. The deadline is close but still realistic

As of **April 4, 2026**, the official IC2E 2026 deadlines are:

- abstract: **April 17, 2026**
- paper: **April 24, 2026**

That is close enough to create urgency, but still realistic if the scope is kept tight.

## Why the Other Options Are Less Feasible Right Now

### SoCC 2026

SoCC is the best topical match, but it is not the most feasible first submission.

Reason:

- the paper still looks stronger as a framing-and-analysis paper than as a fully mature systems method paper;
- SoCC will be harsher on method maturity;
- the reserve-reviewer policy adds process overhead if a senior author is involved.

SoCC should be treated as a stretch target, not the default target.

### Middleware 2026

Middleware is a very good backup if IC2E slips. It gives more time and has a strong fit for a systems-plus-method paper.

But for a first acceptance in 2026, IC2E short is still the cleaner and faster route.

## Current Readiness Estimate

For `IC2E 2026 short paper`, the current draft is roughly:

- **70-75% ready**

That means:

- the paper is real and can be shaped into a submission;
- but it still needs a venue-specific tightening pass.

## Main Risks Before Submission

### 1. The method story is not dominant enough

The current paper is strongest when it argues:

- calibration matters for downstream scaling;
- burst-only evaluation reveals hidden failures;
- aggregate metrics alone are not enough.

It is weaker if it tries to argue:

- the current controller clearly wins overall;
- the final policy is already solved.

So the short-paper version must keep the narrative narrow.

### 2. The bibliography is still too thin

The paper currently has only a small reference list. That is acceptable for an internal draft, but weak for submission.

### 3. The paper has not yet been cut to IC2E format

IC2E short papers allow:

- **5 review pages plus references**

So the current draft must be compressed aggressively.

### 4. The PDF has not yet been built and visually checked

Until the paper is rendered in the actual venue template, we do not know:

- the true page count,
- float placement,
- figure/table balance,
- or whether the paper visually reads like a short conference paper.

## Exact Submission Constraints to Respect

From the official IC2E 2026 CFP:

- short papers are limited to **5 review pages plus references**
- submissions are **single-blind**
- short papers must be **clearly marked as such in the title**
- accepted papers are published by IEEE CPS

This affects how we prepare the draft:

- we do **not** need anonymization for IC2E;
- we **do** need to keep the title and paper type explicit;
- we **must** plan around a much shorter page budget than the current draft.

## What the IC2E Short Version Should Emphasize

The IC2E short submission should emphasize only four things:

1. autoscaling is a decision problem under uncertainty
2. calibration quality matters for downstream scaling quality
3. burst-only evaluation reveals failures hidden by aggregate metrics
4. the Azure trace study is a reproducible public benchmark case for this question

Everything else is secondary.

In particular:

- the hybrid guard should stay as a short ablation, not as the paper's main claim
- the peak-proxy result should stay a compact negative-result ablation
- app-specific calibration should stay below headline level

## What Should Be Cut or Compressed

To fit 5 pages, the IC2E short version should compress:

- `Related Work`
- theorem statements and proof exposition
- appendix-style implementation mapping
- long limitations/future-work prose

The short paper should keep:

- one clean theorem-level insight in the main text
- one core method description
- one aggregate table
- one burst table
- one figure or one ablation table, but not too many extras

## Proposed Page Budget

This is the practical target:

1. `Introduction + motivation`: about 0.8 pages
2. `Problem + one theorem-level idea + method`: about 1.2 pages
3. `Experimental setup`: about 0.5 pages
4. `Core results`: about 1.8 pages
5. `Conclusion`: about 0.2 pages
6. `References`: unlimited beyond the review-page cap

That means the current full draft should **not** be edited incrementally into shape. It should be **cut down deliberately** into a short-paper version.

## Concrete Plan From April 4 to April 24, 2026

### By April 6

- lock the venue as `IC2E 2026 short paper`
- freeze the central claim
- decide the exact short-paper title

### By April 8

- move the paper into the IEEE conference template
- create a short-paper branch or a separate short-paper file
- cut the story to one theorem-level idea and one main experimental narrative

### By April 10

- reduce the result section to the strongest artifacts only
- expand the bibliography to a respectable systems-plus-calibration baseline
- remove any prose that sounds like an unfinished full-paper promise

### By April 13

- do a reviewer-style pass:
  novelty, clarity, threat model, experimental honesty, scope fit

### By April 15

- finalize figures and tables
- check single-blind metadata, author list, affiliations, acknowledgements, and disclosure wording

### By April 17

- submit the abstract

### By April 18-23

- final polish
- PDF sanity check
- title and formatting pass

### By April 24

- submit the full short paper

## Fallback Plan

If by **April 10-12** the short-paper version still looks too unstable, switch immediately to:

- `Middleware 2026 Big Ideas`

Do not force a weak IC2E submission just because the deadline is near.

## Bottom-Line Recommendation

If the goal is a **realistic first publication**, the correct move is:

- target **IC2E 2026 short paper first**
- treat `Middleware 2026 Big Ideas` as backup
- treat `SoCC 2026` as stretch, not default

That is the highest-probability path from the current draft to an actual first accepted paper.
