---
name: wechat-mp-article
description: 将内容排版成微信公众号文章并创建草稿。适用于：(1) 将文章发布到微信公众号草稿箱，(2) 微信公众号文章排版优化，(3) 创建公众号图文消息。当用户提到微信公众号、微信文章、公众号草稿时使用此skill。
---

# 微信公众号文章发布

## 快速开始

### 第一步：配置微信公众号

首次使用需要配置公众号凭证。在 TOOLS.md 中添加：

```markdown
### 微信公众号

- app_id: 你的公众号AppID
- app_secret: 你的公众号AppSecret
```

### 第二步：发送内容

将需要发布的内容发送给我，可以是：
- Markdown 格式的文章
- 纯文本内容
- 已写好的 HTML

### 第三步：确认发布

确认后将调用公众号API创建草稿。

## 微信公众号支持的HTML标签

公众号文章支持的标签有限，常用标签：

- 标题：`<h1>`, `<h2>`, `<h3>`
- 加粗：`<strong>` 或 `<b>`
- 斜体：`<em>` 或 `<i>`
- 下划线：`<u>`
- 删除线：`<s>`
- 段落：`<p>`
- 换行：`<br>`
- 列表：`<ul>`, `<ol>`, `<li>`
- 图片：`<img src="url" />`
- 引用：`<blockquote>`
- 代码：`<pre>`, `<code>`
- 分割线：`<hr>`

> 注意：微信公众号不支持 CSS 样式，需使用行内样式。

## 排版转换

调用 Python 脚本将 Markdown 转换为公众号兼容的 HTML：

```bash
python3 scripts/md_to_wechat.py <输入文件> <输出文件> [封面图片URL]
```

## 创建草稿

调用 Python 脚本创建公众号草稿：

```bash
python3 scripts/create_draft.py <html文件> <标题> <作者> [封面图片URL]
```

脚本会自动：
1. 获取 access_token
2. 上传封面图片（如果提供）
3. 创建草稿并返回草稿ID

## 参考

详细 API 说明和示例见 [references/wechat_api.md](references/wechat_api.md)
