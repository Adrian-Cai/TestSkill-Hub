# 安全回退模式

## 安全回退模式

在时间压力下，使用安全回退：

```typescript
// 安全默认值 + 警告（而不是崩溃）
function getConfig(key: string): string {
  const value = process.env[key];
  if (!value) {
    console.warn(`缺少配置：${key}，使用默认值`);
    return DEFAULTS[key] ?? '';
  }
  return value;
}

// 优雅降级（而不是功能损坏）
function renderChart(data: ChartData[]) {
  if (data.length === 0) {
    return <EmptyState message="此时间段没有可用数据" />;
  }
  try {
    return <Chart data={data} />;
  } catch (error) {
    console.error('图表渲染失败：', error);
    return <ErrorState message="无法显示图表" />;
  }
}
```
