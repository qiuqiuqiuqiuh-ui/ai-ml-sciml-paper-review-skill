# Review behavior evaluation

These five inputs are explicitly synthetic exercises, not papers or experimental findings. They exercise decision boundaries that packaging CI cannot check. [The public-paper example](../examples/resnet-review.md) demonstrates source-grounded output separately.

## Run a manual evaluation

1. Give an evaluator the skill and inputs from `inputs/`. Do not give it the rubric or earlier outputs. Prefer a fresh context for each case; if cases share a context, record that limitation.
2. Keep the run read-only and offline; the inputs contain all necessary local evidence. Claims about novelty should remain unverified.
3. Save the complete response before comparing it with [the rubric](rubric.md).
4. Record the skill commit, evaluator/model if known, date, available tools, material scope, per-case observations, and unresolved issues.
5. Repeat relevant cases after changes that affect those decisions. Do not treat a small exercise set as general accuracy evidence.

There is no automated LLM runner or word-matching score. GitHub Actions runs the script regression tests; behavioral results require actual evaluator responses and human judgment.

See the [2026-10-13 trial record](results/2026-10-13/README.md), including the baseline locator error and targeted retest.
