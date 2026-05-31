# 常见性能反模式

## N+1 查询（后端）

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

## 无界数据获取

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

## 缺少图像优化（前端）

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

## 不必要的重新渲染（React）

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

## 大包大小

```typescript
// 坏：导入整个库
import { format } from 'date-fns';

// 好：树摇导入（如果库支持）
import { format } from 'date-fns/format';

// 好：对繁重、很少使用的功能动态导入
const ChartLibrary = lazy(() => import('./ChartLibrary'));
```

## 缺少缓存（后端）

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
