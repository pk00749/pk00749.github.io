# 海参行业数据收集平台 PRD

> 为积累海参行业历史数据而设计的数据采集、存储与展示方案

---

## 一、项目背景与目标

### 1.1 为什么做

海参行业缺乏统一、持续的历史数据积累平台：
- 官方数据分散在年鉴、统计公报里，格式不一，难以对比
- 行业分析需要多年连续数据，而非单点快照
- 数据源更新频率固定（每年一次），适合做自动化采集

### 1.2 目标

搭建一个可持续运行的数据管道，自动从多个官方/权威渠道采集海参行业数据，存入本地历史数据库，并支持可视化展示和导出。

---

## 二、数据范围

### 2.1 核心数据指标

| 指标分类 | 具体指标 | 单位 | 更新频率 |
|---------|---------|------|---------|
| **生产端** | 全国海参总产量 | 万吨 | 年 |
| | 各省海参产量 | 万吨 | 年 |
| | 全国养殖面积 | 万公顷/万亩 | 年 |
| | 各省养殖面积 | 万公顷 | 年 |
| | 全国苗种产量 | 亿头 | 年 |
| | 各省苗种产量 | 亿头 | 年 |
| | 平均亩产 | 斤/亩 | 年 |
| | 各省亩产 | 斤/亩 | 年 |
| **价格端** | 产地收购价（鲜活） | 元/斤 | 季 |
| | 批发市场价 | 元/斤 | 月/季 |
| | 加工品（干参、即食）价格 | 元/斤 | 季 |
| **贸易端** | 进口量/进口额 | 吨/万美元 | 年 |
| | 出口量/出口额 | 吨/万美元 | 年 |
| **行业端** | 产业规模（总产值） | 亿元 | 年 |
| | 主要企业动态 | 条 | 季 |
| **环境端** | 沿海水温异常 | 事件记录 | 季 |
| | 赤潮/病害事件 | 事件记录 | 事件驱动 |

### 2.2 时间范围

- 历史回溯：2013年至今（中国渔业统计年鉴最早可查到约2013年的海参专项数据）
- 实时新增：每年自动采集新增数据

### 2.3 地域维度

- 全国汇总数据
- 主要产区：辽宁、山东、福建、河北（霞浦）、江苏、广东

---

## 三、数据源梳理

### 3.1 官方权威源

| 数据源 | 网址 | 更新频率 | 数据类型 | 获取难度 |
|-------|------|---------|---------|---------|
| 农业农村部渔业渔政管理局 | yyj.moa.gov.cn | 年（6-7月） | 生产端全量 | 免费公开 |
| 《中国渔业统计年鉴》 | 出版发行 | 年（7月） | 生产端全量+财务 | 需购买PDF |
| 国家统计局-中国统计年鉴 | stats.gov.cn | 年（2月） | 少量渔业数据 | 免费公开 |
| 中国海关总署 | stats.customs.gov.cn | 月/年 | 进出口数据 | 免费公开 |
| FAO FishStat | fao.org/fishery/fishstat | 年 | 全球对比数据 | 免费API |

### 3.2 行业媒体源

| 数据源 | 网址 | 更新频率 | 数据类型 |
|-------|------|---------|---------|
| 食品伙伴网-海参专栏 | foodmate.net | 事件驱动 | 行业分析、价格 |
| 中渔协海参产业分会 | 微信公众号 | 不定期 | 产业动态 |
| 海鲜指南 | seaguide.cn | 事件驱动 | 价格、流通 |

### 3.3 数据源优先级

```
P0（必采）: 农业农村部年鉴/公报、海关总署
P1（重要）: FAO数据、价格采集（网站爬虫）
P2（可选）: 行业媒体资讯、天气事件
```

---

## 四、系统架构

