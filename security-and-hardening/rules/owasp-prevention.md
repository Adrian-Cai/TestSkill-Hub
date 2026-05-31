# OWASP Top 10 预防

## 1. 注入（SQL、NoSQL、OS 命令）

```typescript
// 坏：通过字符串连接进行 SQL 注入
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// 好：参数化查询
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);

// 好：使用参数化输入的 ORM
const user = await prisma.user.findUnique({ where: { id: userId } });
```

## 2. 破损的认证

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

## 3. 跨站脚本 (XSS)

```typescript
// 坏：将用户输入渲染为 HTML
element.innerHTML = userInput;

// 好：使用框架自动转义（React 默认执行此操作）
return <div>{userInput}</div>;

// 如果必须渲染 HTML，先清理
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput);
```

## 4. 破损的访问控制

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

## 5. 安全配置错误

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

## 6. 敏感数据暴露

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
