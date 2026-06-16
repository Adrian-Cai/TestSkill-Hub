# 复制逻辑规则

## 源码位置

完整可用的复制逻辑（含主逻辑 + 降级 + 反馈）在：

```
../../snippets/toolbar.html
```

本规则只描述"必须满足的契约"，不重复源码。

## 主逻辑契约

- 必须使用 `navigator.clipboard.write` 配合 `ClipboardItem`
- 必须同时写入 `text/html` 和 `text/plain`：
  - `text/html`：`article.outerHTML`
  - `text/plain`：`article.innerText`

## 降级逻辑契约

- 如果不支持 `ClipboardItem`，必须使用：
  - `Range`
  - `Selection`
  - `document.execCommand('copy')`

## 严格限制

- 不得用 `writeText` 代替主逻辑
- 不得用 `innerHTML` 代替 `article.outerHTML`
- 不得复制整页 `document.body`
- 不得把工具栏复制进去

## 交互反馈

复制成功与失败都必须有明显提示：

- 成功：`已复制,可粘贴到公众号后台`
- 失败：`复制失败,请手动选中文章区域复制`
