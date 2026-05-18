# 输入分类规则

## 目标

在生成测试设计前，先判断用户输入属于哪类测试对象，并决定加载哪些规则。

## 输入类型判断

| 输入特征 | 输入类型 | 建议加载规则 |
| --- | --- | --- |
| 包含需求背景、目标、流程、规则 | 需求文档 / PRD | coverage-multi-dimension.md, trace-requirement-mapping.md |
| 包含 path、method、request、response、status code | 接口文档 | api-test-rules.md |
| 包含页面、按钮、弹窗、表单、列表、筛选、跳转 | 页面说明 | ui-test-rules.md |
| 包含 diff、commit、Controller、Service、Mapper、Config、DTO | 代码 Diff | diff-impact-rules.md |
| 包含表结构、字段、索引、SQL、迁移 | 数据库变更 | data-test-rules.md |
| 包含开关、灰度、白名单、降级、配置项 | 配置变更 | config-test-rules.md |
| 包含 bug、修复、复现、影响范围 | Bug 修复 | regression-scope-rules.md |

## 多类型输入

如果输入同时包含多种类型，应组合加载规则。