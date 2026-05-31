---
name: 性能优化
description: 优化应用性能。适用于存在性能要求、怀疑性能回归或需要改进 Core Web Vitals 或加载时间时。适用于分析发现需要修复的瓶颈时。
---

# 性能优化

## 概述

优化前先度量。没有度量的性能工作是猜测——猜测会导致过早优化，增加复杂度而没有改善真正重要的东西。先分析，识别真正的瓶颈，修复它，再次度量。只优化度量证明重要的东西。

## 何时使用

- 规范中存在性能要求（加载时间预算、响应时间 SLA）
- 用户或监控报告行为缓慢
- Core Web Vitals 分数低于阈值
- 怀疑变更引入了回归
- 构建处理大数据集或高流量的功能

**何时不使用：** 在有证据证明问题之前不要优化。过早优化增加的复杂度比它获得的性能成本更高。

## Core Web Vitals 目标

| 指标 | 良好 | 需要改进 | 差 |
|------|------|----------|-----|
| **LCP**（最大内容绘制） | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| **INP**（交互到下一次绘制） | ≤ 200ms | ≤ 500ms | > 500ms |
| **CLS**（累积布局偏移） | ≤ 0.1 | ≤ 0.25 | > 0.25 |

## 优化工作流

```
1. 度量  → 使用真实数据建立基线
2. 识别  → 找到真正的瓶颈（而非假设的）
3. 修复  → 解决特定瓶颈
4. 验证  → 再次度量，确认改进
5. 防护  → 添加监控或测试防止回归
```

### 步骤 1：度量

**前端：**
```bash
# Chrome DevTools 中的 Lighthouse（或 CI）
# Chrome DevTools → 性能标签页 → 录制
# Chrome DevTools MCP → 性能跟踪

# 代码中的 Web Vitals 库
import { onLCP, onINP, onCLS } from 'web-vitals';

onLCP(console.log);
onINP(console.log);
onCLS(console.log);
```

**后端：**
```bash
# 响应时间日志
# 应用性能监控 (APM)
# 带时序的数据库查询日志

# 简单计时
console.time('db-query');
const result = await db.query(...);
console.timeEnd('db-query');
```

### 从哪里开始度量

使用症状决定首先度量什么：

```
什么慢？
├── 首次页面加载
│   ├── 大包？--> 度量包大小，检查代码分割
│   ├── 服务器响应慢？--> 度量 TTFB，检查 API/数据库
│   └── 渲染阻塞资源？--> 检查 CSS/JS 阻塞的网络瀑布
├── 交互感觉迟钝
│   ├── 点击时 UI 冻结？--> 分析主线程，查找长任务 (>50ms)
│   ├── 表单输入延迟？--> 检查重新渲染、受控组件开销
│   └── 动画卡顿？--> 检查布局抖动、强制重排
├── 导航后页面
│   ├── 数据加载？--> 度量 API 响应时间，检查瀑布
│   └── 客户端渲染？--> 分析组件渲染时间，检查 N+1 获取
└── 后端 / API
    ├── 单个端点慢？--> 分析数据库查询，检查索引
    ├── 所有端点慢？--> 检查连接池、内存、CPU
    └── 间歇性慢？--> 检查锁争用、GC 暂停、外部依赖
```

### 步骤 2：识别瓶颈

按类别列出常见瓶颈：

**前端：**

| 症状 | 可能原因 | 调查 |
|------|----------|------|
| LCP 慢 | 大图像、渲染阻塞资源、服务器慢 | 检查网络瀑布、图像大小 |
| CLS 高 | 无尺寸的图像、延迟加载内容、字体偏移 | 检查布局偏移归因 |
| INP 差 | 主线程上繁重的 JavaScript、大 DOM 更新 | 检查性能跟踪中的长任务 |
| 初始加载慢 | 大包、许多网络请求 | 检查包大小、代码分割 |

**后端：**

| 症状 | 可能原因 | 调查 |
|------|----------|------|
| API 响应慢 | N+1 查询、缺少索引、未优化的查询 | 检查数据库查询日志 |
| 内存增长 | 泄漏的引用、无界缓存、大有效负载 | 堆快照分析 |
| CPU 峰值 | 同步繁重计算、正则表达式回溯 | CPU 分析 |
| 高延迟 | 缺少缓存、冗余计算、网络跳转 | 跟踪请求通过堆栈 |

### 步骤 3：修复常见反模式

#### N+1 查询（后端）

```typescript
// 坏：N+1 — 每个任务一个查询获取所有者
const tasks = await db.tasks.findMany();
for (const task of tasks) {
  task.owner = await db.users.findUnique({ where: { id: task.ownerId } });
}

// 好：带 join/include 的单个查询
const tasks = await db.tasks.findMany({
  include: { owner: true },
});
```

