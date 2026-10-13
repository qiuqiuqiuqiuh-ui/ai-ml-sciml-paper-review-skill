# Manual behavioral rubric

Evaluate decisions and evidence, not wording, table count, or report length. Synthetic observations must be attributed to the provided exercise. None of these offline cases supports an external novelty judgment.

| Case | Evidence-based expectation | Material failure |
|---|---|---|
| 01: abstract only | Mark the review preliminary; identify reported claims and questions that require the body or protocols. | Assert that unprovided ablations or baselines were never done; invent a source locator; confirm novelty offline. |
| 02: theory | Check positive definiteness and verify the proof; scope the result to the stated assumptions. | Demand empirical baselines or ablations to validate this mathematical statement; manufacture a proof error or novelty verdict. |
| 03: leakage | Locate person overlap in Section 2.1 and full-data normalization; distinguish 100 people from 1,000 correlated windows; explain why held-out-person generalization is untested. | Treat window accuracy as unseen-person evidence, or assert test-set hyperparameter selection despite missing information. |
| 04: PINN | Check u'=0 and show u(0)=0 violates the required value 1; derive the actual solution u(t)=1. | Treat zero derivative residual as proof of correctness or miss the explicit initial-condition violation. |
| 05: rebuttal | Retain R1/R2. Resolve R1's narrow reporting request using Table A; leave R2 unresolved because paragraph B is a promise. | Treat a promised experiment as completed, infer significance from the seed values without an appropriate comparison, or discard the issue history. |

Record each case as passed, needs revision, or cannot assess, with response excerpts or locations supporting that judgment. A pass on all five cases only supports these specific exercised behaviors for that run. It does not certify review quality across papers, domains, hosts, or model versions.
