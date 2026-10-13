# 严谨论文评审

面向 AI、ML 和 SciML 的 agent skill：建立主张与证据的可追溯对应关系，审查实验可信度、理论条件与复现边界。

[English](README.md) · [公开论文示例](examples/resnet-review.md) · [贡献指南](CONTRIBUTING.md) · [MIT 许可证](LICENSE)

## 核心能力

- 区分作者主张、论文报告的直接证据、合理推断和未验证部分。
- 按核心结论检查 baselines、ablations、比较公平性、统计、泄漏和泛化。
- 按需使用 SciML、LLM/Agent、数据集、理论证明与代码检查。
- 用稳定的主张和问题 ID 更新 rebuttal，区分解释、未来承诺与已提供结果。
- 根据材料和问题选择深度，避免从摘要推断整篇论文缺失实验。

当前验证的使用环境是 Codex。默认中文，可明确要求英文。结构校验不能证明评审质量；代码阅读、运行成功、结果复现和科学结论验证需要分别记录。

## 安装

将仓库克隆到开发目录，再安装技能文件。安装脚本只需要 Python 3.10+ 标准库；使用已安装技能不需要 Python。若 `python` 不在 PATH 中，请替换成你的 Python 3 可执行文件。

```bash
git clone https://github.com/qiuqiuqiuqiuh-ui/rigorous-paper-review.git
cd rigorous-paper-review
python scripts/install_skill.py
```

仓库名为 `rigorous-paper-review`；安装目录和调用名保留 `review-papers-rigorously`。默认安装到 `$CODEX_HOME/skills/review-papers-rigorously`；未设置 `CODEX_HOME` 时使用 `~/.codex/skills/review-papers-rigorously`。更新后的技能会在下一轮对话中可用。

## 使用

```text
使用 $review-papers-rigorously 评审这篇论文，重点检查核心贡献、比较公平性和结论边界。

使用 $review-papers-rigorously 核查正文与附录的定理条件和关键证明步骤。

使用 $review-papers-rigorously 根据 rebuttal 和新结果，更新原评审的问题状态。
```

提供 PDF、可访问的链接或论文文本；代码核查需提供对应版本。正式评审应提供量表及材料使用政策。外部创新性核查需要检索能力；实际复现需要明确提出，并提供数据与资源预算。

## 更新与核对

在开发仓库目录执行：

```bash
git pull --ff-only
python scripts/install_skill.py --update
python scripts/install_skill.py --check
```

更新会先备份旧安装，默认备份路径为 `~/.codex/skill-backups/review-papers-rigorously/<UTC 时间戳>`；脚本会显示实际路径。它保留无关本地文件，并生成包含源提交、工作区状态和文件哈希的 `INSTALLATION.json`。`--check` 比较磁盘上的技能文件，不证明当前对话已重新加载缓存。自定义完整安装路径可使用 `--target /path/to/review-papers-rigorously`。

## 开发与测试

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_skill.py .
python -m unittest discover -s tests -v
```

仓库校验允许 checkout 或 ZIP 目录名称不同；`--installed` 额外验证安装目录名。校验包含元数据、本地文件、Markdown 标题锚点及未完成占位符。代码示例不会被误当作实际链接，外部 URL 不会被访问。目前支持 Markdown 标题生成的锚点，不识别自定义 HTML 锚点。

GitHub Actions 执行结构校验与回归测试。审稿行为另用[五个合成案例和人工评价规则](evals/README.md)检查，案例不代表真实研究结果或总体评审准确率。测试、评测输入与示例留在开发仓库，不作为技能指令安装。
