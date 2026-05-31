---
name: 文档与决策记录
description: 记录决策和文档。适用于做出架构决策、更改公共 API、发布功能或需要记录未来工程师和 agent 需要理解代码库的上下文时。
---

# 文档与决策记录

## 概述

记录决策，而不仅仅是代码。最有价值的文档捕获*为什么*——导致决策的上下文、约束和权衡。代码显示*构建了什么*；文档解释*为什么这样构建*以及*考虑了哪些替代方案*。这个上下文对于在代码库中工作的未来人类和 agent 至关重要。

## 何时使用

- 做出重大架构决策
- 在竞争方法之间选择
- 添加或更改公共 API
- 发布更改用户面向行为的功能
- 引导新团队成员（或 agent）加入项目
- 当你发现自己在重复解释同一件事时

**何时不使用：** 不要记录显而易见的代码。不要添加重述代码已说明内容的注释。不要为一次性原型编写文档。

## 架构决策记录 (ADR)

ADR 捕获重大技术决策背后的推理。它们是你能编写的最高价值文档。

### 何时编写 ADR

- 选择框架、库或主要依赖
- 设计数据模型或数据库模式
- 选择认证策略
- 决定 API 架构（REST vs. GraphQL vs. tRPC）
- 在构建工具、托管平台或基础设施之间选择
- 任何代价高昂的逆转决策

### ADR 模板

将 ADR 存储在 `docs/decisions/` 中，使用顺序编号：

```markdown
# ADR-001：使用 PostgreSQL 作为主数据库

## 状态
已接受 | 被 ADR-XXX 取代 | 已弃用

## 日期
2025-01-15

## 上下文
我们需要一个任务管理应用程序的主数据库。关键要求：
- 关系数据模型（用户、任务、具有关系的团队）
- 任务状态更改的 ACID 事务
- 支持任务内容的全文搜索
- 可用的托管托管（对于小团队，有限的运维能力）

## 决策
使用 PostgreSQL 和 Prisma ORM。

## 考虑的替代方案

### MongoDB
- 优点：灵活的模式，易于开始
- 缺点：我们的数据本质上是关系型的；需要手动管理关系
- 拒绝：文档存储中的关系数据导致复杂的连接或数据重复

### SQLite
- 优点：零配置，嵌入式，读取快
- 缺点：有限的并发写入支持，生产没有托管托管
- 拒绝：不适合生产中的多用户 Web 应用程序

### MySQL
- 优点：成熟，广泛支持
- 缺点：PostgreSQL 具有更好的 JSON 支持、全文搜索和生态系统工具
- 拒绝：PostgreSQL 更适合我们的功能要求

## 后果
- Prisma 提供类型安全的数据库访问和迁移管理
- 我们可以使用 PostgreSQL 的全文搜索而不是添加 Elasticsearch
- 团队需要 PostgreSQL 知识（标准技能，低风险）
- 托管服务托管（Supabase、Neon 或 RDS）
```

### ADR 生命周期

```
提议 → 接受 → （取代或弃用）
```

- **不要删除旧 ADR。** 它们捕获历史上下文。
- 当决策更改时，编写一个新的 ADR，引用并取代旧的。

## 内联文档

### 何时注释

注释*为什么*，而不是*什么*：

```typescript
// 坏：重述代码
// 计数器加 1
counter += 1;

// 好：解释非显而易见的意图
// 速率限制使用滑动窗口——在窗口边界重置计数器，
// 而不是在固定时间表上，以防止窗口边缘的突发攻击
if (now - windowStart > WINDOW_SIZE_MS) {
  counter = 0;
  windowStart = now;
}
```

### 何时不注释

```typescript
// 不要注释自解释的代码
function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// 不要为应该现在做的事情留 TODO 注释
// TODO：添加错误处理  ← 直接添加

// 不要留注释掉的代码
// const oldImplementation = () => { ... }  ← 删除它，git 有历史
```

### 记录已知陷阱

