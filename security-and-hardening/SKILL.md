---
name: 安全加固
description: 加固代码以防止漏洞。适用于处理用户输入、认证、数据存储或外部集成时。适用于构建接受不可信数据、管理用户会话或与第三方服务交互的任何功能时。
---

# 安全加固

## 概述

Web 应用程序的安全优先开发实践。将每个外部输入视为敌对的，每个机密视为神圣的，每个授权检查视为强制性的。安全不是一个阶段——它是接触用户数据、认证或外部系统的每一行代码的约束。

## 何时使用

- 构建接受用户输入的任何内容
- 实现认证或授权
- 存储或传输敏感数据
- 与外部 API 或服务集成
- 添加文件上传、webhook 或回调
- 处理支付或 PII 数据

## 三层边界系统

### 始终执行（无例外）

- **在系统边界验证所有外部输入**（API 路由、表单处理器）
- **参数化所有数据库查询**——永远不要将用户输入连接到 SQL
- **编码输出**以防止 XSS（使用框架自动转义，不要绕过它）
- **使用 HTTPS** 进行所有外部通信
- **使用 bcrypt/scrypt/argon2 哈希密码**（永远不要存储明文）
- **设置安全头部**（CSP、HSTS、X-Frame-Options、X-Content-Type-Options）
- **使用 httpOnly、secure、sameSite cookies** 存储会话
- **在每次发布前运行 `npm audit`**（或等效命令）

### 先询问（需要人工批准）

- 添加新的认证流程或更改认证逻辑
- 存储新类别的敏感数据（PII、支付信息）
- 添加新的外部服务集成
- 更改 CORS 配置
- 添加文件上传处理器
- 修改速率限制或节流
- 授予提升的权限或角色

### 永远不做

- **永远不要提交机密**到版本控制（API 密钥、密码、令牌）
- **永远不要记录敏感数据**（密码、令牌、完整信用卡号）
- **永远不要信任客户端验证**作为安全边界
- **永远不要为了方便而禁用安全头部**
- **永远不要使用 `eval()` 或 `innerHTML`** 处理用户提供的数据
- **永远不要将会话存储在客户端可访问的存储中**（用于认证令牌的 localStorage）
- **永远不要向用户暴露堆栈跟踪**或内部错误详细信息

## OWASP Top 10 预防

### 1. 注入（SQL、NoSQL、OS 命令）

```typescript
// 坏：通过字符串连接进行 SQL 注入
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// 好：参数化查询
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);

// 好：使用参数化输入的 ORM
const user = await prisma.user.findUnique({ where: { id: userId } });
```

### 2. 破损的认证

```typescript
// 密码哈希
import { hash, compare } from 'bcrypt';

const SALT_ROUNDS = 12;
const hashedPassword = await hash(plaintext, SALT_ROUNDS);
const isValid = await compare(plaintext, hashedPassword);

// 会话管理
app.use(session({
  secret: process.env.SESSION_SECRET,  // 来自环境，而非代码
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,     // JavaScript 不可访问
    secure: true,       // 仅 HTTPS
    sameSite: 'lax',    // CSRF 防护
    maxAge: 24 * 60 * 60 * 1000,  // 24 小时
  },
}));
```

### 3. 跨站脚本 (XSS)

```typescript
// 坏：将用户输入渲染为 HTML
element.innerHTML = userInput;

// 好：使用框架自动转义（React 默认执行此操作）
return <div>{userInput}</div>;

// 如果必须渲染 HTML，先清理
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput);
```

### 4. 破损的访问控制

```typescript
// 始终检查授权，而不仅仅是认证
app.patch('/api/tasks/:id', authenticate, async (req, res) => {
  const task = await taskService.findById(req.params.id);

  // 检查认证用户是否拥有此资源
  if (task.ownerId !== req.user.id) {
    return res.status(403).json({
      error: { code: 'FORBIDDEN', message: '无权修改此任务' }
    });
  }

  // 继续更新
  const updated = await taskService.update(req.params.id, req.body);
  return res.json(updated);
});
```

### 5. 安全配置错误

```typescript
// 安全头部（对 Express 使用 helmet）
import helmet from 'helmet';
app.use(helmet());

// 内容安全策略
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],  // 尽可能收紧
    imgSrc: ["'self'", 'data:', 'https:'],
    connectSrc: ["'self'"],
  },
}));

// CORS — 限制为已知来源
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || 'http://localhost:3000',
  credentials: true,
}));
```

### 6. 敏感数据暴露

```typescript
// 永远不要在 API 响应中返回敏感字段
function sanitizeUser(user: UserRecord): PublicUser {
  const { passwordHash, resetToken, ...publicFields } = user;
  return publicFields;
}

// 对机密使用环境变量
const API_KEY = process.env.STRIPE_API_KEY;
if (!API_KEY) throw new Error('STRIPE_API_KEY 未配置');
```

## 输入验证模式

### 边界处的模式验证

