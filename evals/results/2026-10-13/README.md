# Behavioral trial: 2026-10-13

This is a manual assessment of five synthetic exercises. The evaluator received only the skill, applicable references, and inputs, without the rubric or the editor's earlier findings. It worked offline without experiments. The five baseline cases shared one fresh evaluation context; the targeted retest used a second fresh context. The exact backend model identifier was not exposed by the collaboration tool.

## Baseline observations

| Case | Assessment | Evidence in the saved response |
|---|---|---|
| [01: abstract](baseline/01-abstract-only.md) | Needs revision | Correctly limits the assessment to the abstract, but C2 locates the accuracy result in the third sentence; the input puts it in the second sentence. |
| [02: theory](baseline/02-theory.md) | Passed | Verifies positive definiteness and uniqueness, and does not require training experiments or ablations. |
| [03: leakage](baseline/03-leakage.md) | Passed | Identifies person overlap and full-data normalization; distinguishes correlated windows from independent people; leaves unreported hyperparameter selection unknown. |
| [04: PINN](baseline/04-pinn-residual.md) | Passed | Derives u(t)=1 and checks the explicit initial-condition violation of the zero model. |
| [05: rebuttal](baseline/05-rebuttal.md) | Passed | Retains R1/R2, resolves R1's reporting request, and keeps R2 unresolved because the reply only promises a future experiment. |

The observed locator error led to one narrow skill change: abstract/excerpt locations may use material titles and keywords; sentence numbers and line numbers require verification. The baseline responses remain available, including the error. The accompanying [manifest](manifest.json) identifies evaluated input, skill, reference, and response versions by SHA256 and pins the evaluated source to commit a3101bc, before later display-name changes.

## Targeted retest

[The new abstract response](retest/01-abstract-only.md) passed the rubric. It uses verifiable abstract keywords instead of an unchecked sentence number, keeps novelty unverified, and distinguishes unavailable methods/results from experiments never performed. Only this affected case was rerun after the locator change; the other four observations belong to the baseline skill version.

Published responses preserve their text, with CRLF normalized to LF for portability. Script regression tests are a separate check. These observations support only the exercised decisions in this run; they do not estimate accuracy on full papers or prove repeatability across model versions.
