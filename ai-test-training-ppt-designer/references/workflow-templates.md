# AI测试内训课件设计工作流模板

Use this reference when the user asks for structured outputs, slide plans, instructor scripts, or PPT files.

## 1. Chapter Design Output

Use this structure:

```markdown
# 课程章节设计：<chapter name>

## 1. 章节定位

### 本章在整门课程中的作用
...

### 承接上一章什么内容
...

### 引出下一章什么内容
...

## 2. 本章核心问题
Use testing practitioners' language. Avoid generic AI wording.

## 3. 本章核心方法
### 方法一：<action>
- 输入：
- AI处理：
- 人工审查：
- 最终产出：

## 4. 推荐课堂案例
- 推荐选择：
- 选择理由：

## 5. 课堂训练动作
3-5 actions only.

## 6. 本章交付物
Only list chapter-related templates, checklists, matrices, and examples.
```

For learner-facing handouts or post-class resources, also read `deliverables-checklist.md`.

## 2. PPT Blueprint Output

Use a table with these fields when requested:

| 页码 | 页标题 | 本页核心观点 | 页面主要内容，控制3-5点 | 推荐页面类型 | 建议讲解时间 | 与上一页/下一页的逻辑关系 |
|---|---|---|---|---|---|---|

Rules:

- Use 6-7 pages for a 15-minute module unless the user asks otherwise.
- Make every title a consulting-style claim, not a topic label.
- One core point per page.
- Arrange pages according to the testing workflow.
- Show the loop: requirement input -> AI processing -> human review -> testing output.

## 3. Detailed Slide Design Output

For each page, include:

1. 页标题
2. 本页核心观点
3. PPT页面文案
4. 推荐版式
5. 视觉风格建议
6. 讲师口述重点
7. 本页建议讲解时间
8. 与下一页衔接话术

Slide copy rules:

- 3-5 points per slide.
- Use short, audience-facing phrases.
- Do not paste full speaker notes into slide copy.
- Use concrete testing terms: demand rules, boundary values, status transition, permissions, test point matrix, risk layering, manual review, case optimization.

## 4. Instructor Script Output

For a 15-minute chapter:

- Write a 12-15 minute complete script by slide order.
- Use enterprise internal training tone.
- Keep transitions natural.
- Use one testing case throughout the chapter.
- Include only one interaction unless requested otherwise.

Interaction block:

```markdown
## 课堂互动设计

- 互动问题位置：
- 互动问题：
- 互动时间：
- 学员可能回答：
- 讲师如何接住回答：
- 收回话术：
- 如何过渡到下一部分：
```

Control block:

```markdown
## 授课控制建议

- 哪些内容不要展开太多：
- 哪些地方必须强调：
- 哪些话术能增强学员共鸣：
- 如何避免讲得太虚：
- 如何控制在目标时长内：
- 哪些内容适合后面章节再展开：
```

## 5. Recommended 7-Page Flow For Requirement Review Modules

Use this pattern for "AI辅助需求评审与测试点设计" or similar chapters:

1. Demand review is the easiest AI entry point for testing value.
2. Testers must convert vague requirement text into verifiable questions.
3. AI must work inside a controlled loop, not one-click generation.
4. AI structures requirements and rules; testers check whether it understood correctly.
5. A test point matrix converts rules into scenarios; it is not an AI final answer.
6. High-value review exposes requirement questions and risks early.
7. Classroom practice turns AI usage into a reusable review method.

## 6. PPT Visual Quality Gate

For final PPT files:

- Use 4:3 ratio when requested.
- Keep the deck editable with native text, shapes, tables, arrows, and cards.
- Prefer low-saturation blue-gray, warm gray, muted green, and restrained risk colors.
- Use white or near-white backgrounds with gentle gradients.
- Use thin borders, soft shadows, and generous margins.
- Use matrices, process diagrams, risk grids, and deliverable cards.
- Avoid robots, brains, circuit boards, neon lighting, 3D cartoon characters, and decorative AI clichés.
- Render the deck and inspect page images before delivery.
- Fix overflow, clipping, line breaks, overlap, and over-dense pages.

## 7. Common Wording Anchors

Use these phrases when they fit:

- 测试不是把需求读完，而是把需求变成可验证的问题。
- AI输出是初稿，不是最终测试方案。
- AI帮助测试人员想得更快更多，但不能替代业务判断和风险判断。
- 真正有价值的是“AI生成 + 测试人员审查 + 团队确认”的闭环。
- 测试点数量多不代表质量高，能提前暴露风险才有价值。
