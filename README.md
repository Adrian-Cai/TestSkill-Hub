# TestSkill-Hub
测试技能中心 —— 面向测试人员的 AI Agent Skill 仓库

## 📦 技能列表

### 测试相关技能

| 技能 | 功能描述 | 适用场景 |
| --- | --- | --- |
| [prd-to-testcase](./prd-to-testcase/) | 根据需求文档、接口文档、页面说明、代码 Diff 等生成测试用例和测试分析 | 需求评审后、迭代开始前 |
| [bug-report-writer](./bug-report-writer/) | 根据缺陷现象生成规范 Bug 单，含严重等级/复现步骤/环境信息 | 测试执行过程中 |
| [api-test-gen](./api-test-gen/) | 根据接口文档生成接口测试用例，覆盖正常/异常/鉴权/边界值 | 接口联调前后 |
| [test-report-writer](./test-report-writer/) | 根据测试结果生成测试报告，含质量评估和上线建议 | 版本发布前 |
| [regression-scope](./regression-scope/) | 根据变更内容分析回归范围，输出带优先级的回归测试矩阵 | Bug 修复/需求变更后 |
| [browser-testing-with-devtools](./browser-testing-with-devtools/) | 在真实浏览器中测试，通过 Chrome DevTools MCP 验证 DOM、控制台错误、网络请求 | 构建或调试浏览器内容时 |

### 开发流程技能

| 技能 | 功能描述 | 适用场景 |
| --- | --- | --- |
| [spec-driven-development](./spec-driven-development/) | 在编码前创建规格说明，适用于新项目、新功能或重大变更 | 需求模糊或不完整时 |
| [planning-and-task-breakdown](./planning-and-task-breakdown/) | 将工作拆解为有序任务，适用于有规格说明需要拆分为可实现单元时 | 任务太大或太模糊时 |
| [incremental-implementation](./incremental-implementation/) | 增量交付变更，适用于实现任何多文件变更或大任务拆分 | 实现新功能或重构时 |
| [test-driven-development](./test-driven-development/) | 测试驱动开发，适用于实现任何逻辑、修复任何 bug 或修改现有功能 | 需要证明代码工作时 |
| [idea-refine](./idea-refine/) | 通过结构化的发散和收敛思维迭代精炼想法 | 有模糊想法需要细化时 |

### 代码质量技能

| 技能 | 功能描述 | 适用场景 |
| --- | --- | --- |
| [code-review-and-quality](./code-review-and-quality/) | 多维度代码评审，适用于合并任何变更之前 | 代码评审或合并前 |
| [code-simplification](./code-simplification/) | 简化代码以提高清晰度，适用于重构代码以提高可读性 | 代码可读性或复杂度问题时 |
| [debugging-and-error-recovery](./debugging-and-error-recovery/) | 系统化根本原因调试，适用于测试失败、构建中断或行为不符预期时 | 遇到任何 bug 或错误时 |

### 架构与设计技能

| 技能 | 功能描述 | 适用场景 |
| --- | --- | --- |
| [api-and-interface-design](./api-and-interface-design/) | 指导稳定的 API 和接口设计，适用于设计 API、模块边界或任何公共接口 | 设计新 API 端点或组件接口时 |
| [frontend-ui-engineering](./frontend-ui-engineering/) | 构建生产级 UI，适用于构建或修改面向用户的界面 | 构建新 UI 组件或页面时 |
| [context-engineering](./context-engineering/) | 优化 Agent 上下文设置，适用于开始新会话或 Agent 输出质量下降时 | 开始新会话或切换任务时 |
| [security-and-hardening](./security-and-hardening/) | 加固代码以防止漏洞，适用于处理用户输入、认证、数据存储或外部集成时 | 构建接受不可信数据的功能时 |

### 发布与运维技能

| 技能 | 功能描述 | 适用场景 |
| --- | --- | --- |
| [ci-cd-and-automation](./ci-cd-and-automation/) | 自动化 CI/CD 流水线设置，适用于设置或修改构建和部署流水线 | 设置新项目的 CI 流水线时 |
| [git-workflow-and-versioning](./git-workflow-and-versioning/) | 结构化 git 工作流实践，适用于提交、分支、解决冲突或组织工作时 | 所有代码变更场景 |
| [shipping-and-launch](./shipping-and-launch/) | 准备生产发布，适用于准备部署到生产环境时 | 首次部署功能到生产环境时 |
| [performance-optimization](./performance-optimization/) | 优化应用性能，适用于性能要求存在或怀疑性能回归时 | 性能问题或 Core Web Vitals 不达标时 |

### 维护与文档技能

| 技能 | 功能描述 | 适用场景 |
| --- | --- | --- |
| [deprecation-and-migration](./deprecation-and-migration/) | 管理废弃和迁移，适用于移除旧系统、API 或功能时 | 用新系统替换旧系统时 |
| [documentation-and-adrs](./documentation-and-adrs/) | 记录决策和文档，适用于做出架构决策或更改公共 API 时 | 做出重大架构决策时 |
| [using-agent-skills](./using-agent-skills/) | 发现并调用 Agent 技能，适用于会话开始时或需要判断使用哪个技能时 | 会话开始时 |

