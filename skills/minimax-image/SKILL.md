---
name: minimax-image
description: 使用 MiniMax 文生图 API 生成图片。当需要为文章/内容生成配图时使用。使用方法：运行 scripts/generate_image.py --prompt "描述" [--aspect-ratio 16:9] [--n 1]
---

# MiniMax Image Generation

使用 MiniMax 的 image-01 模型生成图片。

## API 参考

https://platform.minimaxi.com/docs/api-reference/image-generation-t2i

## 环境变量 / API Key

优先从以下顺序获取：
1. `--api-key` 参数
2. `MINIMAX_API_KEY` 环境变量

## 使用方式

```bash
python3 scripts/generate_image.py --prompt "画面描述" [--aspect-ratio 16:9] [--n 1]
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` / `-p` | 画面描述（最长1500字符） | 必填 |
| `--aspect-ratio` / `-r` | 宽高比 | 16:9 |
| `--n` | 生成数量(1-9) | 1 |
| `--model` / `-m` | 模型(image-01/image-01-live) | image-01 |
| `--api-key` / `-k` | API Key | 环境变量 |

### 宽高比可选值

- `1:1` (1024x1024)
- `16:9` (1280x720) ← 爆文配图默认用这个
- `4:3` (1152x864)
- `3:2` (1248x832)
- `2:3` (832x1248)
- `3:4` (864x1152)
- `9:16` (720x1280)
- `21:9` (1344x576) (仅 image-01)

### 输出格式

成功时输出：
```
IMAGE_URL_1: https://...
MEDIA_URL: https://...
```

失败时输出错误信息到 stderr，exit code 1。

## 爆文配图场景

爆文 cron 任务中，图片生成调用方式：
```bash
MINIMAX_API_KEY=sk-cp-xxx \
python3 /home/ubuntu/.openclaw/workspace/skills/minimax-image/scripts/generate_image.py \
  --prompt "具体的画面描述，符合文章主题" \
  --aspect-ratio 16:9
```

## 注意事项

- API key 从 auth-profiles.json 中读取，或设置 MINIMAX_API_KEY 环境变量
- url 有效期 24 小时
- 图片生成时间约 10-30 秒，超时时间设为 120 秒