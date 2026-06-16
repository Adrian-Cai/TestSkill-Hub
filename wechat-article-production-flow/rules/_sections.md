# 规则索引

本技能按三个生产阶段组织规则文件，每个阶段都有可验证的产物。

## Phase 1 · 内容写作 → 产物：2500-3500 字 Markdown 正文

| 规则 | 解决什么 | 何时读 |
|------|---------|--------|
| `writing-style-baseline.md` | 唯一风格基线、语气、绝对禁忌 | 必读基线 |
| `writing-constraints.md` | 字数、标题数、阅读节奏、信息密度 | 必读基线 |
| `writing-topic-selection.md` | 选题判断的 7 项输出 | Step 1 |
| `writing-article-planning.md` | 文章策划的 7 项输出 | Step 2 |
| `writing-full-draft.md` | 正文成稿的结构与排版要求 | Step 3 |
| `writing-self-check.md` | 输出前自检清单 | Step 3 末 |

## Phase 2 · 配图 Prompt 生成 → 产物：封面 + 6 张正文配图 Prompt（中英双语）

| 规则 | 解决什么 | 何时读 |
|------|---------|--------|
| `visuals-structure-extraction.md` | 主题识别、6 个核心章节提取 | Step 4 |
| `visuals-cover-prompt.md` | 封面图 Prompt 比例、风格、构图约束 | Step 5 |
| `visuals-body-prompt.md` | 正文 6 张图的视觉规范和风格统一 | Step 6 |
| `visuals-output-format.md` | 最终输出格式，固定标题顺序与中英结构 | Step 6 末 |
| `visuals-prompt-quality.md` | Prompt 用词质量与禁忌项 | Step 5/6 期间 |

## Phase 3 · 富文本 HTML 发布 → 产物：可下载的 `.html` 文件

| 规则 | 解决什么 | 何时读 |
|------|---------|--------|
| `publish-delivery-contract.md` | 最终交付契约与输出限制 | Step 7 前 |
| `publish-response-guardrails.md` | 回复边界、禁令、最终回复形状 | Step 7/9 |
| `publish-html-structure.md` | 页面结构、工具栏、article#wechatArticle | Step 7 |
| `publish-copy-logic.md` | ClipboardItem 和 fallback 复制逻辑契约 | Step 7 |
| `publish-style-rules.md` | inline style、设计 token、组件与兼容性 | Step 7 |
| `publish-article-processing.md` | 文章整理、伪表格、图片占位块 | Step 7 |

## 阶段衔接

- **Phase 1 → Phase 2**：消费 2500-3500 字正文，按 visuals-structure-extraction 抽出 6 个核心章节名
- **Phase 2 → Phase 3**：消费正文 + 配图占位块标记（`此处插入图 N:xxx`），按 publish-article-processing 加工
- **Phase 3 完成后**：按 publish-delivery-contract 的最终回复形状交付

## 外部资源

- 工具栏 + 复制逻辑完整源码：`../snippets/toolbar.html`
- 阶段产物对照示例：`../examples/README.md`
- 压力测试场景：`../tests/pressure-scenarios.md`
