# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### 微信公众号

- app_id: 你的公众号AppID
- app_secret: 你的公众号AppSecret
- 配置方式：设置环境变量 `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET`，或创建 `~/.wechat_mp_config` 文件

---

### Self-Improvement Skill

- 位置：`/home/ubuntu/.openclaw/workspace/skills/self-improving-agent`
- 日志目录：`/home/ubuntu/.openclaw/workspace/.learnings/`
- 使用：每次被纠正或遇到错误时，记录到对应的 .md 文件

---

Add whatever helps you do your job. This is your cheat sheet.