---

## ⬇️ 如何下载单个技能

### 方法一：Git Sparse Checkout（推荐）

```bash
# 1. 克隆仓库（只下载 .git 目录，不下载文件）
git clone --filter=blob:none --no-checkout https://github.com/your-repo/TestSkill-Hub.git
cd TestSkill-Hub

# 2. 启用 sparse checkout
git sparse-checkout init --cone

# 3. 只检出你需要的技能目录（例如 bug-report-writer）
git sparse-checkout set bug-report-writer

# 4. 切换到 main 分支
git checkout main
```

### 方法二：SVN Export（无需 Git）

```bash
# 如果安装了 SVN，可以直接导出单个目录
svn export https://github.com/your-repo/TestSkill-Hub/trunk/bug-report-writer
```

### 方法三：手动下载

1. 打开 GitHub 仓库页面
2. 导航到要下载的技能目录（如 `bug-report-writer/`）
3. 点击目录进入
4. 点击右上角 `Code` → `Download ZIP`
5. 解压后只保留需要的技能目录

### 方法四：使用 GitHub API

```bash
# 下载整个仓库的 ZIP，然后只保留需要的目录
curl -L https://github.com/your-repo/TestSkill-Hub/archive/refs/heads/main.zip -o repo.zip
unzip repo.zip
mv TestSkill-Hub-main/bug-report-writer ./bug-report-writer
rm -rf TestSkill-Hub-main repo.zip
```

---

## 🚀 如何使用

所有 Skill 均通过 AI Agent 触发，无需手动执行脚本。

### 使用方式
1. 打开 AI Agent 对话，切换到对应 Skill 所在的工作目录
2. 直接用自然语言描述任务，Agent 会自动读取 `SKILL.md` 并执行
3. 产物文件会自动落地到对应的 `outputs/` 目录下

### 快速触发示例

**生成测试用例：**
```
根据这份需求文档生成测试用例并输出 md 文件：<需求文本或链接>
```

**写 Bug 单：**
```
帮我把这个 Bug 整理成规范的 Bug 单：<现象描述>
```

**生成接口测试用例：**
```
根据这份接口文档生成接口测试用例：<Swagger/YAPI 内容>
```

**生成测试报告：**
```
帮我生成测试报告，执行了 200 条用例，通过 185 条，发现 15 个 Bug，遗留 3 个 P2
```

**分析回归范围：**
```
这次改了用户登录模块的 Token 刷新逻辑，帮我分析回归范围
```

---

## ✅ 如何验证 Skill 效果

### 方法一：用示例输入快速验证

每个 Skill 的 `SKILL.md` 末尾都有「快速触发示例」，直接复制示例 prompt 发给 Agent 即可触发。

验证标准：
- Agent 是否按照工作流步骤执行（可观察对话过程）
- 是否在 `outputs/` 目录下生成了实际文件（**必须落地文件，不能只在对话中输出**）
- 产物内容是否符合对应的输出模板格式

### 方法二：用真实业务数据验证

用当前正在进行的真实项目数据触发 Skill，对比产物与人工产出的质量差距：

| Skill | 验证方法 | 验收标准 |
| --- | --- | --- |
| `prd-to-testcase` | 输入一份真实需求文档 | 用例覆盖功能/边界/异常，有文件落地 |
| `bug-report-writer` | 输入一个正在测的真实 Bug | 标题格式规范，步骤可独立复现，等级准确 |
| `api-test-gen` | 输入一个真实接口定义 | 每个接口有正常+异常+鉴权用例，有文件落地 |
| `test-report-writer` | 输入最近一次版本的测试数据 | 通过率计算正确，上线建议有数据支撑 |
| `regression-scope` | 输入最近一次 Bug 修复列表 | 回归矩阵有优先级分级，影响分析有依据 |
| `spec-driven-development` | 输入一个模糊的功能想法 | 输出清晰的规格说明文档 |
| `planning-and-task-breakdown` | 输入一个规格说明 | 输出有序的任务列表 |
| `test-driven-development` | 输入一个 bug 描述 | 先写测试再修复，测试通过 |
| `code-review-and-quality` | 输入一段代码变更 | 输出多维度评审意见 |
| `debugging-and-error-recovery` | 输入一个错误信息 | 系统化定位并修复根本原因 |

### 方法三：检查产物文件

Skill 执行完毕后，检查以下目录是否有新文件生成：

```
prd-to-testcase/outputs/testcases/
bug-report-writer/outputs/reports/
api-test-gen/outputs/testcases/
test-report-writer/outputs/reports/
regression-scope/outputs/analysis/
spec-driven-development/outputs/specs/
planning-and-task-breakdown/outputs/plans/
```

---

## 📁 目录结构说明

每个 Skill 遵循统一目录规范：

```
<skill-name>/
├── SKILL.md              # 技能定义文件（Agent 入口，必读）
├── rules/                # 规则文件目录
│   ├── _sections.md      # 规则索引（说明何时读哪个规则）
│   └── *.md              # 各专项规则
└── outputs/              # 产物落地目录（自动生成，无需手动操作）
```
