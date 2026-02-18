---
name: stock-notice
description: 获取A股当天有公告更新的股票列表。使用 akshare 的 stock_notice_report API。当用户询问股票公告、今日有公告的股票、哪些股票今天发公告了时使用此 skill。
---

# Stock Notice - 股票公告查询

## 功能

获取指定日期/类型有公告更新的 A 股股票代码和名称列表，自动去重。

## 使用方法

```bash
python3 scripts/get_stock_notices.py [选项]
```

### 选项

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--code` | `-c` | 股票代码，查询指定股票 | - |
| `--days` | `-d` | 查询天数（配合 --code 使用） | 30 |
| `--date` | - | 指定日期 (YYYYMMDD)，查询当天公告 | - |
| (无参数) | | 获取最近有公告的股票列表 | - |

### 公告类型 (symbol)

- `全部` - 所有公告
- `重大事项`
- `财务报告`
- `融资公告`
- `风险提示`
- `资产重组`
- `信息变更`
- `持股变动`

## 示例

```bash
# 获取今天全部公告
python3 scripts/get_stock_notice.py

# 获取今天的财务报告公告
python3 scripts/get_stock_notice.py -s 财务报告

# 获取指定日期的公告
python3 scripts/get_stock_notice.py -d 20260214

# 保存到文件
python3 scripts/get_stock_notice.py -o notices.txt
```

## 输出格式

```
日期: 20260214
公告类型: 全部
股票数量: 992

代码        名称           
-------------------------
300344      *ST立方        
002713      *ST东易        
...
```
