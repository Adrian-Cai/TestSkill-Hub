# 本章可交付物清单

Use this reference when the user asks "本章可交付物清单在哪里", "讲完后学员需要什么", "课后材料", "学员带走什么", or asks to package training outputs for learners.

## Output Rule

Separate deliverables into two groups:

- **课堂演示产物**: produced during the instructor demonstration or classroom practice.
- **课后复用材料**: templates and checklists learners can use in real projects after class.

Do not add unrelated artifacts. Keep the list tied to the chapter topic and actual testing workflow.

## Default Deliverables For AI Requirement Review And Test Point Design

### 课堂演示产物

- 需求摘要示例
- 业务规则清单示例
- 测试点矩阵示例
- 需求疑问与风险清单示例
- 风险优先级排序示例

### 课后复用材料

- 《AI辅助需求评审清单》
- 《测试点拆解Prompt模板》
- 《功能测试用例生成模板》
- 《需求规则提取模板》
- 《测试点矩阵模板》
- 《需求疑问与风险清单模板》

## Minimum Learner Pack

If the user asks for a compact version, include only:

1. 《AI辅助需求评审清单》
2. 《测试点拆解Prompt模板》
3. 《测试点矩阵模板》
4. 《需求疑问与风险清单模板》

## Recommended File Layout

When creating files, use a clear learner-pack folder:

```text
outputs/<course-or-chapter-slug>/learner-pack/
├─ 01-ai-requirement-review-checklist.md
├─ 02-test-point-prompt-template.md
├─ 03-test-point-matrix-template.xlsx or .md
├─ 04-requirement-questions-risk-list.md
└─ 05-example-coupon-test-point-matrix.md
```

Use Markdown by default. Use `.xlsx` only when the user asks for spreadsheet-ready templates or when the matrix is large enough to benefit from spreadsheet editing.

## Quality Gate

Before finalizing learner deliverables:

- Each item must be usable by a tester after class.
- Each template must show where to put inputs, what AI should do, what humans must review, and what output should be produced.
- The list must distinguish examples from reusable templates.
- The deliverables must reinforce that AI assists analysis; testers confirm business rules, risks, and final quality.