```
┌─────────────────────────────────────────────────────┐
│                    数据采集层                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │年鉴采集器│  │海关API  │  │价格爬虫 │  │FAO API  │ │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘ │
│       │            │            │            │       │
│       └────────────┴─────┬──────┴────────────┘       │
└──────────────────────────┼───────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────┐
│                    数据存储层                         │
│  ┌──────────────┐    ┌──────────────┐              │
│  │  PostgreSQL  │    │   CSV/JSON   │              │
│  │  (结构化数据) │    │  (原始备份)  │              │
│  └──────────────┘    └──────────────┘              │
└─────────────────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────┐
│                    数据应用层                         │
│  ┌─────────┐  ┌─────────────┐  ┌───────────────┐   │
│  │可视化看板│  │ API接口查询  │  │ 数据导出(CSV) │   │
│  └─────────┘  └─────────────┘  └───────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 五、功能模块

### 5.1 数据采集模块

**年鉴数据采集器**
- 目标：自动从 yyj.moa.gov.cn 采集年度统计公报
- 输入：目标URL列表 + XPath/CSS选择器规则
- 输出：结构化JSON/CSV原始文件
- 维护：每年6-7月检查一次选择器是否失效

**海关数据采集器**
- 目标：自动从海关总署统计网站获取海参相关进出口数据
- 方式：HTTP请求 + JSON解析
- 字段：商品编码（0308开头）、贸易量、贸易额、贸易伙伴国

**价格数据采集器**
- 目标：定期抓取行业网站鲜活海参价格
- 频率：每季度一次
- 防封：随机User-Agent + 请求间隔

**FAO数据采集器**
- 目标：通过FAO API获取全球海参贸易数据
- 方式：HTTP API调用

### 5.2 数据存储模块

**数据库设计**

```sql
-- 产量数据表
CREATE TABLE production (
    id SERIAL PRIMARY KEY,
    year INT NOT NULL,                    -- 数据年份
    province VARCHAR(50),                 -- 省份，NULL表示全国
    output_tons DECIMAL(10,2),            -- 产量（吨）
    area_hectare DECIMAL(10,2),           -- 养殖面积（公顷）
    seedlings_billion INT,                -- 苗种产量（亿头）
    yield_per_mu DECIMAL(8,2),            -- 亩产（斤/亩）
    source VARCHAR(100),                  -- 数据来源
    url TEXT,                             -- 原始链接
    created_at TIMESTAMP DEFAULT NOW()
);

