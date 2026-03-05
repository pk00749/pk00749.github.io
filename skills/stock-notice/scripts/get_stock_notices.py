#!/usr/bin/env python3
"""
获取股票公告详情，并抓取每个公告页面的内容
用于监控股票公告时获取详细信息
"""

import akshare as ak
from datetime import datetime, timedelta
import json
import argparse
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_stock_notice_by_code(stock_code: str, days_back: int = 3) -> dict:
    """获取指定股票代码的最近公告"""
    stock_code = stock_code.strip().upper()
    
    # 标准化股票代码：6位数字
    stock_code_6 = stock_code.zfill(6)  # 000533 -> 000533, 600499 -> 600499
    
    result = {
        "code": stock_code,
        "notices": [],
        "error": None
    }
    
    for i in range(days_back):
        check_date = (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
        try:
            df = ak.stock_notice_report(symbol="全部", date=check_date)
            if df is not None and len(df) > 0 and '代码' in df.columns:
                # 精确匹配6位股票代码
                stock_df = df[df['代码'].astype(str).str.zfill(6) == stock_code_6]
                if len(stock_df) > 0:
                    result["date"] = check_date
                    result["notices"] = stock_df.to_dict('records')
                    break
        except Exception as e:
            continue
    
    if not result["notices"]:
        result["error"] = f"未找到 {stock_code} 的公告（最近{days_back}天）"
    
    return result


def check_and_notify_stock(stock_code: str, days_back: int = 3) -> dict:
    """
    检查股票是否有新公告，如果有则返回详细信息
    用于定时任务推送
    """
    result = get_stock_notice_by_code(stock_code, days_back)
    
    if result["error"]:
        return {"has_news": False, "message": result["error"]}
    
    # 检查是否有今天或昨天的公告（最近2天）
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    recent_notices = []
    for notice in result["notices"]:
        notice_date = str(notice.get('公告日期', ''))
        if today in notice_date or yesterday in notice_date:
            recent_notices.append(notice)
    
    if not recent_notices:
        return {"has_news": False, "message": f"{stock_code} 近期无新公告"}
    
    # 有新公告，返回详细信息
    return {
        "has_news": True,
        "code": stock_code,
        "notices": recent_notices,
        "count": len(recent_notices)
    }


def main():
    parser = argparse.ArgumentParser(description='股票公告查询')
    parser.add_argument('--code', '-c', type=str, default=None,
                        help='股票代码，如 600499')
    parser.add_argument('--days', '-d', type=int, default=3,
                        help='查询天数，默认3天')
    parser.add_argument('--detail', '-v', action='store_true',
                        help='显示详细公告内容（需要网络请求，可能较慢）')
    
    args = parser.parse_args()
    
    if not args.code:
        print("请指定股票代码: -c 600499")
        return
    
    result = get_stock_notice_by_code(args.code, args.days)
    
    if result["error"]:
        print(result["error"])
        return
    
    print(f"📌 {result['code']} 公告（{result.get('date', 'N/A')}）")
    print(f"共 {len(result['notices'])} 条\n")
    
    # 检查是否有今天/昨天的公告
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    for n in result["notices"]:
        notice_date = str(n.get('公告日期', ''))
        is_new = today in notice_date or yesterday in notice_date
        new_tag = "🆕 " if is_new else ""
        
        print(f"{new_tag}• [{n['公告类型']}] {n['公告标题']}")
        print(f"  日期: {n['公告日期']} | 链接: {n['网址']}")
        print()
        
        # 如果需要详细内容和总结
        if args.detail and is_new:
            print("  📄 页面内容抓取需要额外请求，请使用 web_fetch 工具获取详情")
            print()
    
    # 统计公告类型
    types = {}
    for n in result["notices"]:
        t = n['公告类型']
        types[t] = types.get(t, 0) + 1
    
    print("📊 公告类型统计:")
    for t, cnt in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t}: {cnt}条")


if __name__ == "__main__":
    main()
