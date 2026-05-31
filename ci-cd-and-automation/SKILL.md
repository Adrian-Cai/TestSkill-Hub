---
name: CI/CD与自动化
description: 自动化 CI/CD 流水线设置。适用于设置或修改构建和部署流水线。适用于需要自动化质量门禁、在 CI 中配置测试运行器或建立部署策略时。
---

# CI/CD与自动化

## 概述

自动化质量门禁，使没有变更能在未经测试、lint、类型检查和构建的情况下到达生产。CI/CD 是每个其他技能的执行机制——它捕获人类和 agent 遗漏的东西，并且它在每个单一变更上一致地执行。

**左移：** 尽早在流水线中捕获问题。在 lint 中捕获的 bug 成本分钟；在生产中捕获的相同 bug 成本小时。将检查上移——测试前静态分析，staging 前测试，生产前 staging。

**更快更安全：** 更小的批次和更频繁的发布降低风险，而不是增加风险。有 3 个变更的部署比有 30 个变更的更容易调试。频繁的发布建立对发布过程本身的信心。

## 何时使用

- 设置新项目的 CI 流水线
- 添加或修改自动化检查
- 配置部署流水线
- 当变更应触发自动化验证时
- 调试 CI 失败

## 质量门禁流水线

每个变更在合并前都经过这些门禁：

```
拉取请求打开
    │
    ▼
┌─────────────────┐
│   LINT 检查      │  eslint, prettier
│   ↓ 通过         │
│   类型检查       │  tsc --noEmit
│   ↓ 通过         │
│   单元测试       │  jest/vitest
│   ↓ 通过         │
│   构建           │  npm run build
│   ↓ 通过         │
│   集成测试       │  API/DB 测试
│   ↓ 通过         │
│   E2E（可选）    │  Playwright/Cypress
│   ↓ 通过         │
│   安全审计       │  npm audit
│   ↓ 通过         │
│   包大小         │  bundlesize 检查
└─────────────────┘
    │
    ▼
  准备审查
```

**任何门禁都不能跳过。** 如果 lint 失败，修复 lint——不要禁用规则。如果测试失败，修复代码——不要跳过测试。

## GitHub Actions 配置

### 基本 CI 流水线

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: 安装依赖
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: 类型检查
        run: npx tsc --noEmit

      - name: 测试
        run: npm test -- --coverage

      - name: 构建
        run: npm run build

      - name: 安全审计
        run: npm audit --audit-level=high
```

### 带数据库集成测试

```yaml
  integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: ci_user
          POSTGRES_PASSWORD: ${{ secrets.CI_DB_PASSWORD }}
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - name: 运行迁移
        run: npx prisma migrate deploy
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
      - name: 集成测试
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
```

> **注意：** 即使对于仅 CI 的测试数据库，也使用 GitHub Secrets 存储凭据，而不是硬编码值。这建立了良好的习惯，并防止在其他上下文中意外重用测试凭据。

### E2E 测试

```yaml
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - name: 安装 Playwright
        run: npx playwright install --with-deps chromium
      - name: 构建
        run: npm run build
      - name: 运行 E2E 测试
        run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

## 将 CI 失败反馈给 Agent

CI 与 AI agent 结合的力量是反馈循环。当 CI 失败时：

```
CI 失败
    │
    ▼
复制失败输出
    │
    ▼
反馈给 agent：
"CI 流水线因以下错误失败：
[粘贴具体错误]
修复问题并在再次推送前本地验证。"
    │
    ▼
Agent 修复 → 推送 → CI 再次运行
```

**关键模式：**

```
Lint 失败 → Agent 运行 `npm run lint --fix` 并提交
类型错误 → Agent 读取错误位置并修复类型
测试失败 → Agent 遵循调试与错误恢复技能
构建错误 → Agent 检查配置和依赖
```

## 部署策略

### 预览部署

每个 PR 都获得预览部署用于手动测试：

```yaml
# 在 PR 上部署预览（Vercel/Netlify/等）
deploy-preview:
  runs-on: ubuntu-latest
  if: github.event_name == 'pull_request'
  steps:
    - uses: actions/checkout@v4
    - name: 部署预览
      run: npx vercel --token=${{ secrets.VERCEL_TOKEN }}
```

### 特性标志

特性标志将部署与发布解耦。在标志后部署未完成或有风险的功能，这样你可以：

