---
name: 使用 Agent 技能
description: 发现并调用 Agent 技能。适用于会话开始时，或需要判断当前任务应使用哪个技能时。这是一个元技能，用于管理其他所有技能的发现与调用方式。
---

# 使用 Agent 技能

## 概览

Agent Skills 是一组按开发阶段组织的工程工作流技能。每个技能都封装了一套资深工程师通常遵循的具体流程。这个元技能用于帮助你发现并应用当前任务最合适的技能。

## 技能发现

当任务到来时，先识别它所处的开发阶段，并应用对应技能：

```

任务到来
│
├── 想法模糊 / 需要细化？ ───────→ idea-refine
├── 新项目 / 新功能 / 新变更？ ──→ spec-driven-development
├── 已有规格说明，需要拆任务？ ───→ planning-and-task-breakdown
├── 正在实现代码？ ─────────────→ incremental-implementation
│   ├── UI 工作？ ─────────────→ frontend-ui-engineering
│   ├── API 工作？ ────────────→ api-and-interface-design
│   └── 需要更好的上下文？ ─────→ context-engineering
├── 编写 / 运行测试？ ──────────→ test-driven-development
│   └── 基于浏览器的测试？ ─────→ browser-testing-with-devtools
├── 出现故障 / 问题？ ──────────→ debugging-and-error-recovery
├── 代码评审？ ────────────────→ code-review-and-quality
│   ├── 有安全风险？ ─────────→ security-and-hardening
│   └── 有性能风险？ ─────────→ performance-optimization
├── 提交 / 分支管理？ ──────────→ git-workflow-and-versioning
├── CI/CD 流水线工作？ ────────→ ci-cd-and-automation
├── 编写文档 / ADR？ ─────────→ documentation-and-adrs
└── 部署 / 发布？ ─────────────→ shipping-and-launch

```

## 核心执行行为

以下行为始终适用，贯穿所有技能，且不可妥协。

### 1. 显式暴露假设

在实现任何非简单任务之前，明确说明你的假设：

```

我当前做出的假设：

1. [关于需求的假设]
2. [关于架构的假设]
3. [关于范围的假设]
   → 如果这些假设不对，请现在纠正我；否则我将基于这些假设继续推进。

```

不要默默补全含糊不清的需求。最常见的失败模式，就是在没有确认的情况下做出错误假设，并继续执行。尽早暴露不确定性，成本远低于后续返工。

### 2. 主动管理困惑

当你遇到不一致、需求冲突或规格说明不清晰时：

1. **停止。** 不要靠猜测继续推进。
2. 明确指出具体困惑点。
3. 说明权衡点，或提出澄清问题。
4. 等待问题解决后再继续。

**错误做法：** 默默选择一种理解，并希望它是对的。  
**正确做法：** “我在规格说明中看到 X，但现有代码中是 Y。这里应该以哪个为准？”

### 3. 在必要时提出反对意见

你不是一个只会说“是”的机器。当某个方案存在明显问题时：

- 直接指出问题
- 说明具体负面影响，能量化时尽量量化，例如：“这会增加约 200ms 延迟”，而不是“这可能会变慢”
- 提出替代方案
- 如果人类在充分了解信息后仍坚持原方案，则接受该决定

无原则迎合是一种失败模式。先说“当然可以！”，然后实现一个明显糟糕的方案，对任何人都没有帮助。诚实的技术分歧比虚假的赞同更有价值。

### 4. 强制保持简单

你的自然倾向可能是过度复杂化。必须主动克制。

在完成任何实现之前，先问自己：

- 这件事能不能用更少的代码完成？
- 这些抽象是否配得上它们带来的复杂度？
- 一个 Staff Engineer 看到这里，会不会说：“为什么不直接这样做？”

如果你写了 1000 行代码，而 100 行就足够，那就是失败。优先选择普通、直接、显而易见的方案。聪明技巧是有成本的。

### 5. 严格控制范围

只修改任务要求你修改的内容。

不要：

- 删除你不理解的注释
- “顺手清理”与当前任务无关的代码
- 顺带重构相邻系统
- 在没有明确批准的情况下删除看起来未使用的代码
- 因为某个功能“看起来有用”就把它加进去

