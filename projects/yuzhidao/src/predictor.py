"""预测模型模块 - 产量预测 + 价格预测"""
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from src.database import get_production_data, get_price_data, get_weather_data

def predict_output(forecast_years=1):
    """
    基于ARIMA的时间序列产量预测
    return: DataFrame with year, predicted, ci_lower, ci_upper
    """
    try:
        from statsmodels.tsa.arima.model import ARIMA
        
        # 获取全国产量历史数据
        df = get_production_data(2013, 2024)
        national = df[df['province'].isna() | (df['province'] == '全国')]
        if national.empty:
            return _default_forecast(forecast_years)
        
        ts = national.set_index('year')['output_tons'].sort_index()
        
        if len(ts) < 5:
            return _default_forecast(forecast_years)
        
        # ARIMA(1,1,1) 模型
        model = ARIMA(ts, order=(1, 1, 1))
        result = model.fit()
        
        # 预测
        forecast = result.get_forecast(steps=forecast_years)
        pred = forecast.predicted_mean
        conf_int = forecast.conf_int(alpha=0.2)  # 80%置信区间
        
        future_years = list(range(ts.index.max() + 1, ts.index.max() + 1 + forecast_years))
        
        return pd.DataFrame({
            'year': future_years,
            'predicted': pred.values,
            'ci_lower': conf_int.iloc[:, 0].values,
            'ci_upper': conf_int.iloc[:, 1].values
        })
    except Exception as e:
        print(f"ARIMA预测失败，使用默认预测: {e}")
        return _default_forecast(forecast_years)

def _default_forecast(forecast_years):
    """默认预测（当数据不足时）"""
    # 基于2024年数据估算：32.6万吨，年增长率约10%
    base = 32.6
    growth_rate = 1.10
    future_years = [2025 + i for i in range(forecast_years)]
    predictions = [base * (growth_rate ** (i + 1)) for i in range(forecast_years)]
    
    return pd.DataFrame({
        'year': future_years,
        'predicted': predictions,
        'ci_lower': [p * 0.85 for p in predictions],
        'ci_upper': [p * 1.15 for p in predictions]
    })

def predict_price():
    """
    基于多元回归的价格预测
    return: dict with value, volatility, next_quarter
    """
    try:
        from sklearn.linear_model import LinearRegression
        
        price_df = get_price_data(2018, 2024)
        if price_df.empty or len(price_df) < 4:
            return _default_price_forecast()
        
        price_df['date'] = pd.to_datetime(price_df['date'])
        price_df['quarter'] = price_df['date'].dt.quarter
        price_df['year'] = price_df['date'].dt.year
        
        # 获取产量数据
        prod_df = get_production_data(2018, 2024)
        national_prod = prod_df[prod_df['province'].isna() | (prod_df['province'] == '全国')]
        
        if national_prod.empty or len(national_prod) < 3:
            return _default_price_forecast()
        
        # 简化特征：季度、产量
        # 合并
        merged = price_df.merge(national_prod[['year', 'output_tons']], on='year', how='left')
        merged = merged.dropna()
        
        if len(merged) < 4:
            return _default_price_forecast()
        
        # 构造特征矩阵
        X = merged[['quarter', 'output_tons']].values
        y = merged['price_yuan_per_jin'].values
        
        # 标准化
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X_scaled, y)
        
        # 预测下季度
        last_row = merged.iloc[-1]
        next_quarter = (last_row['quarter'] % 4) + 1
        next_year = last_row['year'] if next_quarter != 1 else last_row['year'] + 1
        next_prod = national_prod[national_prod['year'] == next_year]
        next_prod_val = next_prod['output_tons'].values[0] if not next_prod.empty else last_row['output_tons']
        
        X_next = scaler.transform([[next_quarter, next_prod_val]])
        prediction = model.predict(X_next)[0]
        volatility = merged['price_yuan_per_jin'].std()
        
        return {
            'value': round(float(prediction), 1),
            'volatility': round(float(volatility), 1),
            'next_quarter': int(next_quarter)
        }
    except Exception as e:
        print(f"价格预测失败，使用默认预测: {e}")
        return _default_price_forecast()

def _default_price_forecast():
    """默认价格预测"""
    price_df = get_price_data(2020, 2024)
    if price_df.empty:
        return {'value': 55.0, 'volatility': 5.0, 'next_quarter': 1}
    
    current_price = price_df['price_yuan_per_jin'].iloc[-1]
    volatility = price_df['price_yuan_per_jin'].std()
    
    # 简单用当前价格作为预测
    return {
        'value': round(float(current_price), 1),
        'volatility': round(float(volatility), 1) if volatility > 0 else 5.0,
        'next_quarter': 1
    }

def get_forecast_summary():
    """获取预测摘要"""
    output_forecast = predict_output(2)
    price_forecast = predict_price()
    
    return {
        'next_year_output': output_forecast['predicted'].iloc[0] if not output_forecast.empty else None,
        'output_ci': (output_forecast['ci_lower'].iloc[0], output_forecast['ci_upper'].iloc[0]) if not output_forecast.empty else None,
        'next_quarter_price': price_forecast['value'],
        'price_volatility': price_forecast['volatility']
    }

if __name__ == "__main__":
    print("=== 产量预测 ===")
    print(predict_output(2))
    print("\n=== 价格预测 ===")
    print(predict_price())
