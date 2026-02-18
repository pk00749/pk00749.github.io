#!/usr/bin/env python3
"""
获取股票公告
- 默认获取当天/最近有公告的股票列表
- 支持指定股票代码查询最近公告
"""

import akshare as ak
from datetime import datetime, timedelta
import json
import argparse

def get_recent_notices(days_back: int = 5) -> dict:
    """获取最近几天有公告的股票"""
    today = datetime.now().strftime('%Y%m%d')
    
    # 尝试获取最近几天直到有数据
    for i in range(days_back + 1):
        check_date = (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
        try:
            df = ak.stock_notice_report(symbol="全部", date=check_date)
            if df is not None and len(df) > 0 and '代码' in df.columns:
                return {
                    "date": check_date,
                    "count": len(df),
                    "stocks": df[['代码', '名称']].drop_duplicates().to_dict('records')
                }
        except:
            continue
    
    return {"error": "无法获取公告数据"}


def get_stock_notice_by_code(stock_code: str, days_back: int = 30) -> dict:
    """获取指定股票代码的最近公告"""
    stock_code = stock_code.strip().upper()
    
    # 最近几天有公告的股票
    result = {
        "code": stock_code,
        "notices": [],
        "error": None
    }
    
    # 尝试获取最近几天的数据
    for i in range(days_back):
        check_date = (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
        try:
            df = ak.stock_notice_report(symbol="全部", date=check_date)
            if df is not None and len(df) > 0 and '代码' in df.columns:
                # 筛选指定股票
                stock_df = df[df['代码'].astype(str).str.contains(stock_code.lstrip('0'))]
                if len(stock_df) > 0:
                    result["date"] = check_date
                    result["notices"] = stock_df.to_dict('records')
                    break
        except Exception as e:
            continue
    
    if not result["notices"]:
        result["error"] = f"未找到 {stock_code} 的公告（最近{days_back}天）"
    
    return result


def main():
    parser = argparse.ArgumentParser(description='股票公告查询')
    parser.add_argument('--code', '-c', type=str, default=None,
                        help='股票代码，如 600499')
    parser.add_argument('--days', '-d', type=int, default=30,
                        help='查询天数，默认30天')
    
    args = parser.parse_args()
    
    if args.code:
        # 查询指定股票
        result = get_stock_notice_by_code(args.code, args.days)
        if result["error"]:
            print(result["error"])
            return
        
        print(f"📌 {result['code']} 公告（{result.get('date', 'N/A')}）")
        print(f"共 {len(result['notices'])} 条\n")
        
        for n in result["notices"]:
            print(f"• [{n['公告类型']}] {n['公告标题'][:50]}...")
            print(f"  日期: {n['公告日期']} | 链接: {n['网址']}")
            print()
    else:
        # 获取最近有公告的股票
        result = get_recent_notices()
        if "error" in result:
            print(result["error"])
            return
        
        print(f"📊 {result['date']} 有公告的股票")
        print(f"共 {result['count']} 条公告，{len(result['stocks'])} 只股票\n")
        
        stocks = sorted(result['stocks'], key=lambda x: str(x['代码']))
        for s in stocks:
            print(f"{s['代码']:>6}  {s['名称']}")


if __name__ == "__main__":
    main()