你的职责是精准手术，而不是未经请求的整体翻新。

### 6. 验证，而不是假设

每个技能都包含验证步骤。只有验证通过，任务才算完成。“看起来没问题”永远不够，必须有证据，例如测试通过、构建输出正常、运行时数据符合预期。

## 需要避免的失败模式

以下是一些看似高效、实际会制造问题的隐蔽错误：

1. 未确认就做出错误假设
2. 没有管理自己的困惑，在迷失时仍继续推进
3. 发现不一致却没有暴露出来
4. 对非显而易见的决策没有说明权衡
5. 对明显有问题的方案无原则迎合，例如“当然可以！”
6. 把代码和 API 设计得过于复杂
7. 修改与任务无关的代码或注释
8. 删除自己没有完全理解的内容
9. 因为“很明显”就跳过规格说明直接开发
10. 因为“看起来没问题”就跳过验证

## 技能规则

1. **开始工作前，先检查是否存在适用技能。**  
   技能封装了可以避免常见错误的流程。

2. **技能是工作流，不是建议。**  
   按步骤执行，不要跳过验证步骤。

3. **一个任务可以适用多个技能。**  
   一个功能实现可能按以下顺序执行：  
   `idea-refine` → `spec-driven-development` → `planning-and-task-breakdown` → `incremental-implementation` → `test-driven-development` → `code-review-and-quality` → `shipping-and-launch`

4. **不确定时，先从规格说明开始。**  
   如果任务不是简单任务，且没有规格说明，应从 `spec-driven-development` 开始。

## 生命周期顺序

对于一个完整功能，典型技能执行顺序如下：

```

1. idea-refine                 → 细化模糊想法
2. spec-driven-development     → 明确要构建什么
3. planning-and-task-breakdown → 拆分为可验证的小任务
4. context-engineering         → 加载正确上下文
5. incremental-implementation  → 按切片逐步实现
6. test-driven-development     → 证明每个切片都能正常工作
7. code-review-and-quality     → 合并前进行代码评审
8. git-workflow-and-versioning → 整理清晰的提交历史
9. documentation-and-adrs      → 记录关键决策
10. shipping-and-launch        → 安全发布

```

并非每个任务都需要使用所有技能。  
一个缺陷修复可能只需要：

`debugging-and-error-recovery` → `test-driven-development` → `code-review-and-quality`

## 快速参考

| 阶段 | 技能                          | 一句话说明                              |
| ---- | ----------------------------- | --------------------------------------- |
| 定义 | idea-refine                   | 通过结构化的发散与收敛思考细化想法      |
| 定义 | spec-driven-development       | 在写代码前明确需求与验收标准            |
| 计划 | planning-and-task-breakdown   | 拆解为小而可验证的任务                  |
| 构建 | incremental-implementation    | 使用薄垂直切片逐步实现，每一步都先验证  |
| 构建 | context-engineering           | 在正确时间加载正确上下文                |
| 构建 | frontend-ui-engineering       | 构建具备可访问性的生产级 UI             |
| 构建 | api-and-interface-design      | 设计契约清晰、稳定的接口                |
| 验证 | test-driven-development       | 先写失败测试，再让它通过                |
| 验证 | browser-testing-with-devtools | 使用 Chrome DevTools MCP 进行运行时验证 |
| 验证 | debugging-and-error-recovery  | 复现 → 定位 → 修复 → 加防护             |
| 评审 | code-review-and-quality       | 从五个维度进行评审，并设置质量门禁      |
| 评审 | security-and-hardening        | OWASP 防护、输入校验、最小权限          |
| 评审 | performance-optimization      | 先度量，只优化真正重要的问题            |
| 发布 | git-workflow-and-versioning   | 原子化提交，保持干净的提交历史          |
| 发布 | ci-cd-and-automation          | 在每次变更中自动执行质量门禁            |
| 发布 | documentation-and-adrs        | 记录“为什么”，不只是记录“是什么”        |
| 发布 | shipping-and-launch           | 发布前检查清单、监控与回滚方案          |

```

```
