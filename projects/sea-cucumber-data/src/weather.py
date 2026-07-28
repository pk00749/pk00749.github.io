"""天气影响分析模块"""
import pandas as pd
import numpy as np
from scipy import stats
from src.database import get_production_data, get_weather_data, get_weather_events_from_db

# 行业经验值（当数据不足时使用）
DEFAULT_TEMP_ELASTICITY = -8.5   # 水温每升高1℃，亩产下降约8.5斤
DEFAULT_TYPHOON_PRICE_EFFECT = 3.2  # 每次台风，价格上涨约3.2元/斤

def get_weather_impact():
    """
    分析天气事件对产量和价格的影响
    返回：弹性系数字典
    """
    try:
        prod_df = get_production_data(2013, 2024)
        weather_df = get_weather_data(2013, 2024)
        
        # 合并数据
        merged = prod_df.merge(weather_df, on='year', how='left')
        national = merged[merged['province'].isna() | (merged['province'] == '全国')]
        
        # 高温弹性计算
        if 'summer_water_temp_anomaly' in national.columns and not national['summer_water_temp_anomaly'].isna().all():
            valid = national.dropna(subset=['yield_per_mu', 'summer_water_temp_anomaly'])
            if len(valid) > 3:
                # 计算弹性
                temp_corr = valid['yield_per_mu'].corr(valid['summer_water_temp_anomaly'])
                temp_std = valid['yield_per_mu'].std()
                anomaly_std = valid['summer_water_temp_anomaly'].std()
                if anomaly_std > 0:
                    temp_elasticity = temp_corr * temp_std / anomaly_std
                else:
                    temp_elasticity = DEFAULT_TEMP_ELASTICITY
            else:
                temp_elasticity = DEFAULT_TEMP_ELASTICITY
        else:
            temp_elasticity = DEFAULT_TEMP_ELASTICITY
        
        return {
            'temp_elasticity': round(temp_elasticity, 1),
            'typhoon_price_effect': DEFAULT_TYPHOON_PRICE_EFFECT,
            'data_availability': 'real' if temp_elasticity != DEFAULT_TEMP_ELASTICITY else 'estimated'
        }
    except Exception as e:
        print(f"天气影响分析失败: {e}")
        return {
            'temp_elasticity': DEFAULT_TEMP_ELASTICITY,
            'typhoon_price_effect': DEFAULT_TYPHOON_PRICE_EFFECT,
            'data_availability': 'estimated'
        }

def get_weather_events(start_year, end_year):
    """获取天气事件列表"""
    try:
        return get_weather_events_from_db(start_year, end_year)
    except Exception as e:
        print(f"获取天气事件失败: {e}")
        return pd.DataFrame()

def get_seasonal_weather_pattern():
    """
    获取季节性天气模式
    海参养殖关键期：3-6月（春参生长期）、9-11月（秋参收获期）
    """
    return {
        'spring': {
            'period': '3-6月',
            'key_concern': '水温回升速度、赤潮',
            'impact': '决定春参产量'
        },
        'summer': {
            'period': '7-8月',
            'key_concern': '高温、台风',
            'impact': '主要风险期，产量波动大'
        },
        'autumn': {
            'period': '9-11月',
            'key_concern': '台风尾、降温速度',
            'impact': '决定秋参上市量'
        },
        'winter': {
            'period': '12-2月',
            'key_concern': '冰冻、海参冬眠',
            'impact': '产量最低，价格最高'
        }
    }

def simulate_weather_scenario(temp_anomaly, typhoon_count, red_tide_area):
    """
    模拟天气情景对产量的影响
    用于快速评估天气条件变化的影响
    """
    impact = get_weather_impact()
    
    # 产量影响
    output_impact = temp_anomaly * impact['temp_elasticity']
    # 价格影响
    price_impact = typhoon_count * impact['typhoon_price_effect']
    # 赤潮影响（估算）
    red_tide_price_effect = 2.0  # 每1000km2赤潮面积，价格涨2元/斤
    price_impact += (red_tide_area / 1000) * red_tide_price_effect
    
    return {
        'yield_impact_jin_per_mu': round(output_impact, 1),
        'price_impact_yuan_per_jin': round(price_impact, 1),
        'scenario': {
            'temp_anomaly': temp_anomaly,
            'typhoon_count': typhoon_count,
            'red_tide_area_km2': red_tide_area
        }
    }

def get_climate_trend():
    """
    分析气候变化趋势
    返回：水温变化趋势、极端天气频率变化
    """
    weather_df = get_weather_data(2013, 2024)
    if weather_df.empty or 'sea_surface_temp' not in weather_df.columns:
        return {
            'sst_trend': '+0.05℃/年（行业估算）',
            'extreme_weather_frequency': '上升',
            'implication': '海参养殖风险增加，单产波动加大'
        }
    
    valid = weather_df.dropna(subset=['sea_surface_temp'])
    if len(valid) < 5:
        return {
            'sst_trend': '+0.05℃/年（行业估算）',
            'extreme_weather_frequency': '上升',
            'implication': '海参养殖风险增加，单产波动加大'
        }
    
    # 线性趋势
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        valid['year'], valid['sea_surface_temp']
    )
    
    return {
        'sst_trend': f'{slope:+.3f}℃/年',
        'r_squared': round(r_value**2, 3),
        'p_value': round(p_value, 3),
        'extreme_weather_frequency': '上升' if slope > 0 else '稳定',
        'implication': '水温持续偏高，高温减产风险加大' if slope > 0 else '水温趋势稳定'
    }

if __name__ == "__main__":
    print("=== 天气影响系数 ===")
    print(get_weather_impact())
    
    print("\n=== 情景模拟 ===")
    # 模拟高温+1℃，1次台风，500km2赤潮
    print(simulate_weather_scenario(1, 1, 500))
    
    print("\n=== 季节性模式 ===")
    print(get_seasonal_weather_pattern())
    
    print("\n=== 气候变化趋势 ===")
    print(get_climate_trend())
