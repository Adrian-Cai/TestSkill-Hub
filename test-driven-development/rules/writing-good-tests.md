# 编写好的测试

## 测试状态，而非交互

断言操作的*结果*，而不是内部调用了哪些方法。验证方法调用序列的测试在重构时会中断，即使行为没有改变。

## 测试中 DAMP 优于 DRY

在生产代码中，DRY（不要重复自己）通常是正确的。在测试中，**DAMP（描述性和有意义的短语）** 更好。测试应该读起来像规范——每个测试都应该讲述一个完整的故事，而不需要读者追溯共享辅助函数。

## 优先使用真实实现而非 mock

使用完成工作的最简单测试替身。测试使用的真实代码越多，它们提供的信心就越多。

```
偏好顺序（从最不preferred到最不preferred）：
1. 真实实现  → 最高信心，捕获真实 bug
2. Fake      → 依赖的内存版本（如 fake DB）
3. Stub      → 返回预制数据，无行为
4. Mock（交互）→ 验证方法调用——谨慎使用
```

**仅在以下情况使用 mock：** 真实实现太慢、不确定或有无法控制的副作用（外部 API、电子邮件发送）。过度 mock 会导致测试通过但生产中断。

## 使用 Arrange-Act-Assert 模式

```typescript
it('当截止日期已过时标记逾期任务', () => {
  // Arrange：设置测试场景
  const task = createTask({
    title: 'Test',
    deadline: new Date('2025-01-01'),
  });

  // Act：执行被测试的操作
  const result = checkOverdue(task, new Date('2025-01-02'));

  // Assert：验证结果
  expect(result.isOverdue).toBe(true);
});
```

## 每个概念一个断言

```typescript
// 好：每个测试验证一个行为
it('拒绝空标题', () => { ... });
it('修剪标题中的空白', () => { ... });
it('强制最大标题长度', () => { ... });

// 坏：所有内容在一个测试中
it('正确验证标题', () => {
  expect(() => createTask({ title: '' })).toThrow();
  expect(createTask({ title: '  hello  ' }).title).toBe('hello');
  expect(() => createTask({ title: 'a'.repeat(256) })).toThrow();
});
```

## 描述性命名测试

```typescript
// 好：读起来像规范
describe('TaskService.completeTask', () => {
  it('设置状态为完成并记录时间戳', ...);
  it('对不存在的任务抛出 NotFoundError', ...);
  it('是幂等的——完成已完成的任务是空操作', ...);
  it('向任务指派人发送通知', ...);
});

// 坏：模糊的名称
describe('TaskService', () => {
  it('工作', ...);
  it('处理错误', ...);
  it('测试 3', ...);
});
```
