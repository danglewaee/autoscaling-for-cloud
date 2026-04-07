# Author Defense Sheet

This document is for the **human author** of the paper.

Purpose:

- make sure the paper is genuinely yours to defend,
- reduce the risk of submitting a draft that sounds polished but is not fully owned,
- prepare for advisor questions, reviewer objections, and submission-form decisions.

Primary papers:

- long draft:
  [paper/calibration_aware_autoscaling_paper.tex](/D:/UMASS%20AMHERST/Study/Sophomore/Research/Self%20Research/autoscaling-for-cloud/paper/calibration_aware_autoscaling_paper.tex)
- short-paper draft:
  [paper/calibration_aware_autoscaling_ic2e_short.tex](/D:/UMASS%20AMHERST/Study/Sophomore/Research/Self%20Research/autoscaling-for-cloud/paper/calibration_aware_autoscaling_ic2e_short.tex)

## How To Use This Sheet

You should be able to answer each question:

- without reading from the paper,
- in your own words,
- in about `20-60` seconds,
- and without drifting into claims the paper does not support.

If you cannot do that, the paper is not yet fully author-owned.

## Section A: One-Minute Ownership Test

You should be able to answer all five of these immediately.

### A1. What is the paper actually about?

Target answer:

- It studies autoscaling as a decision problem under uncertainty, not just a forecasting problem.
- The paper asks whether calibration quality affects downstream scaling quality.
- The empirical point is that burst-only evaluation reveals failures that aggregate metrics can hide.

Bad sign:

- you answer by listing file names, models, or baselines before stating the core question.

### A2. Why is this not just another forecasting paper?

Target answer:

- Because the paper is about how uncertainty enters the scaling decision.
- A forecast can have decent point error but still be dangerous for autoscaling if its upper tail is miscalibrated.
- The contribution is decision-aware evaluation, not just better prediction accuracy.

Bad sign:

- you start talking only about MAE or RMSE.

### A3. Why did you use Azure Functions 2021?

Target answer:

- It is a public, reproducible serverless trace.
- It supports an autoscaling-style setup with invocation timing and duration information.
- It is a better fit for the paper's cloud/serverless scope than heavier cluster traces that do not map as cleanly to this decision problem.

Bad sign:

- you say only that it is "official" or "from Microsoft" without mentioning fit.

### A4. What is the central claim?

Target answer:

- Forecast accuracy alone is not enough for robust autoscaling.
- Calibration quality materially affects downstream scaling decisions.
- Aggregate metrics are insufficient because burst-only windows reveal much harsher failures.

Bad sign:

- you claim the method already solves burst robustness.

### A5. What is the strongest result right now?

Target answer:

- The strongest result is not that the proposed method dominates everything.
- The strongest result is that predictive methods look reasonable on aggregate metrics, but burst-only evaluation reveals severe hidden failure modes for all current methods.
- That empirical gap is central to the paper's value.

Bad sign:

- you oversell the risk-calibrated method as clearly best overall.

## Section B: Theory Defense

### B1. What does the main theorem say?

Target answer:

- If your upper predictive bound is calibrated up to error $\varepsilon$, then the induced exceedance probability is bounded by $\alpha + \varepsilon$.
- In plain language, calibration error transfers directly into SLA error.

Bad sign:

- you restate the theorem symbolically but cannot explain it in plain English.

### B2. Why is this theorem useful?

Target answer:

- It links a calibration metric to a decision metric.
- It justifies why calibration should matter to autoscaling, rather than being only a descriptive forecast property.

Bad sign:

- you say only that it "looks rigorous".

### B3. What does the quantile discussion contribute?

Target answer:

- It explains why fixed-quantile scaling is not arbitrary.
- Under a simplified asymmetric-cost objective, a quantile rule is the optimizer.
- This gives a decision-theoretic interpretation to the fixed-quantile baseline.

Bad sign:

- you claim the full dynamic method is proved optimal by this argument.

### B4. What does the paper explicitly not prove?

Target answer:

- It does not prove an exact finite-sample guarantee for the implemented residual method.
- It does not claim distribution-free robustness for the deployed policy.
- It does not prove that the current method dominates point-forecast scaling in all settings.

Bad sign:

- you blur together conformal guarantees and the current implementation.

## Section C: Method Defense

### C1. What is the method in one paragraph?

Target answer:

- Fit a simple short-horizon autoregressive forecaster.
- Use validation residuals to build calibrated intervals and demand scenarios.
- Choose capacity by minimizing an objective that balances cost, underprovision risk, and oscillation.

Bad sign:

- you give a long pipeline description but cannot summarize the decision logic.

### C2. Why use a simple linear autoregressive predictor?

Target answer:

- To isolate the role of calibration and decision logic.
- A stronger forecaster would make it harder to tell whether gains came from model scale or from the uncertainty-aware policy.
- For a first paper, this keeps the system reproducible and interpretable.

