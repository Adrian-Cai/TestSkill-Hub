# 性能预算

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

## 在 CI 中强制执行

```bash
# 包大小检查
npx bundlesize --config bundlesize.config.json

# Lighthouse CI
npx lhci autorun
```
