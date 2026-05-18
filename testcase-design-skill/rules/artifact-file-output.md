---
title: 产物必须落地文件
impact: 关键
impactDescription: 防止结果只停留在会话页面，并保证每次生成可追踪
tags: artifact, markdown, xmind, output, metadata
---

## 产物必须落地文件

测试策略和测试用例必须写入本地文件，不能只在会话中展示。每次生成还必须产出 `metadata.json`，用于追踪生成上下文。

**错误（只给页面结果，无文件）：**

```markdown
## 一、测试策略
...
```

**正确（先落地文件，再做摘要）：**

```text
输出文件：
- outputs/2026-04/payment-refund/20260418_v1/testcases.md
- outputs/2026-04/payment-refund/20260418_v1/metadata.json

会话仅展示摘要与文件路径。
```

### 输出路径规范（分层结构）

```
outputs/
└── <YYYY-MM>/              ← 按年月分组
    └── <project-slug>/     ← 按项目/需求名分组（英文小写，连字符分隔）
        └── <YYYYMMDD>_v<N>/  ← 按日期+版本号（同一天迭代时递增 v2, v3...）
            ├── testcases.md      ← 测试用例主文档（必须）
            ├── metadata.json     ← 生成元数据（必须）
            └── testcases.xmind   ← 脑图（仅用户要求时）
```

**路径示例：**

```text
outputs/2026-04/order-submit/20260418_v1/testcases.md
outputs/2026-04/order-submit/20260418_v1/metadata.json
outputs/2026-04/order-submit/20260418_v1/testcases.xmind
```

**版本迭代规则：**

- 当天第一次生成：`20260418_v1`
- 同一天修改重新生成：`20260418_v2`、`20260418_v3`...
- 不同日期重新生成：新建日期目录，如 `20260420_v1`

### 最低要求

- 必须产出 `testcases.md`
- 必须产出 `metadata.json`（与 `testcases.md` 同目录）
- 用户明确要求"XMind/脑图"时，额外产出 `testcases.xmind`
- 若只要求 XMind，也要先生成 Markdown 再转换
- 回复中必须列出所有产出文件的完整路径
