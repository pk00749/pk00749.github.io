# What is War — 技术架构 & MVP 方案

> "书本的历史滞后，但历史每天都在发生。"
> 做一个记录全球每天战争情况的网站，让历史"实时发生"。

---

## 1. 项目定位

**名字：What is War**

**一句话：** 面向普通人的全球战争实时简报工具。

**核心价值：** 每天自动化抓取全球冲突数据，生成可视化战况简报，让用户不用看几十篇新闻也能知道今天世界哪里在打仗、死了多少人。

**MVP 定位：** 先做一个地区（俄乌战争），验证数据流程和用户需求。

---

## 2. 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                     Vercel (部署层)                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐         ┌──────────────────────────┐  │
│  │  React 前端   │         │   Python API (FastAPI)  │  │
│  │  Next.js     │  <───>  │   /api/events           │  │
│  │  shadcn/ui   │         │   /api/stats            │  │
│  │  Recharts    │         │   /api/timeline        │  │
│  │  Mapbox GL   │         └──────────┬─────────────┘  │
│  └──────────────┘                    │                 │
│                                       │                 │
│                          ┌────────────▼────────────┐    │
│                          │   JSONL Data Layer      │    │
│                          │   (Git Repo / Blob)     │    │
│                          │   /data/conflicts/      │    │
│                          │   /data/daily/          │    │
│                          └─────────────────────────┘    │
│                                                          │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │ CI/CD (GitHub Actions)
                          │
┌──────────────────────────▼─────────────────────────────┐
│                   数据源 (Data Sources)                  │
│                                                          │
│   GDELT API          ACLED (免费层)       人工录入     │
│   (免费, 日更新)      (事件级冲突数据)     (补充实时)   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 技术栈选择

### 前端

| 技术 | 用途 | 选择理由 |
|------|------|----------|
| **Next.js 14** | React 框架 | Vercel 原生支持，SSR/SSG 灵活，数据更新友好 |
| **Tailwind CSS** | 样式 | 开发快，定制强，Vercel 内置支持 |
| **shadcn/ui** | UI 组件库 | 基于 Radix，质量高，可深度定制 |
| **Recharts** | 图表 | React 原生，轻量，好看 |
| **Mapbox GL JS** | 交互地图 | 战争地点可视化核心，比 Leaflet 更美观 |
| **date-fns** | 日期处理 | 轻量日期库 |

### 后端

| 技术 | 用途 |
|------|------|
| **Python 3.11** | 数据处理核心语言 |
| **FastAPI** | Python API 框架，轻量高性能 |
| **httpx** | 异步 HTTP 请求，抓取 GDELT/ACLED |
| **BeautifulSoup4** | HTML 解析，备用爬虫 |

### 部署 & 基础设施

| 技术 | 用途 |
|------|------|
| **Vercel** | 前端 + Python API 部署 |
| **GitHub Actions** | 数据更新 CI/CD 流水线 |
| **GitHub Repository** | JSONL 数据存储（用 git 作版本控制） |
| **Terraform** | 云资源管理（你的强项） |

---

## 4. 数据结构方案（JSONL）

### 设计原则

- **每行一条记录**，方便追加和流式处理
- **文件按「冲突区域 + 时间」分割**，避免单文件过大
- **零数据库**，所有数据存在 GitHub 仓库的 `/data` 目录下
- **只追加，不修改历史行**，保证数据可溯源

### 目录结构

```
data/
├── ukraine/                     # 俄乌冲突
│   ├── ukraine-2026-01.jsonl    # 俄乌冲突 2026 年 1 月
│   ├── ukraine-2026-02.jsonl
│   ├── ukraine-2026-03.jsonl
│   └── ukraine-2026-04.jsonl
├── middle-east/                     # 中东冲突
│   ├── middle-east-2026-01.jsonl    # 中东冲突 2026 年 1 月
│   ├── middle-east-2026-02.jsonl
│   ├── middle-east-2026-03.jsonl
│   └── middle-east-2026-04.jsonl
├── stats/
│   ├── ukraine-daily.jsonl      # 俄乌每日统计汇总
│   ├── middle-east-daily.jsonl  # 中东每日统计汇总
│   └── global-weekly.jsonl      # 全球每周概览
└── sources/
    └── source-index.jsonl       # 数据来源索引
```

### 核心数据结构

#### 4.1 冲突事件（conflict-event）

