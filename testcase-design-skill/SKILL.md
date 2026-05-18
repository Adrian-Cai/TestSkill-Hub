---
name: 通用测试用例设计生成器
description: 根据需求文档、接口文档、页面说明、代码 Diff、配置变更、数据库变更、Bug 修复说明等输入，生成测试分析、风险清单、测试点、测试用例、回归范围和待确认项，并落地为 Markdown 文件。适用于“根据需求生成测试用例”“测试点设计”“回归范围分析”“变更影响分析”“接口/页面/业务流程测试设计”等场景。
---

# 通用测试用例设计生成器

## 技能介绍

本技能用于将产品需求、接口文档、页面说明、业务流程、代码 Diff、数据库变更、配置变更、Bug 修复说明等输入，转化为可评审、可执行、可落地的测试设计产物。

核心目标：

- 不只生成用例，还要先做测试分析和风险识别
- 不只覆盖接口，还要覆盖业务流程、页面交互、数据、权限、配置、兼容、回归范围
- 不只输出清单，还要明确优先级、前置条件、验证点和待确认项
- 所有结果必须落地为 Markdown 文件，便于评审和沉淀

## 何时应用

当用户提出以下需求时，应使用本技能：

- 根据需求文档生成测试用例
- 根据 PRD / 用户故事设计测试点
- 根据接口文档生成接口测试用例
- 根据页面说明设计 UI 测试用例
- 根据代码 Diff 分析测试影响范围
- 根据 Bug 修复说明补充回归用例
- 根据配置 / 数据库变更设计测试方案
- 生成测试分析报告、测试覆盖矩阵、风险清单、待确认项

## 必须先读的规则

执行本技能时，先阅读：

- `rules/_sections.md`
- `rules/artifact-output.md`
- `rules/input-classification.md`
- `rules/general-test-dimensions.md`

再根据输入内容按需读取：

- 接口相关：`rules/api-test-rules.md`
- 页面相关：`rules/ui-test-rules.md`
- 参数 / 字段 / 金额 / 数量边界：`rules/boundary-strategy.md`
- 鉴权 / 权限 / 越权：`rules/auth-permission-rules.md`
- 业务风险：`rules/business-risk-rules.md`
- 业务链路：`rules/chain-test-rules.md`
- 代码 Diff：`rules/diff-impact-rules.md`
- 数据库变更：`rules/data-test-rules.md`
- 配置变更：`rules/config-test-rules.md`
- 回归范围：`rules/regression-scope-rules.md`
- 人工评审与回流：`rules/review-feedback-rules.md`

## 产出目标

默认每次至少产出：

- `outputs/<YYYY-MM>/<project-slug>/<YYYYMMDD>_v<N>/testcases.md`
- `outputs/<YYYY-MM>/<project-slug>/<YYYYMMDD>_v<N>/metadata.json`

如用户要求脑图，额外产出：

- `outputs/<YYYY-MM>/<project-slug>/<YYYYMMDD>_v<N>/testcases.xmind`

## 输入模式

支持以下输入：

### 1. 需求文档 / PRD

用于生成业务测试点、流程用例、异常场景、回归范围。

### 2. 接口文档

支持 Swagger / OpenAPI / YAPI / RAP / 文本接口描述。

### 3. 页面 / 原型说明

用于生成 UI 交互、表单校验、展示逻辑、兼容性测试。

### 4. 代码 Diff

用于分析变更影响范围、回归重点、风险模块。

### 5. 数据库变更

用于分析字段兼容、默认值、索引、数据迁移、历史数据影响。

### 6. 配置变更

用于分析开关、灰度、降级、环境差异、配置回滚。

### 7. Bug 修复说明

用于生成复现用例、修复验证用例、关联回归用例。

## 执行原则

1. 先判断输入类型，再选择对应规则。
2. 先做测试分析和风险识别，再生成测试用例。
3. 不能只生成正常路径，必须覆盖异常路径、边界、权限、数据、兼容、回归。
4. 如果输入信息不足，基于合理假设继续产出，并在“待确认项”中列出。
5. 输出用例必须包含：前置条件、操作步骤、测试数据、预期结果、优先级。
6. 对高风险场景必须标记 P0 / P1，并说明原因。
7. 产物必须落地为文件，不得只在对话中输出。

## 标准工作流

```text
Task Progress:
- [ ] Step 1: 判断输入类型与测试对象
- [ ] Step 2: 提取业务对象、流程、字段、接口、页面、变更点
- [ ] Step 3: 识别风险点和影响范围
- [ ] Step 4: 确定测试维度与优先级
- [ ] Step 5: 生成测试点和测试用例
- [ ] Step 6: 生成覆盖矩阵和待确认项
- [ ] Step 7: 写入 Markdown 产物
```
