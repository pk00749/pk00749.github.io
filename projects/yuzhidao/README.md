# 海参行业数据收集平台

自动采集、存储、可视化海参行业历史数据。

## 项目结构

```
sea-cucumber-data/
├── config.yaml              # 配置文件
├── requirements.txt         # Python依赖
├── prd.md                   # 产品需求文档
├── implementation.md        # 实施方案
├── README.md                # 本文件
├── scripts/                 # 数据采集脚本
│   ├── collect_fishery_stats.py
│   ├── collect_customs.py
│   ├── collect_price.py
│   └── collect_fao.py
├── src/                     # 核心模块
│   ├── __init__.py
│   ├── database.py          # 数据库操作
│   ├── parser.py            # 解析工具
│   └── notifier.py          # 告警通知
├── db/                      # 数据库文件
│   └── sea_cucumber.db      # SQLite数据库
├── data/
│   ├── raw/                 # 原始文件备份
│   └── processed/           # 处理后数据
├── dashboard/
│   └── app.py               # Streamlit看板
├── dags/
│   ├── monthly.sh           # 季度调度
│   └── yearly.sh            # 年度调度
└── Makefile                 # 常用命令
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python src/database.py
```

### 3. 启动看板

```bash
streamlit run dashboard/app.py --server.port 8501
```

## 数据指标

| 指标 | 单位 | 更新频率 |
|-----|------|---------|
| 全国海参产量 | 万吨 | 年 |
| 各省产量 | 万吨 | 年 |
| 养殖面积 | 万公顷 | 年 |
| 苗种产量 | 亿头 | 年 |
| 价格（鲜活/干参/即食） | 元/斤 | 季度 |
| 进出口数据 | 吨/万美元 | 年 |

## 数据来源

- 农业农村部渔业渔政管理局 (yyj.moa.gov.cn)
- 中国海关总署统计 (stats.customs.gov.cn)
- FAO FishStat (fao.org/fishery/fishstat)
- 中国统计年鉴 (stats.gov.cn)

## 调度任务

| 任务 | 时间 | 说明 |
|-----|------|------|
| 年度采集 | 每年7月15日 | 渔业统计公报 |
| 海关数据 | 每年1月5日 | 上年度进出口 |
| 价格采集 | 每季度15日 | 市场批发价 |

## 开发命令

```bash
make help          # 查看所有命令
make collect-year  # 执行年度采集
make collect-price # 执行价格采集
make dashboard     # 启动看板
make db-init       # 初始化数据库
```
