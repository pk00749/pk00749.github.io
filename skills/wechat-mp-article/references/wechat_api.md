# 微信公众号API参考

## 获取Access Token

### 请求

```
GET https://api.weixin.qq.com/cgi-bin/token
```

### 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| grant_type | 是 | 固定值: client_credential |
| appid | 是 | 公众号AppID |
| secret | 是 | 公众号AppSecret |

### 响应

```json
{
  "access_token": "ACCESS_TOKEN",
  "expires_in": 7200
}
```

### Python示例

```python
import requests

def get_access_token(app_id, app_secret):
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        'grant_type': 'client_credential',
        'appid': app_id,
        'secret': app_secret
    }
    response = requests.get(url, params=params)
    return response.json().get('access_token')
```

## 创建草稿

### 请求

```
POST https://api.weixin.qq.com/cgi-bin/draft/add
```

### 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| access_token | 是 | 调用凭证 |

### 请求体

```json
{
  "articles": [
    {
      "title": "文章标题",
      "author": "作者",
      "content": "HTML内容",
      "digest": "摘要",
      "content_source_url": "原文链接",
      "thumb_media_id": "封面图片media_id"
    }
  ]
}
```

### 响应

```json
{
  "draft_id": 123456789,
  "msg_id": "msg_id"
}
```

## 上传封面图片

### 请求

```
POST https://api.weixin.qq.com/cgi-bin/media/uploadimg
```

### 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| access_token | 是 | 调用凭证 |

### 请求体

multipart/form-data:
- media: 图片文件

### 响应

```json
{
  "url": "http://mmbiz.qpic.cn/...",
  "media_id": "MEDIA_ID"
}
```

> 注意：上传封面需要使用 `uploadimg` 接口，而不是 `media/upload`。返回的是 url，可以在创建草稿时直接使用图片URL。

## 注意事项

1. **access_token有效期**: 2小时，需要缓存重复使用
2. **接口调用频率**: 每个账号每分钟最多60次
3. **图片大小**: 封面图片不超过2MB
4. **HTML限制**: 公众号文章HTML不支持CSS外部样式表，需使用行内样式
