# Venue Shortlist and First-Publication Strategy

As of **April 1, 2026**, this paper is no longer just an idea. It has:

- a concrete public dataset,
- a reproducible codebase,
- formal problem framing,
- first-round empirical results,
- and a narrowed claim set after theory audit.

That is enough to start planning submission seriously. It is **not** yet a paper that should be sent blindly to the hardest full-paper venue available.

The right strategy for a first publication is to optimize for:

- scope fit,
- submission realism,
- and probability of producing an archival acceptance in 2026.

## What Counts as a Good Target for This Paper

For the current draft, the best venue types are:

- `short research paper` or `vision/big-ideas paper` at a cloud/systems venue,
- or, if the paper is still not stable enough, an `archival poster/demo paper` as a safety net.

For the current draft, I do **not** recommend aiming first for:

- a top-tier full systems paper with a broad implementation claim,
- or a venue that expects a production-quality controller rather than a focused public-trace study.

## Shortlist

### 1. IC2E 2026: Best first-shot target if you want the highest probability of an acceptance in 2026

- Venue:
  IEEE International Conference on Cloud Engineering 2026
- Official site:
  <https://conferences.computer.org/IC2E/2026/index.html>
- Location and dates:
  Santa Clara, California, USA, **October 13-16, 2026**
- Submission window:
  abstract due **April 17, 2026**
  paper due **April 24, 2026**
- Paper formats:
  `full` up to 9 review pages plus references
  `short` up to 5 review pages plus references
- Review model:
  `single-blind`
- Publication:
  accepted papers are published by IEEE Computer Society CPS and the CFP says they are EI indexed
- Why it fits:
  the CFP explicitly welcomes cloud management and engineering, serverless computing, and resource management
- Why it is realistic:
  this is the cleanest near-term target for a first publication because the topic fit is strong and the paper can be scoped down to a short paper without pretending to be a fully mature production system
- What I would submit here:
  `short paper` first
- How to frame it:
  "calibration-aware autoscaling as a decision-sensitive cloud engineering problem on a public serverless trace"

### 2. Middleware 2026: Best middle-ground target if you want a stronger systems venue without forcing a full final-method claim

- Venue:
  ACM/IFIP International Middleware Conference 2026
- Official site:
  <https://middleware-conf.github.io/2026/>
- Research CFP:
  <https://middleware-conf.github.io/2026/calls/call-for-research-papers/>
- Location and dates:
  Tarragona, Spain, **December 14-18, 2026**
- Submission window, second cycle:
  abstract due **May 29, 2026**
  paper due **June 5, 2026**
- Paper formats:
  `research` or `experimentation and deployment` up to 12 pages of technical content
  `big ideas` up to 6 pages of technical content
- Review model:
  `double-anonymous`
- Publication:
  accepted papers appear in the ACM Digital Library
- Why it fits:
  the CFP covers serverless, cloud and data-center systems, monitoring, and resource management, which matches the paper's autoscaling setting well
- Why it is attractive:
  Middleware has a cleaner path for a paper that mixes formal framing with a focused empirical study, and its revision model is helpful for a first serious submission
- What I would submit here:
  `Big Ideas` if the main value is the formulation plus burst-only evaluation narrative
  `Research` only if the empirical section becomes noticeably tighter before late May
- How to frame it:
  "calibration-aware autoscaling as a middleware decision problem, with burst-only evaluation exposing hidden failure regimes"

### 3. SoCC 2026: Best topical fit, but also the most ambitious target on this list

- Venue:
  ACM Symposium on Cloud Computing 2026
- Official site:
  <https://acmsocc.org/2026/>
- CFP:
  <https://acmsocc.org/2026/papers.html>
- Location and dates:
  Singapore, **November 18-20, 2026**
- Remaining submission window:
  abstract due **July 7, 2026**
  paper due **July 14, 2026**
- Paper formats:
  `full research` 12 pages plus unlimited references
  `short research` 6 pages plus unlimited references
  `vision` 6 pages plus unlimited references
- Review model:
  `dual-anonymous`
- Publication:
  accepted papers appear in the ACM Digital Library
- Extra submission note:
  SoCC 2026 has a `reserve reviewer` policy for senior authors, with exemptions listed in the CFP
- Why it fits:
  the CFP explicitly lists serverless, microservices, and resource management / provisioning / scheduling
- Why it is harder:
  SoCC is the strongest topical match here, but it is also the venue most likely to punish a paper whose final method story is still incomplete on bursts
- What I would submit here:
  `short research` or `vision`, not a full paper, unless the next round of experiments becomes substantially stronger
