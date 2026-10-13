# Contributing

Changes are most useful when they address a demonstrated review error or a reproducible packaging problem. Small corrections are welcome.

## Report a problem

Include the input type, source version, relevant section or code location, actual output, and the decision that should change. Explain whether the problem is an incorrect fact, unsupported criticism, missed evidence, excessive requirements, or an installation/validation failure. Use public sources or a minimal synthetic example; do not post confidential manuscripts.

## Make a change

1. Keep shared constraints in `SKILL.md` and substantial conditional checks in `references/`.
2. Preserve the skill invocation name unless a change includes an explicit migration plan.
3. Add a regression test for a demonstrated script failure. For review behavior, add a self-contained input and an evidence-based rubric rather than checking exact wording.
4. Run the validation and tests listed in [the README](README.md#develop-and-evaluate).
5. Explain what changed, why it affects a review decision, how it was checked, and what remains uncertain.

Do not turn every possible experiment into a universal requirement. A justified narrowing of a paper's claim can resolve an issue without adding a new experiment. New scientific assertions should have a verifiable source or be labeled as a proposed check.

## 中文提示

提交问题时，请提供材料版本、可核查定位、实际输出与应改变的判断。区分事实错误、无证据批评、遗漏证据、过度实验要求和安装问题。脚本缺陷应附回归测试；审稿行为应附输入与证据评价规则，不要求固定措辞。请使用公开或合成材料。