```jsonl
{"id": "gdelt-20260413-001", "source": "gdelt", "region": "ukraine", "date": "2026-04-13", "time": "14:32:00Z", "location": {"lat": 48.456, "lon": 35.017, "place": "顿涅茨克州", "country": "乌克兰"}, "event_type": "battle", "sub_type": "aerial_strike", "actors": {"perpetrator": ["俄军", "第 58 集团军"], "target": ["乌军", "第 54 旅"]}, "fatalities": {"confirmed": 12, "estimated_min": 10, "estimated_max": 15, "civilians": 3}, "description": "俄军对顿涅茨克州某地发动空袭，造成至少 12 名乌军士兵死亡。", "sources": [{"name": "路透社", "url": "https://reuters.com/..."}, {"name": "Ukrainska Pravda", "url": "https://un.ua/..."}], "confidence": 0.85, "related_events": ["gdelt-20260413-002"], "tags": ["俄乌战争", "空袭", "顿巴斯"]}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 全局唯一 ID，格式：`{来源}-{日期}-{序号}` |
| `source` | string | 数据来源：`gdelt` / `acled` / `manual` |
| `region` | string | 冲突区域：`ukraine` / `middle-east` / `sudan` 等 |
| `date` | string | 事件日期，格式 `YYYY-MM-DD` |
| `time` | string | 事件时间（UTC），可选 |
| `location` | object | 地理位置 |
| `event_type` | string | 事件类型（见事件类型表） |
| `sub_type` | string | 事件子类型 |
| `actors` | object | 涉事方 |
| `fatalities` | object | 伤亡数据 |
| `description` | string | 事件描述（英文原始或中文翻译） |
| `sources` | array | 来源链接 |
| `confidence` | float | 数据可信度 0.0-1.0 |
| `related_events` | array | 关联事件 ID |
| `tags` | array | 自定义标签 |

#### 4.2 每日统计（daily-stat）

```jsonl
{"date": "2026-04-13", "region": "ukraine", "events_total": 47, "events_by_type": {"battle": 18, "explosion": 12, "protest": 2, "civilian_violence": 8, "other": 7}, "fatalities_total": 156, "fatalities_civilians": 34, "fatalities_military": 122, " hottest_location": [{"place": "巴赫穆特", "count": 8}, {"place": "马里乌波尔", "count": 5}], "trending_topics": ["无人机袭击", "弹药库爆炸"], "last_updated": "2026-04-13T23:59:00Z"}
```

#### 4.3 事件类型分类

| event_type | 说明 |
|------------|------|
| `battle` | 武装交火/战斗 |
| `explosion` | 爆炸（地雷、炮弹、炸弹） |
| `aerial_strike` | 空袭 |
| `missile_attack` | 导弹攻击 |
| `drone_strike` | 无人机袭击 |
| `civilian_violence` | 平民暴力（杀害、绑架） |
| `protest` | 抗议/游行 |
| `riot` | 骚乱 |
| `remote_violence` | 远程火力打击 |
| `strategic_development` | 战略进展（领土变化等） |

#### 4.4 来源索引（source-index）

```jsonl
{"source_id": "gdelt", "name": "GDELT Project", "url": "https://www.gdeltproject.org/", "license": "CC BY-NC 4.0", "update_frequency": "daily", "coverage": "全球", "api_endpoint": "https://api.gdeltproject.org/api/v2/doc/doc?format=json"}
{"source_id": "acled", "name": "Armed Conflict Location & Event Data", "url": "https://acleddata.com/", "license": "ACLED Free Tier", "update_frequency": "real-time", "coverage": "全球 150+ 国家和地区"}
```

---

## 5. API 设计

### 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/api/events` | 获取事件列表，支持过滤 |
| `GET` | `/api/stats/{region}/{date}` | 获取某地区某日统计 |
| `GET` | `/api/map/{region}` | 获取地图数据 |
| `GET` | `/api/timeline/{region}` | 获取时间线数据 |
| `GET` | `/api/daily-summary` | 获取全球今日简报 |

### 查询参数（events）

```
?region=ukraine
&start_date=2026-04-01
&end_date=2026-04-13
&event_type=battle
&min_fatalities=10
&page=1&page_size=50
```

---

## 6. 前端页面设计

### 页面 1：首页 / 全球战况总览

```
┌─────────────────────────────────────────────┐
│  🔥 全球战争日报                  [今日日期] │
├─────────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │ 47      │ │ 156     │ │ 34      │       │
│  │ 今日事件 │ │ 今日死亡 │ │ 平民伤亡 │       │
│  └─────────┘ └─────────┘ └─────────┘       │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │         世界地图（热力图）           │   │
│  │     用 Mapbox 标记冲突地点           │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  📊 今日最热地区                            │
│  🔴 乌克兰东部  ·  18 事件                 │
│  🟠 加沙地带    ·  12 事件                 │
│  🟡 苏丹达尔富尔·  8 事件                  │
└─────────────────────────────────────────────┘
```

### 页面 2：地区详情（俄乌战争）

```
┌─────────────────────────────────────────────┐
│  🇺🇦 俄乌战争日报                [选择日期] │
├─────────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐   │
│  │        战役地图（Mapbox）            │   │
│  │   点击标记查看事件详情                │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  📍 今日新增事件：47 件                     │
│  ┌─────────────────────────────────────┐   │
│  │ ● 14:32  巴赫穆特  空袭  死亡 12    │   │
│  │ ● 13:15  马里乌波尔  炮击  死亡 5   │   │
│  │ ● 11:00  扎波罗热  无人机袭击  死亡 3│   │
│  └─────────────────────────────────────┘   │
│                                             │
│  📈 近 30 天趋势（Recharts 折线图）        │
└─────────────────────────────────────────────┘
```

