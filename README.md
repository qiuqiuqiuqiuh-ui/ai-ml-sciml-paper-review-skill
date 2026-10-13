# Rigorous Paper Review

An evidence-grounded agent skill for AI, ML, and SciML paper review, with claim–evidence tracking and reproducibility checks.

[中文说明](README.zh-CN.md) · [Example review](examples/resnet-review.md) · [Contributing](CONTRIBUTING.md) · [CI](https://github.com/qiuqiuqiuqiuh-ui/rigorous-paper-review/actions/workflows/validate.yml) · [MIT license](LICENSE)

## What makes it useful

- Separate author claims, reported observations, justified inferences, and unanswered questions.
- Audit baselines, ablations, comparison budgets, statistics, leakage, and generalization.
- Apply targeted checks for SciML, LLM/Agent evaluation, benchmarks, theory, and code.
- Track claims and review issues across rebuttals without treating promised experiments as completed evidence.
- Scale the review to the question and available material; an abstract supports a preliminary assessment.

This is a skill, not a standalone review service. Codex is the tested host. Responses default to Chinese; ask for English when needed. Structural CI does not establish scientific review accuracy, and reading code does not establish independent reproduction.

## Install

Clone the repository into a development directory, then install its skill files. The installer uses Python 3.10+ and only the standard library; using the installed skill itself does not require Python. Substitute your Python 3 executable for `python` if needed.

```bash
git clone https://github.com/qiuqiuqiuqiuh-ui/rigorous-paper-review.git
cd rigorous-paper-review
python scripts/install_skill.py
```

The repository name is **rigorous-paper-review**. The installation directory and invocation name remain **review-papers-rigorously** for compatibility. The default destination is `$CODEX_HOME/skills/review-papers-rigorously`, or `~/.codex/skills/review-papers-rigorously` when `CODEX_HOME` is unset. The updated skill is available on your next turn.

## Use

```text
Use $review-papers-rigorously to review this paper in English.
Focus on evidence for its core claims, comparison fairness, and conclusion boundaries.

Use $review-papers-rigorously to check the theorem assumptions and proof.

Use $review-papers-rigorously to update the original review from this rebuttal and new results.
```

Provide a PDF, accessible paper URL, or paper text, and the matching code version when relevant. Formal reviews should include the venue rubric and material-use policy. External novelty checks need retrieval access; actual reproduction needs an explicit request, data, and a resource budget.

## Update and verify

From the development checkout:

```bash
git pull --ff-only
python scripts/install_skill.py --update
python scripts/install_skill.py --check
```

Updates first back up the existing installation to `~/.codex/skill-backups/review-papers-rigorously/<UTC timestamp>` by default. The installer prints the actual path, preserves unrelated local files, and writes `INSTALLATION.json` with source commit information, working-tree status, and file hashes. `--check` compares installed skill files with this checkout; it does not verify the running chat's cached context. Use `--target /path/to/review-papers-rigorously` for a custom complete installation path.

## Develop and evaluate

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_skill.py .
python -m unittest discover -s tests -v
```

Repository validation allows a different checkout name, including GitHub ZIP folders. `--installed` additionally checks the installation directory name. Validation covers metadata, missing local files, Markdown heading links, and unfinished scaffold lines. It parses Markdown links, including reference links, while ignoring code examples. External URLs are not fetched. Only generated Markdown heading anchors are supported; custom HTML anchors are not recognized.

GitHub Actions runs packaging validation and regression tests. Review behavior is evaluated separately using [five synthetic cases and a manual rubric](evals/README.md). These cases are exercises, not reported research results or an estimate of general review accuracy.

The installed skill contains `SKILL.md`, `agents/`, `references/`, optional assets, and the license. Tests, evaluation cases, and examples stay in the development repository.
