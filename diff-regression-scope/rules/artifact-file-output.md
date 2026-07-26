# 文件落地规则

默认将报告写入：

```text
outputs/analysis/<slug>.md
```

如果当前项目没有 `outputs/analysis` 目录，先创建。

文件命名建议：

- `diff-regression-scope-<module>.md`
- `pr-<id>-regression-scope.md`
- `<feature>-diff-risk-analysis.md`

最终回复必须包含：

- 文件路径
- 最高风险摘要
- 必测范围摘要
- 待确认项数量或关键待确认项

不要只在对话中输出完整报告而不落地文件。
