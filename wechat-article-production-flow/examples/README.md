# Examples 索引

本目录是公众号文章生产流程的**产物对照库**。每个子目录对应一个阶段的产物，存放 1 份完整的 demo（按"按阶段分目录、各一例"原则）。

## 子目录用途

| 目录 | 阶段 | 用途 |
|------|------|------|
| `source/` | Phase 0 输入 | 喂给 agent 的"原始主题输入"，让 agent 从这一份输入开始完整跑三阶段 |
| `plan/` | Phase 1 产物 | 7 项选题分析 + 7 项文章策划，展示"达标"的判别 |
| `visuals/` | Phase 2 产物 | 封面 + 6 张正文配图 Prompt（中英双语）完整产物 |
| `published/` | Phase 3 产物 | 最终 `.html` 交付物，可在 Chrome/Edge 打开并复制到公众号后台 |

## 主题一致性

4 份 demo 围绕**同一主题**展开，方便跨阶段对比：

> **AI 不会淘汰测试工程师，但会改变测试工程师值钱的方式**

这个主题在三类方向里横跨"AI 落地手记"和"质量内功"两个候选栏目，最终选"质量内功"。

## 已知缺陷（不要照抄）

每份 demo 都标注了"已知缺陷"段，目的是让学习者**知道可以学什么、不能照搬什么**：

- `source/ai-testing-engineer-survival.md`：故意只给"主题 + 一句话方向"，**不**给栏目、不给旧文库。模拟"用户信息不全"的真实场景。
- `plan/ai-testing-engineer-survival-plan.md`：7 项选题中的"与旧文重复风险"标注"未提供历史文章库，基于常见公众号选题进行推断" — 这是 writing-topic-selection.md 兜底策略的范例。**不是**虚构旧文。
- `visuals/ai-testing-engineer-survival-prompts.md`：封面与 6 张正文图都严格遵守 design token。Prompt 中的"白底"必须出现，不接受"简洁背景"等模糊描述。
- `published/ai-will-not-replace-test-engineers.html`：来自实际抓取的真实公众号文章，**不**是本 skill 产出的"完美样本"。它告诉你"公众号后台排版长什么样"，但工具栏代码不一定符合 snippets/toolbar.html 的最新规范（抓取自旧版，工具栏可能不完整或结构不同）。

## demo-1.html 与 demo-2.html

这两份是早期抓取的样本，分别对应：

- `demo-1.html`：用 WeChat 抓取工具从公众号后台"读"出来的结构（含 `id="js_content"` 等 WeChat 专属类名）
- `demo-2.html`：用其他工具抓取的另一版结构

它们的**结构与 toolbar 不一定符合本 skill 的规范**。`published/` 目录收录它们是为了：

1. 让学习者看到"真实公众号后台"与"本 skill 产出"在 inline style 上的差异
2. 作为`visuals-output-format.md`反面案例 — 真实公众号文章里的"花哨 SVG / 渐变背景 / 多层嵌套"在 skill 输出里**不要**照搬

**不要把 demo-1.html / demo-2.html 当作"标准交付物"参考。标准交付物看 `ai-will-not-replace-test-engineers.html`（注意：这是抓取版，工具栏仍可参考）以及按 snippets/toolbar.html 新生成的产物。**

## 跨阶段查看顺序

```
source/  →  plan/  →  visuals/  →  published/
   ↑          ↑           ↑             ↑
 输入       选题策划     配图 Prompt    最终 .html
```

每个目录的 demo 都按"喂给下一阶段"的形式组织：
- `source/` 输出作为 `plan/` 的输入
- `plan/` 输出的"6 个核心章节名"作为 `visuals/` 的输入
- `visuals/` 输出的"封面图 + 6 张正文图"作为 `published/` 的图片占位块参考