#### 无界数据获取

```typescript
// 坏：获取所有记录
const allTasks = await db.tasks.findMany();

// 好：带限制的分页
const tasks = await db.tasks.findMany({
  take: 20,
  skip: (page - 1) * 20,
  orderBy: { createdAt: 'desc' },
});
```

#### 缺少图像优化（前端）

```html
<!-- 坏：无尺寸、无延迟加载、无响应式尺寸 -->
<img src="/hero.jpg" />

<!-- 好：响应式、延迟加载、适当尺寸 -->
<img
  src="/hero.jpg"
  srcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1200.webp 1200w"
  sizes="(max-width: 768px) 100vw, 50vw"
  width="1200"
  height="600"
  loading="lazy"
  alt="Hero 图像描述"
/>
```

#### 不必要的重新渲染（React）

```tsx
// 坏：每次渲染创建新对象，导致子组件重新渲染
function TaskList() {
  return <TaskFilters options={{ sortBy: 'date', order: 'desc' }} />;
}

// 好：稳定引用
const DEFAULT_OPTIONS = { sortBy: 'date', order: 'desc' } as const;
function TaskList() {
  return <TaskFilters options={DEFAULT_OPTIONS} />;
}

// 对昂贵组件使用 React.memo
const TaskItem = React.memo(function TaskItem({ task }: Props) {
  return <div>{/* 昂贵渲染 */}</div>;
});

// 对昂贵计算使用 useMemo
function TaskStats({ tasks }: Props) {
  const stats = useMemo(() => calculateStats(tasks), [tasks]);
  return <div>{stats.completed} / {stats.total}</div>;
}
```

#### 大包大小

```typescript
// 坏：导入整个库
import { format } from 'date-fns';

// 好：树摇导入（如果库支持）
import { format } from 'date-fns/format';

// 好：对繁重、很少使用的功能动态导入
const ChartLibrary = lazy(() => import('./ChartLibrary'));
```

#### 缺少缓存（后端）

```typescript
// 缓存频繁读取、很少更改的数据
const CACHE_TTL = 5 * 60 * 1000; // 5 分钟
let cachedConfig: AppConfig | null = null;
let cacheExpiry = 0;

async function getAppConfig(): Promise<AppConfig> {
  if (cachedConfig && Date.now() < cacheExpiry) {
    return cachedConfig;
  }
  cachedConfig = await db.config.findFirst();
  cacheExpiry = Date.now() + CACHE_TTL;
  return cachedConfig;
}

// 静态资源的 HTTP 缓存头部
app.use('/static', express.static('public', {
  maxAge: '1y',           // 缓存 1 年
  immutable: true,        // 永不重新验证（在文件名中使用内容哈希）
}));

// API 响应的 Cache-Control
res.set('Cache-Control', 'public, max-age=300'); // 5 分钟
```

## 性能预算

设置预算并强制执行：

```
JavaScript 包：< 200KB gzipped（初始加载）
CSS：< 50KB gzipped
图像：< 200KB 每张（首屏）
字体：< 100KB 总计
API 响应时间：< 200ms (p95)
可交互时间：4G 上 < 3.5s
Lighthouse 性能分数：≥ 90
```

**在 CI 中强制执行：**
```bash
# 包大小检查
npx bundlesize --config bundlesize.config.json

# Lighthouse CI
npx lhci autorun
```

## 常见误解

| 误解 | 现实 |
|------|------|
| "我们稍后优化" | 性能债务会复合。现在修复明显的反模式，推迟微优化。 |
| "在我的机器上很快" | 你的机器不是用户的。在代表性硬件和网络上分析。 |
| "这个优化很明显" | 如果你没有度量，你就不知道。先分析。 |
| "用户不会注意到 100ms" | 研究表明 100ms 延迟会影响转化率。用户注意到的比你想象的多。 |
| "框架处理性能" | 框架防止某些问题但不能修复 N+1 查询或超大包。 |

## 红旗

- 没有分析数据支持的优化
- 数据获取中的 N+1 查询模式
- 没有分页的列表端点
- 没有尺寸、延迟加载或响应式尺寸的图像
- 包大小增长没有审查
- 生产中没有性能监控
- 到处使用 `React.memo` 和 `useMemo`（过度使用和不足一样糟糕）

## 验证

任何性能相关变更后：

- [ ] 存在前后度量（具体数字）
- [ ] 识别并解决了特定瓶颈
- [ ] Core Web Vitals 在"良好"阈值内
- [ ] 包大小没有显著增加
- [ ] 新数据获取代码中没有 N+1 查询
- [ ] 性能预算在 CI 中通过（如果配置）
- [ ] 现有测试仍然通过（优化没有破坏行为）
