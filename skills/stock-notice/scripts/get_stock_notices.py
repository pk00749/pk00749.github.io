#!/usr/bin/env python3
"""
获取当天有公告更新的股票代号和名称
使用 akshare 的 stock_notice_report API
"""

import akshare as ak
from datetime import datetime, timedelta
import argparse


def get_stock_notices(date: str = None, symbol: str = "全部") -> list:
    """
    获取指定日期的股票公告
    
    Args:
        date: 日期，格式 YYYYMMDD，默认为今天
        symbol: 公告类型，默认为全部
    
    Returns:
        股票列表 [(代码, 名称), ...]
    """
    # 如果没有指定日期，默认获取今天
    if date is None:
        date = datetime.now().strftime('%Y%m%d')
    
    # 尝试获取数据，如果失败则回退到昨天
    try:
        df = ak.stock_notice_report(symbol=symbol, date=date)
        if df is None or len(df) == 0:
            raise ValueError("No data")
    except:
        # 回退到昨天
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        print(f"当天无数据，回退到昨天: {yesterday}")
        date = yesterday
        df = ak.stock_notice_report(symbol=symbol, date=date)
    
    if df is None or len(df) == 0:
        return []
    
    # 提取股票代码和名称，去重
    stocks = df[['代码', '名称']].drop_duplicates()
    stocks = stocks.sort_values('代码')
    
    return stocks.values.tolist()


def main():
    parser = argparse.ArgumentParser(description='获取当天有公告更新的股票')
    parser.add_argument('--date', '-d', type=str, default=None, 
                        help='日期，格式 YYYYMMDD，默认为今天')
    parser.add_argument('--symbol', '-s', type=str, default='全部',
                        choices=['全部', '重大事项', '财务报告', '融资公告', '风险提示', '资产重组', '信息变更', '持股变动'],
                        help='公告类型')
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='输出文件路径')
    
    args = parser.parse_args()
    
    print(f"正在获取公告数据...")
    stocks = get_stock_notices(date=args.date, symbol=args.symbol)
    
    print(f"\n共有 {len(stocks)} 只股票有公告更新:\n")
    print(f"{'代码':<10} {'名称':<15}")
    print("-" * 25)
    
    for code, name in stocks:
        print(f"{code:<10} {name:<15}")
    
    # 如果指定了输出文件，保存到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"日期: {args.date or datetime.now().strftime('%Y%m%d')}\n")
            f.write(f"公告类型: {args.symbol}\n")
            f.write(f"股票数量: {len(stocks)}\n\n")
            f.write(f"{'代码':<10} {'名称':<15}\n")
            f.write("-" * 25 + "\n")
            for code, name in stocks:
                f.write(f"{code:<10} {name:<15}\n")
        print(f"\n已保存到: {args.output}")


if __name__ == "__main__":
    main()