```typescript
/**
 * 重要：此函数必须在第一次渲染之前调用。
 * 如果在水合后调用，它会导致无样式内容闪烁，
 * 因为主题上下文在 SSR 期间不可用。
 *
 * 有关完整设计原理，请参阅 ADR-003。
 */
export function initializeTheme(theme: Theme): void {
  // ...
}
```

## API 文档

对于公共 API（REST、GraphQL、库接口）：

### 带类型的内联（TypeScript 首选）

```typescript
/**
 * 创建新任务。
 *
 * @param input - 任务创建数据（标题必填，描述可选）
 * @returns 创建的任务，包含服务器生成的 ID 和时间戳
 * @throws {ValidationError} 如果标题为空或超过 200 个字符
 * @throws {AuthenticationError} 如果用户未认证
 *
 * @example
 * const task = await createTask({ title: '购买杂货' });
 * console.log(task.id); // "task_abc123"
 */
export async function createTask(input: CreateTaskInput): Promise<Task> {
  // ...
}
```

### REST API 的 OpenAPI / Swagger

```yaml
paths:
  /api/tasks:
    post:
      summary: 创建任务
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateTaskInput'
      responses:
        '201':
          description: 任务已创建
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '422':
          description: 验证错误
```

## README 结构

每个项目都应该有一个涵盖以下内容的 README：

```markdown
# 项目名称

项目功能的单段描述。

## 快速开始
1. 克隆仓库
2. 安装依赖：`npm install`
3. 设置环境：`cp .env.example .env`
4. 运行开发服务器：`npm run dev`

## 命令
| 命令 | 描述 |
|------|------|
| `npm run dev` | 启动开发服务器 |
| `npm test` | 运行测试 |
| `npm run build` | 生产构建 |
| `npm run lint` | 运行 linter |

## 架构
项目结构和关键设计决策的简要概述。
链接到 ADR 获取详细信息。

## 贡献
如何贡献、编码标准、PR 流程。
```

## 变更日志维护

对于已发布功能：

```markdown
# 变更日志

## [1.2.0] - 2025-01-20
### 添加
- 任务共享：用户可以与团队成员共享任务 (#123)
- 任务分配的电子邮件通知 (#124)

### 修复
- 快速点击创建按钮时出现重复任务 (#125)

### 更改
- 任务列表现在每页加载 50 个项目（之前是 20）以获得更好的 UX (#126)
```

## Agent 的文档

对 AI agent 上下文的特殊考虑：

- **CLAUDE.md / 规则文件** — 记录项目约定以便 agent 遵循
- **规范文件** — 保持规范更新以便 agent 构建正确的内容
- **ADR** — 帮助 agent 理解过去决策的原因（防止重新决策）
- **内联陷阱** — 防止 agent 陷入已知陷阱

## 常见误解

| 误解 | 现实 |
|------|------|
| "代码是自文档化的" | 代码显示什么。它不显示为什么、哪些替代方案被拒绝或哪些约束适用。 |
| "我们会在 API 稳定后编写文档" | 当你记录它们时，API 更快稳定。文档是设计的第一次测试。 |
| "没人读文档" | Agent 会。未来的工程师会。你 3 个月后的自己会。 |
| "ADR 是开销" | 10 分钟的 ADR 防止六个月后关于相同决策的 2 小时辩论。 |
| "注释会过时" | 关于*为什么*的注释是稳定的。关于*什么*的注释会过时——这就是为什么你只编写前者。 |

## 红旗

- 没有书面理由的架构决策
- 没有文档或类型的公共 API
- README 不解释如何运行项目
- 注释掉的代码而不是删除
- 存在数周的 TODO 注释
- 具有重大架构选择的项目中没有 ADR
- 重述代码而不是解释意图的文档

## 验证

记录后：

- [ ] 所有重大架构决策都有 ADR
- [ ] README 涵盖快速开始、命令和架构概述
- [ ] API 函数有参数和返回类型文档
- [ ] 已知陷阱在相关地方内联记录
- [ ] 没有注释掉的代码残留
- [ ] 规则文件（CLAUDE.md 等）是最新的且准确的