```typescript
import { z } from 'zod';

const CreateTaskSchema = z.object({
  title: z.string().min(1).max(200).trim(),
  description: z.string().max(2000).optional(),
  priority: z.enum(['low', 'medium', 'high']).default('medium'),
  dueDate: z.string().datetime().optional(),
});

// 在路由处理器中验证
app.post('/api/tasks', async (req, res) => {
  const result = CreateTaskSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: '输入无效',
        details: result.error.flatten(),
      },
    });
  }
  // result.data 现在是类型化且已验证的
  const task = await taskService.create(result.data);
  return res.status(201).json(task);
});
```

### 文件上传安全

```typescript
// 限制文件类型和大小
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_SIZE = 5 * 1024 * 1024; // 5MB

function validateUpload(file: UploadedFile) {
  if (!ALLOWED_TYPES.includes(file.mimetype)) {
    throw new ValidationError('不允许的文件类型');
  }
  if (file.size > MAX_SIZE) {
    throw new ValidationError('文件太大（最大 5MB）');
  }
  // 不要信任文件扩展名——如果关键，检查魔术字节
}
```

## 分类 npm audit 结果

并非所有审计发现都需要立即行动。使用此决策树：

```
npm audit 报告漏洞
├── 严重性：关键或高
│   ├── 可疑代码在你的应用中可访问？
│   │   ├── 是 --> 立即修复（更新、修补或替换依赖）
│   │   └── 否（仅开发依赖、未使用代码路径）--> 尽快修复，但不是阻塞项
│   └── 有可用修复？
│       ├── 是 --> 更新到修补版本
│       └── 否 --> 检查解决方法，考虑替换依赖，或添加到允许列表并设置审查日期
├── 严重性：中等
│   ├── 生产中可访问？--> 在下一个发布周期修复
│   └── 仅开发？--> 方便时修复，在待办事项中跟踪
└── 严重性：低
    └── 在常规依赖更新期间跟踪和修复
```

**关键问题：**
- 可疑函数是否在你的代码路径中实际调用？
- 依赖是运行时依赖还是仅开发依赖？
- 鉴于你的部署上下文，漏洞是否可被利用（例如，客户端应用中的服务器端漏洞）？

当你推迟修复时，记录原因并设置审查日期。

## 速率限制

```typescript
import rateLimit from 'express-rate-limit';

// 通用 API 速率限制
app.use('/api/', rateLimit({
  windowMs: 15 * 60 * 1000, // 15 分钟
  max: 100,                   // 每个窗口 100 个请求
  standardHeaders: true,
  legacyHeaders: false,
}));

// 认证端点的更严格限制
app.use('/api/auth/', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,  // 每 15 分钟 10 次尝试
}));
```

## 机密管理

```
.env 文件：
  ├── .env.example  → 已提交（带占位符值的模板）
  ├── .env          → 未提交（包含真实机密）
  └── .env.local    → 未提交（本地覆盖）

.gitignore 必须包含：
  .env
  .env.local
  .env.*.local
  *.pem
  *.key
```

**提交前始终检查：**
```bash
# 检查意外暂存的机密
git diff --cached | grep -i "password\|secret\|api_key\|token"
```

## 安全审查清单

```markdown
### 认证
- [ ] 密码使用 bcrypt/scrypt/argon2 哈希（盐轮数 ≥ 12）
- [ ] 会话令牌是 httpOnly、secure、sameSite
- [ ] 登录有速率限制
- [ ] 密码重置令牌过期

### 授权
- [ ] 每个端点检查用户权限
- [ ] 用户只能访问自己的资源
- [ ] 管理操作需要管理员角色验证

### 输入
- [ ] 所有用户输入在边界处验证
- [ ] SQL 查询是参数化的
- [ ] HTML 输出是编码/转义的

### 数据
- [ ] 代码或版本控制中没有机密
- [ ] 敏感字段从 API 响应中排除
- [ ] PII 静态加密（如果适用）

### 基础设施
- [ ] 安全头部已配置（CSP、HSTS 等）
- [ ] CORS 限制为已知来源
- [ ] 依赖经过漏洞审计
- [ ] 错误消息不暴露内部信息
```

## 常见误解

| 误解 | 现实 |
|------|------|
| "这是内部工具，安全不重要" | 内部工具会被破坏。攻击者针对最薄弱的环节。 |
| "我们稍后添加安全" | 安全改造比内置难 10 倍。现在添加。 |
| "没人会试图利用这个" | 自动扫描器会找到它。通过模糊实现的安全不是安全。 |
| "框架处理安全" | 框架提供工具，而非保证。你仍然需要正确使用它们。 |
| "这只是原型" | 原型会成为生产。从第一天开始的安全习惯。 |

## 红旗

- 用户输入直接传递到数据库查询、shell 命令或 HTML 渲染
- 源代码或提交历史中的机密
- 没有认证或授权检查的 API 端点
- 缺少 CORS 配置或通配符 (`*`) 来源
- 认证端点没有速率限制
- 向用户暴露堆栈跟踪或内部错误
- 具有已知关键漏洞的依赖

## 验证

实现安全相关代码后：

- [ ] `npm audit` 没有关键或高漏洞
- [ ] 源代码或 git 历史中没有机密
- [ ] 所有用户输入在系统边界验证
- [ ] 每个受保护端点都检查了认证和授权
- [ ] 响应中存在安全头部（使用浏览器 DevTools 检查）
- [ ] 错误响应不暴露内部详细信息
- [ ] 认证端点上启用了速率限制
