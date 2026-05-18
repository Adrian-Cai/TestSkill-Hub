---
title: XMind 结构与转换
impact: 中低
impactDescription: 统一脑图交付结构与可读性
tags: xmind, mindmap, structure, conversion
---

## XMind 结构与转换

当用户需要脑图交付时，先生成 Markdown，再转换为 XMind。

**推荐命令：**

```bash
python3 scripts/markdown_to_xmind.py --input <md_path> --output <xmind_path> --title "<标题>"
```

**推荐结构：**

```text
<项目/需求名称>
├── 测试策略
├── 冒烟用例
├── 完整测试用例
├── 覆盖与追踪
└── 待确认项
```

### 交付要求

- `.xmind` 与 `.md` 文件放在同一目录，便于追溯
- 文件名使用同一 slug，例如：
  - `outputs/testcases/order-submit.md`
  - `outputs/testcases/order-submit.xmind`
- 会话回复需要同时给出两个路径
