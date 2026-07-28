"""天气数据采集器 - NOAA水温 + 台风数据"""
import requests
import pandas as pd
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import save_weather_data, save_weather_event
import yaml

# 加载配置
CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"
with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

WEATHER_CFG = config.get('weather', {})
ALERT_CFG = config.get('alert_thresholds', {})

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
]

def fetch_noaa_sst(lat, lon, start_date, end_date):
    """
    从NOAA获取海表水温数据
    dataset: OISST (Optimum Interpolation Sea Surface Temperature)
    """
    url = "https://www.ncei.noaa.gov/access/services/data/v1"
    params = {
        "dataset": "OISST",
        "stations": f"{lat},{lon}",
        "startDate": start_date,
        "endDate": end_date,
        "units": "metric",
        "format": "json"
    }
    
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data
    except Exception as e:
        print(f"NOAA SST获取失败: {e}")
        return []

def fetch_typhoon_list(year):
    """
    获取台风列表
    数据源：中国气象局台风网
    """
    # 简化实现：返回模拟数据（实际需解析网页）
    # 真实实现需要爬取 https://typhoon.weather.com.cn
    print(f"[提示] 台风数据采集需要解析网页，当前使用模拟数据")
    return []

def check_red_tide_alerts():
    """
    检查赤潮预警
    数据源：自然资源部海洋预警监测司
    """
    url = "https://www.mnr.gov.cn/"
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        # 实际需要解析赤潮预警页面
        return []
    except Exception as e:
        print(f"赤潮数据获取失败: {e}")
        return []

def process_sst_data(raw_data, station_name):
    """
    处理SST数据，返回年度统计
    """
    if not raw_data:
        return None
    
    df = pd.DataFrame(raw_data)
    if df.empty or 'date' not in df.columns:
        return None
    
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    
    # 计算夏季（6-8月）平均水温异常
    summer = df[(df['date'].dt.month >= 6) & (df['date'].dt.month <= 8)]
    
    if summer.empty:
        return None
    
    # 相对于年均值的异常
    annual_mean = df['value'].mean()
    summer_mean = summer['value'].mean()
    anomaly = summer_mean - annual_mean
    
    return {
        'station': station_name,
        'year': df['year'].iloc[0],
        'annual_mean_temp': round(annual_mean, 2),
        'summer_mean_temp': round(summer_mean, 2),
        'summer_water_temp_anomaly': round(anomaly, 2),
        'data_points': len(df)
    }

def check_alerts(weather_record):
    """
    检查是否触发告警阈值
    """
    alerts = []
    
    # 水温告警
    if weather_record and 'summer_water_temp_anomaly' in weather_record:
        if weather_record['summer_water_temp_anomaly'] > 2:
            alerts.append({
                'type': 'high_temp',
                'severity': 'warning',
                'message': f"水温异常偏高: {weather_record['summer_water_temp_anomaly']}℃"
            })
    
    # 可以扩展其他告警检查
    
    return alerts

def run_weather_collection():
    """
    主函数：采集天气数据
    """
    print("=== 开始采集天气数据 ===")
    
    # 计算上一个完整年份
    current_year = datetime.now().year
    target_year = current_year - 1  # 采集上一年度完整数据
    
    all_records = []
    
    # 采集各站点水温数据
    stations = WEATHER_CFG.get('sources', {}).get('noaa_sst', {}).get('stations', [])
    
    if not stations:
        # 默认站点
        stations = [
            {"name": "大连", "lat": 38.9, "lon": -121.6},
            {"name": "青岛", "lat": 36.1, "lon": -120.4},
            {"name": "霞浦", "lat": 26.9, "lon": -120.0},
        ]
    
    for station in stations:
        print(f"采集站点: {station['name']}")
        
        start_date = f"{target_year}-01-01"
        end_date = f"{target_year}-12-31"
        
        raw_data = fetch_noaa_sst(station['lat'], station['lon'], start_date, end_date)
        processed = process_sst_data(raw_data, station['name'])
        
        if processed:
            all_records.append(processed)
            print(f"  {station['name']}: 年均水温 {processed['annual_mean_temp']}℃, 夏季异常 {processed['summer_water_temp_anomaly']}℃")
        
        time.sleep(random.uniform(2, 5))
    
    # 保存到数据库
    if all_records:
        save_weather_data(all_records)
        print(f"已保存 {len(all_records)} 条天气数据")
    else:
        print("未获取到天气数据")
    
    # 采集台风数据
    print("\n采集台风数据...")
    typhoon_list = fetch_typhoon_list(target_year)
    
    # 检查告警
    if all_records:
        for record in all_records:
            alerts = check_alerts(record)
            for alert in alerts:
                print(f"⚠️ 告警: {alert['message']}")
    
    print("=== 天气数据采集完成 ===")

def run_weather_collection_current():
    """
    采集当年当前数据（用于实时监控）
    """
    print("=== 采集当季度天气数据（实时）===")
    
    now = datetime.now()
    start_date = f"{now.year}-01-01"
    end_date = now.strftime("%Y-%m-%d")
    
    stations = [
        {"name": "大连", "lat": 38.9, "lon": -121.6},
        {"name": "青岛", "lat": 36.1, "lon": -120.4},
        {"name": "霞浦", "lat": 26.9, "lon": -120.0},
    ]
    
    for station in stations:
        print(f"采集: {station['name']}")
        raw_data = fetch_noaa_sst(station['lat'], station['lon'], start_date, end_date)
        processed = process_sst_data(raw_data, station['name'])
        if processed:
            save_weather_data([processed])
            print(f"  完成: {processed}")
        time.sleep(random.uniform(2, 5))

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='海参行业天气数据采集')
    parser.add_argument('--year', type=int, help='指定采集年份')
    parser.add_argument('--current', action='store_true', help='采集当季度实时数据')
    args = parser.parse_args()
    
    if args.current:
        run_weather_collection_current()
    elif args.year:
        # 采集指定年份（需要修改日期范围）
        print(f"采集 {args.year} 年数据")
    else:
        run_weather_collection()