- How to frame it:
  either as a crisp short empirical paper on calibration-aware scaling under bursty serverless traces,
  or as a vision-style argument that calibration should be treated as a first-class systems objective

### 4. IC2E 2026 Poster/Demo: Safety net if the full paper is not clean enough by late April or early June

- Official CFP:
  <https://conferences.computer.org/IC2E/2026/cfp-demos-posters.html>
- Submission deadline:
  **June 29, 2026**
- Format:
  2 double-column pages
- Review model:
  `single-blind`
- Publication:
  accepted poster/demo papers are published by IEEE CPS, and the CFP states they are indexed by EI
- Why it matters:
  if the main paper is still unstable, this is still a real archival publication route and a good way to get public feedback without forcing the paper into a full-track submission too early

## Recommendation

### If your goal is the highest probability of a first accepted publication in 2026

Use this order:

1. `IC2E 2026 short paper`
2. `Middleware 2026 Big Ideas`
3. `SoCC 2026 short research or vision`
4. `IC2E 2026 poster/demo` as a safety net

This path is the most pragmatic.

### If your goal is the strongest topical venue and you are willing to take more risk

Use this order:

1. `SoCC 2026 short research or vision`
2. `Middleware 2026 Big Ideas or Research`
3. `IC2E 2026 short paper`

This path gives you the best cloud-systems fit, but not the highest probability of a first acceptance.

## My Actual Recommendation for This Paper

For the current draft, I recommend:

1. **Primary target:** `IC2E 2026 short paper`
2. **Secondary target if not ready by April 24:** `Middleware 2026 Big Ideas`
3. **Ambitious later target:** `SoCC 2026 short research`
4. **Safety net:** `IC2E 2026 poster/demo`

Reason:

- the paper is already real, but the method story is still not strong enough for a confident full-paper push;
- the burst narrative is good enough for a short paper or big-ideas paper;
- IC2E gives the fastest realistic path to a first archival acceptance;
- Middleware gives you a stronger systems framing option if you want a little more time;
- SoCC is the best fit, but it should be treated as the stretch target, not the default one.

## How Submission Actually Works

For conferences like these, the real process is:

1. choose one venue and one paper type
2. freeze the claim set
3. cut the paper to the venue page limit
4. format in the exact template
5. check anonymization rules
6. ensure the paper is not under review anywhere else
7. prepare PDF, figures, and metadata
8. submit through HotCRP or EasyChair
9. wait for reviews
10. revise, rebut, or resubmit depending on the decision

Two practical rules matter a lot:

- you cannot submit the same paper to multiple venues concurrently;
- the paper type matters almost as much as the venue itself.

For this project, choosing the right `paper type` is probably more important than choosing the exact conference brand.

## What To Do Next

### If we target IC2E 2026

By **April 7-10**:

- freeze the title and paper type as `short paper`
- cut the paper to one clean story
- keep only `green` headline claims

By **April 10-15**:

- move fully to IEEE format
- build final figures and tables
- clean references and related work

By **April 15-17**:

- finish metadata, author list, acknowledgements, and AI-disclosure language
- prepare the abstract submission

By **April 24, 2026**:

- submit

### If IC2E slips

Switch immediately to `Middleware 2026 Big Ideas`:

- keep the main theoretical framing
- keep only the strongest aggregate and burst results
- cut anything that reads like an unfinished production-policy claim

### If the paper is still not submission-clean by June

Hold the full paper and use one of:

- `SoCC 2026 short research`
- `SoCC 2026 vision`
- or `IC2E 2026 poster/demo`

That is still a valid first-publication strategy. It is better than forcing a weak full-paper submission too early.

## Cost and Publishing Logistics

For the ACM venues on this list, UMass Amherst appears on the ACM Open participant list:

- <https://libraries.acm.org/acmopen/open-participants>

That strongly suggests ACM open-access publication costs may be covered through the institution, but you should still verify that with the library or advisor before camera-ready.

## Sources

- IC2E 2026 homepage:
  <https://conferences.computer.org/IC2E/2026/index.html>
- IC2E 2026 research/industry CFP:
  <https://conferences.computer.org/IC2E/2026/cfp-main.html>
- IC2E 2026 demos/posters CFP:
  <https://conferences.computer.org/IC2E/2026/cfp-demos-posters.html>
- Middleware 2026 homepage:
  <https://middleware-conf.github.io/2026/>
- Middleware 2026 research CFP:
  <https://middleware-conf.github.io/2026/calls/call-for-research-papers/>
- SoCC 2026 homepage:
  <https://acmsocc.org/2026/>
- SoCC 2026 CFP:
  <https://acmsocc.org/2026/papers.html>
- ACM Open participant list:
  <https://libraries.acm.org/acmopen/open-participants>
