# HTML 结构规则

## 必须包含的结构

每个生成的文件都必须包含：

- 顶部工具栏
- 工具栏标题：`公众号富文本复制器`
- 按钮文本：`复制富文本`
- 提示文本：`点击按钮后粘贴到公众号后台`
- 正文容器：`<article id="wechatArticle">...</article>`

## 工具栏与复制逻辑

**不要在规则文件里贴源码**。完整可用的工具栏 DOM + 复制逻辑 + Design Tokens 在：

```
../../snippets/toolbar.html
```

直接复制该文件的内容到生成的 `.html` 中相应位置。

## 结构约束

- `id="wechatArticle"` 必须且只能出现一次
- 被复制的根节点必须是 `article#wechatArticle`
- 工具栏不能放进 `article#wechatArticle` 里
- 正文容器样式必须包含：`max-width:760px; margin:0 auto; background:#fff;`
- 页面需要移动端友好

## 推荐布局

- 页面底部和四周保留足够留白
- 工具栏固定在正文外层容器中
- 正文作为独立白底内容区，适合直接复制到公众号后台
