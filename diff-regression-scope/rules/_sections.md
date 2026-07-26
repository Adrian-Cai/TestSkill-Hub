# 规则索引

执行 `diff-regression-scope` 时按需读取以下规则：

- `rules/diff-impact-analysis.md`：用于从 Git Diff / PR Diff / 变更文件清单中识别影响面。
- `rules/regression-priority.md`：用于判定必测、建议测、可抽测和可暂不测范围。
- `rules/artifact-file-output.md`：用于将分析结果落地为 Markdown 文件。

核心顺序固定为：

```text
Diff 事实层 -> 影响面 -> 风险点 -> 回归范围 -> 测试产出
```