- **发布代码而不启用它。** 尽早合并到 main，准备就绪时启用。
- **无需重新部署即可回滚。** 禁用标志而不是回滚代码。
- **金丝雀新功能。** 为 1% 的用户启用，然后 10%，然后 100%。
- **运行 A/B 测试。** 比较有和没有功能的行为。

```typescript
// 简单的特性标志模式
if (featureFlags.isEnabled('new-checkout-flow', { userId })) {
  return renderNewCheckout();
}
return renderLegacyCheckout();
```

**标志生命周期：** 创建 → 为测试启用 → 金丝雀 → 全面推出 → 移除标志和死代码。永远存在的标志会成为技术债务——创建时设置清理日期。

### 分阶段推出

```
PR 合并到 main
    │
    ▼
  Staging 部署（自动）
    │ 手动验证
    ▼
  生产部署（手动触发或 staging 后自动）
    │
    ▼
  监控错误（15 分钟窗口）
    │
    ├── 检测到错误 → 回滚
    └── 干净 → 完成
```

### 回滚计划

每次部署在发生之前都需要回滚计划：

```yaml
# 手动回滚工作流
name: 回滚
on:
  workflow_dispatch:
    inputs:
      version:
        description: '要回滚到的版本'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - name: 回滚部署
        run: |
          # 部署指定的先前版本
          npx vercel rollback ${{ inputs.version }}
```

## 环境管理

```
.env.example       → 已提交（开发人员模板）
.env                → 未提交（本地开发）
.env.test           → 已提交（测试环境，无真实机密）
CI 机密            → 存储在 GitHub Secrets / vault 中
生产机密           → 存储在部署平台 / vault 中
```

CI 永远不应有生产机密。为 CI 测试使用单独的机密。

## CI 之外的自动化

### Dependabot / Renovate

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
    open-pull-requests-limit: 5
```

### 构建值班角色

指定某人负责保持 CI 绿色。当构建中断时，构建值班的工作是修复或回滚——而不是导致中断的人。这防止中断构建累积，而每个人都认为别人会修复它。

### PR 检查

- **必需审查：** 合并前至少 1 个批准
- **必需状态检查：** 合并前 CI 必须通过
- **分支保护：** 不允许强制推送到 main
- **自动合并：** 如果所有检查通过并批准，自动合并

## CI 优化

当流水线超过 10 分钟时，按影响顺序应用这些策略：

```
CI 流水线慢？
├── 缓存依赖
│   └── 使用 actions/cache 或 setup-node 缓存选项用于 node_modules
├── 并行运行作业
│   └── 将 lint、类型检查、测试、构建拆分为单独的并行作业
├── 只运行更改的内容
│   └── 使用路径过滤器跳过不相关的作业（例如，仅文档 PR 跳过 e2e）
├── 使用矩阵构建
│   └── 跨多个运行器分片测试套件
├── 优化测试套件
│   └── 从关键路径移除慢测试，改为按计划运行
└── 使用更大的运行器
    └── GitHub 托管的更大运行器或 CPU 密集型构建的自托管
```

**示例：缓存和并行**
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npx tsc --noEmit

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm test -- --coverage
```

## 常见误解

| 误解 | 现实 |
|------|------|
| "CI 太慢" | 优化流水线（见下方 CI 优化），不要跳过它。5 分钟的流水线防止数小时的调试。 |
| "这个变更微不足道，跳过 CI" | 微不足道的变更会破坏构建。CI 对于微不足道的变更是快速的。 |
| "测试不稳定，重新运行" | 不稳定测试掩盖真实 bug 并浪费每个人的时间。修复不稳定性。 |
| "我们稍后添加 CI" | 没有 CI 的项目会累积中断状态。在第一天设置它。 |
| "手动测试足够" | 手动测试不可扩展且不可重复。自动化你能自动化的东西。 |

## 红旗

- 项目中没有 CI 流水线
- CI 失败被忽略或静音
- CI 中禁用测试以使流水线通过
- 生产部署没有 staging 验证
- 没有回滚机制
- 机密存储在代码或 CI 配置文件中（不在机密管理器中）
- 长时间 CI 而没有优化努力

## 验证

设置或修改 CI 后：

- [ ] 所有质量门禁都存在（lint、类型、测试、构建、审计）
- [ ] 流水线在每个 PR 和推送到 main 时运行
- [ ] 失败阻止合并（配置了分支保护）
- [ ] CI 结果反馈到开发循环
- [ ] 机密存储在机密管理器中，而不是代码中
- [ ] 部署有回滚机制
- [ ] 流水线在测试套件的 10 分钟内运行
