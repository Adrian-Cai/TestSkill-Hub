# TestSkill-Hub

测试技能中心，面向测试人员、测试开发、质量工程师的 AI Agent Skill 仓库。

本仓库为测试相关技能集合，聚焦需求评审、测试设计、接口测试、Bug 整理、回归分析、浏览器验证、测试报告和测试驱动开发等高频质量工作。

## 保留技能

| 技能 | 功能描述 | 适用场景 |
| --- | --- | --- |
| [ai-requirement-review-test-design](./ai-requirement-review-test-design/) | 根据需求文档、用户故事或业务流程提取规则、风险、测试点矩阵和功能测试模板 | 需求评审、测试分析、用例设计前 |
| [prd-to-testcase](./prd-to-testcase/) | 根据需求文档、接口文档、页面说明、代码 Diff、配置变更等生成测试分析和测试用例 | 迭代开始前、需求变更后、测试设计阶段 |
| [api-test-gen](./api-test-gen/) | 根据 Swagger、YAPI、RAP 或文本接口说明生成接口测试用例 | 接口评审、联调前后、接口回归 |
| [bug-report-writer](./bug-report-writer/) | 根据缺陷现象生成规范 Bug 单，包含复现步骤、严重等级、优先级、环境信息和日志摘要 | 测试执行、缺陷提交、缺陷复盘 |
| [regression-scope](./regression-scope/) | 根据需求变更、代码改动或 Bug 修复内容分析回归范围和优先级 | 版本回归、补丁发布、风险评估 |
| [test-report-writer](./test-report-writer/) | 根据用例通过率、Bug 列表和遗留问题生成测试报告、质量评估和上线建议 | 提测结束、发布评审、上线前总结 |
| [browser-testing-with-devtools](./browser-testing-with-devtools/) | 在真实浏览器中验证页面、DOM、控制台错误、网络请求和运行时表现 | Web 页面测试、前端缺陷定位、可视化验收 |
| [test-driven-development](./test-driven-development/) | 使用测试驱动开发方式复现 Bug、编写失败测试、实现修复并验证通过 | 修改逻辑、修复 Bug、补齐自动化测试 |
| [ai-test-training-ppt-designer](./ai-test-training-ppt-designer/) | 设计 AI 软件测试内训课程章节、PPT 结构、讲师稿和课堂互动 | 测试团队培训、AI 测试课程建设 |

## 如何使用

所有 Skill 均通过 AI Agent 触发，无需手动执行脚本。

1. 打开 AI Agent 对话，并切换到本仓库工作目录。
2. 用自然语言描述你的测试任务。
3. Agent 会根据任务读取对应目录下的 `SKILL.md` 和必要规则文件。
4. 需要落地的产物会写入对应技能的 `outputs/` 目录。

## 快速触发示例

生成需求测试点：

```text
根据这份需求文档做需求评审，提取业务规则、风险清单和测试点矩阵：<需求内容>
```

生成测试用例：

```text
根据这份 PRD 生成测试用例，并输出 Markdown 文件：<需求内容>
```

生成接口测试用例：

```text
根据这份 Swagger 文档生成接口测试用例：<接口文档内容>
```

整理 Bug 单：

```text
帮我把这个缺陷整理成规范 Bug 单：<现象、步骤、环境、日志>
```

分析回归范围：

```text
这次修改了登录 Token 刷新逻辑，帮我分析回归测试范围和优先级
```

生成测试报告：

```text
帮我生成测试报告：执行 200 条用例，通过 185 条，发现 15 个 Bug，遗留 3 个 P2
```

进行浏览器验证：

```text
帮我在真实浏览器里检查这个页面的控制台错误、网络请求和关键交互：<页面地址>
```

按 TDD 修复问题：

```text
这个函数在空输入时会报错，请先写失败测试复现，再修复并验证通过
```

## 如何下载单个技能

推荐使用 Git Sparse Checkout 只拉取需要的技能目录：

```bash
git clone --filter=blob:none --no-checkout https://github.com/Adrian-Cai/TestSkill-Hub.git
cd TestSkill-Hub
git sparse-checkout init --cone
git sparse-checkout set bug-report-writer
git checkout main
```

如果只想手动下载，也可以在 GitHub 页面进入目标技能目录，使用 `Code` -> `Download ZIP` 下载后仅保留需要的目录。

## 验证 Skill 效果

验证一个 Skill 是否可用时，重点看三件事：

- Agent 是否按 `SKILL.md` 中定义的工作流执行。
- 是否在 `outputs/` 目录生成实际文件，而不是只在对话中回答。
- 产物是否符合测试团队可评审、可执行、可追踪的标准。

常见产物目录：

```text
ai-requirement-review-test-design/outputs/reviews/
prd-to-testcase/outputs/testcases/
api-test-gen/outputs/testcases/
bug-report-writer/outputs/reports/
regression-scope/outputs/analysis/
test-report-writer/outputs/reports/
```

## 目录结构

每个 Skill 通常遵循以下结构：

```text
<skill-name>/
├── SKILL.md
├── rules/
│   ├── _sections.md
│   └── *.md
├── agents/
│   └── openai.yaml
└── outputs/
```

其中 `SKILL.md` 是 Agent 入口文件，`rules/` 存放专项规则，`outputs/` 用于保存执行产物。