-- 价格数据表
CREATE TABLE price (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,                   -- 价格日期
    region VARCHAR(50),                   -- 地区
    product_type VARCHAR(50),             -- 产品类型（鲜活/干参/即食）
    price_yuan_per_jin DECIMAL(8,2),      -- 价格（元/斤）
    source VARCHAR(100),
    url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 进出口数据表
CREATE TABLE trade (
    id SERIAL PRIMARY KEY,
    year INT NOT NULL,
    month INT,                            -- 月度数据时记录
    direction VARCHAR(10),                -- 'import' or 'export'
    quantity_tons DECIMAL(12,2),
    amount_usd DECIMAL(14,2),
    partner_country VARCHAR(100),
    source VARCHAR(100),
    url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 历史原始文件表
CREATE TABLE raw_files (
    id SERIAL PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    year INT,
    file_path TEXT NOT NULL,              -- 存储路径
    file_type VARCHAR(20),                -- json/csv/html/pdf
    url TEXT,
    hash VARCHAR(64),                     -- 文件校验
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 5.3 可视化展示模块

**看板功能**
- 年份选择器（2013-当前年）
- 产量趋势折线图（全国 + 分省）
- 养殖面积趋势图
- 亩产对比柱状图
- 苗种产量趋势
- 进出口趋势（可选）

**数据导出**
- 支持按指标+年份范围导出CSV
- 支持导出完整历史数据压缩包

### 5.4 预测推算模块

**基于历史数据的趋势推算**
- 目标：用历史产量、价格数据，建立时间序列预测模型
- 用途：
  - 产量预测：为来年产量提供参考区间
  - 价格预测：基于产量 + 季节 + 历史价格走势预测价格区间
  - 缺口分析：供需缺口推算（产量 vs 消费量估算）

**模型方法**
| 场景 | 方法 | 适用数据量 |
|-----|------|----------|
| 产量趋势预测 | 线性回归 / ARIMA | 10年以上 |
| 价格预测 | 多元回归（产量+季节+原料） | 5年以上 |
| 季节性波动 | 季节性分解（STL） | 3年以上 |
| 异常检测 | Isolation Forest / 3σ原则 | 任意 |

**推算输出**
- 来年产量预测值 + 80%置信区间
- 下季度价格预测值 + 波动范围
- 同比/环比增长率预测
- 异常年份标注（高温/赤潮/疫情等）

---

### 5.5 天气影响分析模块

**核心假设**：海参养殖受水温、台风、赤潮等气象事件显著影响

**天气数据源**
| 数据源 | 指标 | 获取方式 |
|-------|------|---------|
| 国家气象科学数据中心 | 水温、降水、台风 | API申请/CSV下载 |
| NOAA | 西北太平洋海温（SST） | 免费API |
| 中国台风网 | 台风路径、登陆点 | 网页爬虫 |
| 沿海省份海洋预报台 | 赤潮预警 | 定期抓取 |

**分析维度**
| 分析项 | 说明 | 方法 |
|-------|------|------|
| 高温减产关联 | 夏季水温>30℃持续天数 vs 亩产 | 相关性分析 |
| 台风损失评估 | 台风路径经过产区 vs 产量损失 | 事件研究法 |
| 赤潮影响分析 | 赤潮发生面积 vs 产区减产 | 回归分析 |
| 价格波动归因 | 天气事件 vs 价格异常涨幅 | 脉冲响应 |

**输出**
- 天气-产量弹性系数（高温每升1℃产量降多少%）
- 天气-价格弹性系数（台风每起价格涨多少%）
- 天气事件标注层叠加在趋势图上
- 赤潮/高温预警推送（当水温异常时）

---

### 5.6 告警与维护模块

- 每年数据更新季（6-7月）自动提醒采集
- 采集失败告警（钉钉/飞书webhook）
- 数据空值/异常检测
- 水温/赤潮异常告警（触发阈值后推送）

---

## 六、技术选型

| 组件 | 选型 | 理由 |
|-----|------|------|
| 采集语言 | Python | 爬虫生态成熟，requests + BeautifulSoup + selenium |
| 数据库 | PostgreSQL / SQLite | 轻量级开发，SQLite足够早期使用 |
| 预测模型 | Python statsmodels / scikit-learn | 时间序列+回归分析 |
| 天气数据 | requests + 气象API | 水温/台风数据获取 |
| 数据格式 | CSV + JSON | 原始备份，跨平台 |
| 看板 | Streamlit / Gradio | 快速开发，数据可视化天然集成 |
| 调度 | cron + shell脚本 | 简单可靠，不需要额外框架 |
| 部署 | 本地服务器 | 数据量小，本地运行即可 |

---

## 七、更新节奏

| 数据类型 | 采集频率 | 执行时间 |
|---------|---------|---------|
| 渔业统计年鉴/公报 | 每年一次 | 每年7月15日后 |
| 海关进出口数据 | 每年一次 | 每年1月（补齐上年度） |
| 价格数据 | 每季度一次 | 1/4/7/10月15日 |
| FAO全球数据 | 每年一次 | 每年10月 |

---

## 八、MVP范围

第一期只做最核心的：

1. **手动采集** 历史年鉴数据（2013-2024），清洗入库
2. **自动采集** 农业农村部年度统计公报（每年7月）
3. **数据库** SQLite，3张核心表（production/trade/price）
4. **展示** Streamlit单页看板，支持年份筛选和图表
5. **导出** CSV导出功能

---

## 九、ROI估算

**投入**：
- 开发：约2-3天（Python采集器 + Streamlit看板）
- 维护：每年约4-6小时（更新采集）

**产出**：
- 历史数据资产沉淀，随时可查
- 为后续行业分析报告、定价模型打下基础
- 可复用到其他水产品种（扇贝、鲍鱼等）

---

## 十、预测模型设计

### 10.1 产量预测模型

```python
# 伪代码：ARIMA产量预测
from statsmodels.tsa.arima.model import ARIMA

def predict_output(history_df, forecast_years=1):
    """
    history_df: 包含year, output_tons的历史数据
    return: 预测值 + 置信区间
    """
    ts = history_df.set_index('year')['output_tons']
    model = ARIMA(ts, order=(1, 1, 1))
    result = model.fit()
    forecast = result.get_forecast(steps=forecast_years)
    return forecast.predicted_mean, forecast.conf_int()
```

### 10.2 价格预测模型

```python
# 伪代码：多元回归价格预测
# 特征：产量、季节（Q1-Q4）、去年价格、台风标志

features = ['output_tons', 'season_q', 'last_year_price', 'typhoon_flag']
model = LinearRegression()
model.fit(X_train, y_train)  # y = 价格

# 预测下季度价格
price_pred = model.predict(X_next)
```

### 10.3 天气-产量弹性模型

```python
# 伪代码：高温对亩产的影响
# 变量：夏季平均水温异常值、台风经过次数、赤潮面积

elasticity = df['yield_per_mu'].corr(df['summer_water_temp_anomaly'])
# 水温每升1℃，亩产下降约 X 斤
```

---

## 十一、天气事件数据表

```sql
-- 天气事件表
CREATE TABLE weather_events (
    id SERIAL PRIMARY KEY,
    event_date DATE NOT NULL,
    event_type VARCHAR(50),               -- 'typhoon'/'red_tide'/'high_temp'/'disease'
    region VARCHAR(50),                   -- 涉及产区
    severity VARCHAR(20),                 -- 'warning'/'moderate'/'severe'
    description TEXT,                     -- 事件描述
    source VARCHAR(100),
    url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 气象数据表
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    region VARCHAR(50),
    sea_surface_temp DECIMAL(5,2),        -- 海表水温（℃）
    air_temp DECIMAL(5,2),                -- 气温（℃）
    precipitation_mm DECIMAL(6,2),        -- 降水量（mm）
    typhoon_count INT,                    -- 当月台风数
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

*PRD版本：v1.1 — 新增预测模型 + 天气影响分析*
*创建时间：2026-07-27*
*创建时间：2026-07-27*