### 页面 3：数据下载 / 订阅

```
┌─────────────────────────────────────────────┐
│  📥 数据订阅                                │
├─────────────────────────────────────────────┤
│  免费用户：访问公开页面                      │
│  付费订阅（计划设计）：                     │
│  ┌────────┐ ┌────────┐ ┌────────┐        │
│  │ FREE   │ │ PRO    │ │ ENTER. │        │
│  │ ¥0/月  │ │ ¥29/月 │ │ ¥99/月 │        │
│  │ 公开页面│ │ API访问│ │ 全量数据│        │
│  └────────┘ └────────┘ └────────┘        │
└─────────────────────────────────────────────┘
```

### UI 组件清单（shadcn/ui）

| 组件 | 用途 |
|------|------|
| `Card` | 数据统计卡片 |
| `Badge` | 事件类型标签 |
| `Button` | 操作按钮 |
| `Select` | 日期/地区选择 |
| `Tabs` | 切换视图（地图/列表/统计） |
| `ScrollArea` | 事件列表滚动区域 |
| `Table` | 桌面端事件表格 |
| `Avatar` | 涉事方图标 |
| `Progress` | 伤亡进度条 |
| `Separator` | 分隔线 |

---

## 7. 数据更新流程（CI/CD）

```
1. GitHub Actions 定时触发（每日 08:00 UTC）
   └─> 触发 Python 脚本

2. Python 数据脚本执行：
   ├─> 从 GDELT API 拉取过去 24h 数据
   ├─> 从 ACLED 免费层拉取增量数据
   ├─> 数据清洗 + 转换格式
   ├─> 追加写入 data/conflicts/{region}-{YYYY-MM}.jsonl
   ├─> 更新 data/stats/{region}-daily.jsonl
   └─> 更新 data/sources/source-index.jsonl

3. GitHub Actions 自动 commit + push
   └─> Vercel 检测到仓库更新
       └─> 重新部署前端 + API

预计执行时间：3-5 分钟
执行频率：每日 1 次（MVP 阶段）
```

---

## 8. MVP 开发计划

### 第一周：基础设施
- [ ] 初始化 Next.js 项目（Vercel 部署）
- [ ] 配置 GitHub Actions 数据更新流水线
- [ ] 搭建 Python FastAPI 后端
- [ ] 设计 JSONL 数据结构和目录

### 第二周：数据层
- [ ] 对接 GDELT API（俄乌关键词过滤）
- [ ] 对接 ACLED 免费层
- [ ] 数据清洗脚本
- [ ] JSONL 写入和读取逻辑

### 第三周：前端
- [ ] 首页 UI（shadcn/ui + Tailwind）
- [ ] Mapbox 地图集成
- [ ] 事件列表页面
- [ ] 统计图表（Recharts）

### 第四周：API + 细节
- [ ] FastAPI 端点开发
- [ ] 前后端联调
- [ ] 响应式适配
- [ ] 错误处理和日志

### 第五周：上线 & 验证
- [ ] 域名绑定
- [ ] MVP 发布
- [ ] 收集用户反馈
- [ ] 确定第二阶段方向

---

## 9. 成本估算（MVP 阶段）

| 项目 | 方案 | 费用 |
|------|------|------|
| 前端部署 | Vercel Hobby | **$0** |
| 后端 API | Vercel Serverless Functions | **$0** |
| 数据存储 | GitHub Repository | **$0** |
| 地图 | Mapbox 免费层（5 万次/月） | **$0** |
| 数据源 | GDELT + ACLED 免费 | **$0** |
| 域名 | 可选 | **$0** |
| **合计** | | **$0** |

> MVP 阶段完全免费跑通。付费点：Mapbox 超量、ACLED 全量数据、用户量上来后的 Vercel 升级。

---

## 10. 潜在挑战 & 应对

| 挑战 | 应对 |
|------|------|
| GDELT 数据延迟（天级） | 补充 ACLED 实时数据 + 人工审核通道 |
| 数据可信度参差不齐 | 用 `confidence` 字段标记，前端按可信度过滤 |
| Mapbox 国内访问不稳定 | 备选：百度地图 JS SDK / 纯文字事件列表 |
| 俄乌以外地区数据稀疏 | MVP 先只做俄乌，第二阶段再扩 |
| Vercel Serverless 冷启动慢 | 缓存 + 预热策略 |

---

## 11. 下一步行动

1. **确认 MVP 范围**：是否先只做俄乌战争？
2. **Mapbox 账号**：需要申请一个免费 API Key
3. **GDELT API 测试**：确认能拉到俄乌数据
4. **开工**：我来帮你搭项目结构？

---

*文档版本：v1.0*
*日期：2026-04-13*
