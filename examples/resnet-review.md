# Example: a bounded review of ResNet

Source: He et al., [Deep Residual Learning for Image Recognition, arXiv v1](https://arxiv.org/pdf/1512.03385v1). Scope: Sections 3.2 and 4.1, Figure 4, and Table 2. This is an illustrative excerpt; no training was reproduced and novelty was not externally audited.

| ID | Author claim | Reported evidence | Inference | Boundary |
|---|---|---|---|---|
| C1 | Residual reformulation eases optimization. | Figure 4 compares training and validation curves; Table 2 reports better validation performance for the 34-layer residual network than its plain counterpart. | The comparison supports an optimization benefit in the tested ImageNet setting. | It does not establish a universal convergence guarantee. |

R1 — **Reader clarification, linked to C1.** Section 3.2 distinguishes identity shortcuts from projections used when dimensions change. Parameter-free identity shortcuts should not imply that every shortcut configuration is parameter-free. Preserve that distinction in implementation summaries; this is a reader note, not an alleged defect in the paper.

The evidence supports the tested comparison. It does not independently verify implementation fidelity, performance under new training protocols, or first-of-kind novelty. This excerpt demonstrates evidence separation without inventing a mandatory criticism or acceptance score.
