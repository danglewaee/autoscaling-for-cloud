# IC2E 2026 Short-Paper Solo Sprint

Date of planning: **April 7, 2026**

Primary venue:

- IC2E 2026 CFP:
  <https://conferences.computer.org/IC2E/2026/cfp-main.html>

Primary target:

- `IC2E 2026 short paper`

Official constraints confirmed from the CFP:

- abstract due **April 17, 2026**
- full and short paper due **April 24, 2026**
- short papers are limited to **5 review pages**, excluding references
- submission is **single-blind**
- short papers must be **clearly marked as such in the title**
- AI-generated text, figures, images, or code must be **disclosed in the acknowledgments section**

Primary paper files:

- long draft:
  [paper/calibration_aware_autoscaling_paper.tex](/D:/UMASS%20AMHERST/Study/Sophomore/Research/Self%20Research/autoscaling-for-cloud/paper/calibration_aware_autoscaling_paper.tex)
- short-paper working copy:
  [paper/calibration_aware_autoscaling_ic2e_short.tex](/D:/UMASS%20AMHERST/Study/Sophomore/Research/Self%20Research/autoscaling-for-cloud/paper/calibration_aware_autoscaling_ic2e_short.tex)

## Core Rule for the Next 17 Days

This is now a `submission sprint`, not an open research phase.

That means:

- no new datasets
- no new major methods
- no venue switching unless the paper misses an internal gate
- no writing that does not improve the IC2E submission directly

The paper does **not** need to become a final systems paper in 17 days.
It only needs to become:

- coherent,
- honest,
- properly formatted,
- and strong enough for a short cloud-engineering submission.

## Solo Strategy

Because the paper has only one author, the sprint must reduce context switching.

Use this rule:

- each day has one primary objective
- each objective ends in a concrete artifact
- no day is allowed to end with only vague progress

This is what makes a solo sprint realistic.

## Internal Gates

### Gate 1: April 10

By the end of **April 10, 2026**, the short-paper draft must:

- have the final central claim
- have the final result selection
- have no extra ablations in the main text
- have a bibliography that no longer looks thin

If this gate fails badly, start preparing a Middleware fallback in parallel.

### Gate 2: April 14

By the end of **April 14, 2026**, the short-paper draft must:

- be in the venue template
- be close enough to the page budget that final trimming feels realistic
- have all final figures and tables selected

If this gate fails, do not keep polishing blindly. Re-scope harder.

### Gate 3: April 20

By the end of **April 20, 2026**, the draft must:

- read like a submission, not a working note
- have final title, author block, and acknowledgments plan
- be ready for final formatting and EasyChair submission work

If this gate fails, submission risk is high.

## Day-by-Day Sprint

### April 7, 2026

Objective:

- lock the solo sprint and freeze the claim set

Deliverables:

- this sprint document
- a one-paragraph submission pitch
- a final answer to: "what is the paper actually claiming?"

Definition of done:

- the short-paper story is frozen around:
  calibration matters for scaling decisions,
  burst-only evaluation reveals hidden failures,
  and the current method is competitive on aggregate metrics but incomplete on bursts

### April 8, 2026

Objective:

- expand the bibliography and strengthen Related Work

Deliverables:

- at least `4-6` additional references
- tighter systems positioning
- tighter calibration positioning

Definition of done:

- the paper no longer looks under-cited for a conference short paper

### April 9, 2026

Objective:

- tighten the short-paper narrative

Deliverables:

- one clean opening motivation
- one theorem-level insight
- one method description
- one aggregate table
- one burst table
- one figure

Definition of done:

- if a section or result does not support that spine, it is removed from the short version

### April 10, 2026

Objective:

- pass `Gate 1`

Deliverables:

- a clean redline of what stays and what is cut
- a short-paper draft with no major structural uncertainty left

Definition of done:

- no more open debate about method scope or result scope

### April 11, 2026

Objective:

- move the short paper into IEEE-style formatting

Deliverables:

- venue-aligned LaTeX structure
- title marked as short paper
- placeholder acknowledgments section for disclosure language

Definition of done:

- the paper visually starts resembling the submission artifact

### April 12, 2026

Objective:

- first hard compression pass

Deliverables:

- one shorter draft after aggressive trimming
- notes on what still causes page pressure

Definition of done:

- every paragraph justifies its existence

### April 13, 2026

Objective:

- reviewer-style content pass

Review questions:

- is the contribution clear in the first page?
- is the theory proportionate to a short paper?
- do the results support the headline claim?
- does the paper sound honest rather than defensive?

Deliverables:

- reviewer notes
- a list of required fixes, ranked by severity

### April 14, 2026

Objective:

- pass `Gate 2`

Deliverables:

- stable figure/table set
- stable section order
- stable page-budget estimate

Definition of done:

- no more structural changes after this date unless something is clearly broken

### April 15, 2026

Objective:

- submission metadata pass

Deliverables:

- final author name and affiliation
- final title
- acknowledgments text draft
- AI-disclosure wording draft if needed

Important note:

- because the CFP explicitly requires disclosure for AI-generated text, figures, images, or code, this must be handled deliberately rather than left to the last day

### April 16, 2026

Objective:

- abstract-submission readiness

Deliverables:

- final abstract text
- keywords / metadata notes
- EasyChair-ready author list

Definition of done:

- the abstract can be submitted on the next day without more writing

### April 17, 2026

Objective:

- submit the abstract

Deliverables:

- abstract submitted
- submission record saved
- any EasyChair issues resolved immediately

### April 18, 2026

Objective:

- final technical polish pass

Deliverables:

- cleaned equations
- cleaned captions
- cleaned theorem wording
- cleaned transitions

### April 19, 2026

Objective:

- final language-compression pass

Deliverables:

- shorter prose
- stronger topic sentences
- fewer repeated claims

Definition of done:

- the paper reads tight, not padded

### April 20, 2026

Objective:

- pass `Gate 3`

Deliverables:

- near-final submission PDF
- final list of blockers, ideally empty or very small

### April 21, 2026

Objective:

- final formatting and references pass

Deliverables:

- bibliography cleaned
- citation formatting checked
- page overflows and ugly spacing fixed

### April 22, 2026

Objective:

- submission simulation

Deliverables:

- pretend-submit checklist completed
- final file naming and packaging checked
- final PDF sanity checked one more time

Definition of done:

- if EasyChair opened right now, the paper could be uploaded without panic

### April 23, 2026

Objective:

- buffer day

Use only for:

- unavoidable fixes
- formatting surprises
- metadata corrections
- disclosure wording corrections

Do not use this day to reopen the research story.

### April 24, 2026

Objective:

- submit the short paper

Deliverables:

- full short paper submitted
- confirmation saved
- post-submission notes recorded for later revision

## What Not To Do

Do not spend the next 17 days on:

- new baselines unless a reviewer would obviously demand them
- another capacity proxy
- another dataset
- another theoretical proposition
- a full-paper rewrite
- polishing the long draft instead of the submission draft

## Immediate Next Task

The first high-value task after this sprint file is:

- **expand the bibliography and strengthen Related Work on April 8**

Reason:

- it improves credibility quickly
- it is low risk
- and it prepares the short paper for the template/compression pass that follows

## Bottom-Line Rule

For a solo first-author submission, success comes from:

- freezing the story early,
- cutting aggressively,
- and shipping on time.

The paper is already past the "idea" stage.
The remaining work is not to invent a new paper.
The remaining work is to finish this one.
