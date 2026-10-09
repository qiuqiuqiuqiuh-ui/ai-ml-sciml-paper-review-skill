# review-papers-rigorously

用于 AI、ML、Deep Learning 和 SciML 论文的中文严谨评审技能。将作者主张、论文报告的直接证据、合理推断和未验证部分建立为可追溯账本，并按核心结论选择检查。

## 能做什么

- 批判性阅读、正式评审、创新性核查、实验可信度审查及复现决策。
- 检查 baselines、ablations、比较公平性、统计、泄漏、泛化、理论条件和效率。
- 按需检查 SciML 物理有效性，LLM/Agent 评估，数据集与 benchmark，以及公式到代码的映射。
- 使用稳定的主张 ID 和问题 ID 更新 rebuttal 证据，区分已解决、部分解决、未解决与无法核查。

技能按材料和问题调整深度。摘要或节选只支持初步分析；静态代码检查、运行成功、结果复现和科学结论验证分别记录。它不能保证评审正确，也不能替代原文核查和领域专家判断。

## 安装与使用

将本仓库目录复制到你的 Codex 技能目录，例如 `~/.codex/skills/review-papers-rigorously`。仅安装技能本身不需要 Python；Python 和 PyYAML 仅用于仓库校验。

```text
使用 $review-papers-rigorously 评审这篇论文，重点核查核心贡献、比较公平性和结论边界。

使用 $review-papers-rigorously 检查正文与附录中的定理条件，并区分已核查证明和未验证部分。

使用 $review-papers-rigorously 根据这份 rebuttal 和新实验，更新原评审的问题状态。
```

提供 PDF、可访问的论文链接或论文文本；如需代码核查，提供对应版本。正式评审应同时给出会议/期刊量表及材料使用政策。创新性外部核查需要可用检索工具；受联网限制时应标明尚未外部核查。实际复现需明确提出，并提供运行资源与数据。

## 文件结构

- `SKILL.md`：触发范围、证据账本、评审流程和交付要求。
- `agents/openai.yaml`：显示信息与自动调用策略。
- `references/sciml.md`：SciML 专项检查。
- `references/specialized-checks.md`：LLM/Agent、基准、理论和代码检查。
- `scripts/validate_skill.py`：验证 frontmatter、元数据和本地资源引用。

## 开发校验

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_skill.py .
```

GitHub Actions 自动执行相同检查。该检查只验证技能包结构和引用完整性，不衡量实际审稿质量。实际质量应通过真实论文案例核查证据定位、批评成立性及补证建议的必要性。

本次修订修复不存在的图标引用，明确有限材料与单点评审范围，兼容理论证据的支持程度措辞，增加代码检查边界与 rebuttal 问题追踪。

仓库尚未指定开源许可证。