Bad sign:

- you answer that it was used only because it was easy.

### C3. What is the decision objective actually trading off?

Target answer:

- provisioning cost,
- expected underprovision under calibrated demand scenarios,
- and oscillation relative to the previous capacity.

Bad sign:

- you cannot explain why oscillation is in the objective.

### C4. Why did you not make the method more complicated?

Target answer:

- Because the paper's contribution is not "the biggest model".
- The goal is to test a decision hypothesis cleanly on a public trace.
- Complexity would make attribution harder and could weaken the short-paper story.

Bad sign:

- you sound apologetic rather than deliberate.

## Section D: Experimental Defense

### D1. What are the baselines and why these ones?

Target answer:

- Reactive scaling, moving average, point forecast, and fixed quantile.
- Together they cover the main design families the paper wants to separate: reactive control, smoothing heuristics, point-forecast scaling, and quantile-based uncertainty heuristics.

Bad sign:

- you cannot explain what each baseline stands for conceptually.

### D2. What do the aggregate results say?

Target answer:

- Reactive is clearly weak on reliability.
- Risk-calibrated is competitive with point-forecast scaling on aggregate metrics.
- But aggregate metrics do not tell the full story.

Bad sign:

- you present aggregate results as if they settle the paper.

### D3. What do the burst-only results say?

Target answer:

- Burst windows are rare but much harder.
- All methods perform badly there, including the calibration-aware one.
- This is the core evidence that average metrics hide the real difficulty.

Bad sign:

- you minimize how weak the burst results still are.

### D4. Why keep a result that shows your method still fails?

Target answer:

- Because that failure is scientifically informative.
- It supports the paper's main argument about evaluation and hidden failure regimes.
- A first paper does not need to solve the whole problem to contribute something publishable.

Bad sign:

- you sound embarrassed by the burst results.

### D5. Why is burst-only evaluation important?

Target answer:

- Because SLA risk is concentrated in rare hard windows.
- Aggregate averages can make a policy look safe even if it fails exactly where users care most.
- The paper's main empirical contribution depends on making that regime visible.

Bad sign:

- you describe burst-only analysis as just an extra ablation.

## Section E: Limitation Defense

### E1. What are the top three limitations?

Target answer:

1. the calibration layer is residual-based, not fully conformalized
2. the empirical study uses one public serverless trace
3. the current method is still weak on bursts

Bad sign:

- you answer only with future-work slogans.

### E2. Why is the paper still publishable despite those limitations?

Target answer:

- Because the contribution is focused and honest.
- The paper contributes a clean framing, a theorem-to-decision link, and an evaluation result that changes how autoscaling quality should be interpreted.
- Short papers are allowed to make narrower contributions than full mature systems papers.

Bad sign:

- you try to pretend the limitations are minor.

## Section F: Venue and Submission Defense

### F1. Why IC2E short paper instead of a bigger venue?

Target answer:

- Because the topic fits cloud engineering well.
- The paper is real, but its strongest value is still a focused short-paper story rather than a mature full-method systems story.
- This is the pragmatic path to a first accepted publication.

Bad sign:

- you say only that IC2E is "easier".

### F2. What paper type is this?

Target answer:

- A short research paper in the research track.

Bad sign:

- you are unsure whether it is research, vision, or experience.

### F3. What happens after submission?

Target answer:

- Abstract submission by the venue deadline.
- Full paper submission by the venue deadline.
- Then peer review.
- Then author notification.
- If accepted, camera-ready submission.
- Only after acceptance and camera-ready does it become a published conference paper.

Bad sign:

- you think "submitted" means "published".

## Section G: AI and Authorship Defense

### G1. Did you use AI assistance?

Target answer:

- Yes, as a writing and coding assistant.
- But the research decisions, final claims, and submission responsibility remain with the author.
- The venue disclosure policy will be followed exactly.

Bad sign:

- you try to hide the fact or become vague.

### G2. Why is this still your paper?

Target answer:

- Because I understand the question, method, assumptions, results, and limitations.
- I can explain and defend every major choice in my own words.
- I am taking responsibility for the final submitted content.

Bad sign:

- you rely on "the bot said so" for any substantive claim.

### G3. What must you be able to defend without help?

Target answer:

- why the problem matters
- why the dataset fits
- what the theorem means
- how the method works
- what the results actually show
- what the paper does not claim

Bad sign:

- you can paraphrase the abstract but not answer follow-up questions.

## Final Ownership Test

Before submission, you should be able to do this:

1. explain the paper in `60` seconds
2. explain the theorem in plain English
3. explain the difference between aggregate and burst results
4. name the top limitations without reading
5. explain why IC2E short is the right venue
6. explain the role of AI assistance honestly and calmly

If any of these fail, the paper is not yet fully author-owned.

That does not mean the paper is bad.
It means the author needs one more pass of understanding before submitting.
