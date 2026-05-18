---
title: 元数据记录规范
impact: 关键
impactDescription: 保证每次生成可追踪、可复现、可评估质量
tags: metadata, traceability, output, version
---

## 元数据记录规范

每次生成测试用例时，必须在输出目录下同步产出 `metadata.json`，记录本次生成的上下文信息。

### 完整结构

```json
{
  "project": "<project-slug>",
  "generated_at": "<ISO8601时间，例如 2026-04-18T14:30:00+08:00>",
  "version": "v1",
  "input_sources": [
    {
      "type": "prd",
      "source": "<文件路径或URL，例如 https://km.xxx.com/doc/12345>"
    },
    {
      "type": "tech_spec",
      "source": "<文件路径或URL，无则省略此项>"
    }
  ],
  "output_stats": {
    "total_testcases": 0,
    "smoke_cases": 0,
    "functional_cases": 0,
    "boundary_cases": 0,
    "exception_cases": 0
  },
  "pending_items": 0,
  "reviewer": "",
  "review_date": ""
}
```

### 字段说明

| 字段 | 类型 | 谁填 | 说明 |
| --- | --- | --- | --- |
| `project` | string | AI 生成 | 需求/项目名，英文小写连字符格式，例如 `order-submit` |
| `generated_at` | ISO8601 | AI 生成 | 生成时间，带时区 |
| `version` | string | AI 生成 | 当前目录版本号，与目录名对应（如 `v1`） |
| `input_sources` | array | AI 生成 | 输入来源列表，`type` 可选 `prd` / `tech_spec` / `knowledge_base` / `examples` |
| `output_stats.*` | int | AI 生成 | 各类用例计数，生成完成后填入实际数字 |
| `pending_items` | int | AI 生成 | 「待确认项」的数量 |
| `reviewer` | string | 人工填写 | 评审人姓名/工号，AI 不填 |
| `review_date` | string | 人工填写 | 评审日期（`YYYY-MM-DD`），AI 不填 |

### 生成时注意

- `output_stats` 中的数字必须与 `testcases.md` 中的用例数量一致，**生成完用例后统计并填入**，不能全填 0。
- `reviewer` 和 `review_date` 留空字符串，由人工评审后补填。
- `input_sources` 如为纯文本输入（无URL），`source` 填写 `"inline-text"`。

### 示例

```json
{
  "project": "order-submit",
  "generated_at": "2026-04-18T14:30:00+08:00",
  "version": "v1",
  "input_sources": [
    {
      "type": "prd",
      "source": "https://km.sankuai.com/doc/98765"
    },
    {
      "type": "tech_spec",
      "source": "inline-text"
    }
  ],
  "output_stats": {
    "total_testcases": 38,
    "smoke_cases": 5,
    "functional_cases": 18,
    "boundary_cases": 10,
    "exception_cases": 5
  },
  "pending_items": 3,
  "reviewer": "",
  "review_date": ""
}
```

**错误（output_stats 全为 0，未统计）：**

```json
"output_stats": {
  "total_testcases": 0,
  "smoke_cases": 0,
  ...
}
```

**正确（生成后统计实际数字填入）：**

```json
"output_stats": {
  "total_testcases": 38,
  "smoke_cases": 5,
  ...
}
```
