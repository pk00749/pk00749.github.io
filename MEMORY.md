# MEMORY.md - 长期记忆

_这里是同德贾维斯的长期记忆，记录重要的事情、偏好、决策和教训。_

---

## 关于魔兽

- **GitHub**: pk00749
- **偏好**: 高效直接的沟通
- **创建了私有仓库**: jarvis-openclaw
- **2026-03-05**: 回公司上班

---

## 定时任务

- 6 个定时任务，全部由 main agent 负责
- 股票公告跟踪：600499、000533
- 每日任务：爆文、日志、workspace 自动提交

---

## 已完成任务

- 修复了 Feishu 插件重复加载问题

---

## Self-Improvement Skill (2026-03-07)

安装位置：`/home/ubuntu/.openclaw/workspace/skills/self-improving-agent`

### 核心功能

自动记录学习、错误和修正，用于持续改进。

### 日志文件

- `.learnings/LEARNINGS.md` - 学到的新知识、用户纠正、最佳实践
- `.learnings/ERRORS.md` - 命令失败、异常
- `.learnings/FEATURE_REQUESTS.md` - 用户请求的功能

### 触发场景

| 场景 | 记录到 |
|------|--------|
| 命令/操作失败 | ERRORS.md |
| 用户纠正 ("No, that's wrong...") | LEARNINGS.md (correction) |
| 用户请求不存在的功能 | FEATURE_REQUESTS.md |
| API/外部工具失败 | ERRORS.md |
| 知识过时/错误 | LEARNINGS.md (knowledge_gap) |
| 发现更好的方法 | LEARNINGS.md (best_practice) |

### 提升规则

广泛适用的学习内容，提升到：
- **行为模式** → SOUL.md
- **工作流改进** → AGENTS.md
- **工具问题** → TOOLS.md

### 使用频率

- 每次被纠正时记录
- 每次遇到错误时记录
- 每周回顾一次学习内容

---

*更新于 2026-03-07*
