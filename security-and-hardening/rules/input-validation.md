# 输入验证模式

## 边界处的模式验证

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

## 文件上传安全

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
