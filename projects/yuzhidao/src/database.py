"""数据库操作模块"""
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "sea_cucumber.db"

def get_conn():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """初始化数据库表"""
    conn = get_conn()
    cursor = conn.cursor()

    # 产量数据表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS production (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            province TEXT,
            output_tons REAL,
            area_hectare REAL,
            seedlings_billion INTEGER,
            yield_per_mu REAL,
            source TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(year, province)
        )
    """)

    # 价格数据表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            region TEXT,
            product_type TEXT,
            price_yuan_per_jin REAL,
            source TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 进出口数据表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            month INTEGER,
            direction TEXT,
            quantity_tons REAL,
            amount_usd REAL,
            partner_country TEXT,
            source TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 原始文件记录表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            year INTEGER,
            file_path TEXT NOT NULL,
            file_type TEXT,
            url TEXT,
            hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print(f"数据库初始化完成: {DB_PATH}")

def import_production_data(df: pd.DataFrame):
    """批量导入产量数据"""
    conn = get_conn()
    for _, row in df.iterrows():
        conn.execute("""
            INSERT OR REPLACE INTO production
            (year, province, output_tons, area_hectare, seedlings_billion, yield_per_mu, source, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['year'], row.get('province'), row.get('output_tons'),
            row.get('area_hectare'), row.get('seedlings_billion'),
            row.get('yield_per_mu'), row.get('source'), row.get('url')
        ))
    conn.commit()
    conn.close()

def get_production_data(start_year=2013, end_year=2024):
    """获取指定年份范围的产量数据"""
    conn = get_conn()
    df = pd.read_sql("""
        SELECT * FROM production
        WHERE year BETWEEN ? AND ?
        ORDER BY year, province
    """, conn, params=(start_year, end_year))
    conn.close()
    return df

def import_price_data(df: pd.DataFrame):
    """批量导入价格数据"""
    conn = get_conn()
    for _, row in df.iterrows():
        conn.execute("""
            INSERT INTO price
            (date, region, product_type, price_yuan_per_jin, source, url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row['date'], row.get('region'), row.get('product_type'),
            row.get('price_yuan_per_jin'), row.get('source'), row.get('url')
        ))
    conn.commit()
    conn.close()

def get_price_data(start_year=2020, end_year=2024):
    """获取价格数据"""
    conn = get_conn()
    df = pd.read_sql("""
        SELECT * FROM price
        WHERE strftime('%Y', date) BETWEEN ? AND ?
        ORDER BY date, region
    """, conn, params=(str(start_year), str(end_year)))
    conn.close()
    return df

def get_trade_data(start_year=2013, end_year=2024):
    """获取贸易数据"""
    conn = get_conn()
    df = pd.read_sql("""
        SELECT * FROM trade
        WHERE year BETWEEN ? AND ?
        ORDER BY year, month, direction
    """, conn, params=(start_year, end_year))
    conn.close()
    return df

def init_weather_db():
    """初始化天气数据表"""
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_date DATE NOT NULL,
            event_type TEXT NOT NULL,
            region TEXT,
            severity TEXT,
            description TEXT,
            source TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            station TEXT,
            sea_surface_temp REAL,
            summer_water_temp_anomaly REAL,
            typhoon_count INTEGER,
            red_tide_area REAL,
            data_points INTEGER,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(year, station)
        )
    """)
    
    conn.commit()
    conn.close()
    print("天气数据表初始化完成")

def save_weather_data(records: list):
    """批量保存天气数据"""
    conn = get_conn()
    for r in records:
        conn.execute("""
            INSERT OR REPLACE INTO weather_data
            (year, station, sea_surface_temp, summer_water_temp_anomaly, data_points)
            VALUES (?, ?, ?, ?, ?)
        """, (
            r.get('year'), r.get('station'),
            r.get('annual_mean_temp'), r.get('summer_water_temp_anomaly'),
            r.get('data_points')
        ))
    conn.commit()
    conn.close()

def get_weather_data(start_year=2013, end_year=2024):
    """获取天气数据"""
    conn = get_conn()
    df = pd.read_sql("""
        SELECT * FROM weather_data
        WHERE year BETWEEN ? AND ?
        ORDER BY year, station
    """, conn, params=(start_year, end_year))
    conn.close()
    return df

def save_weather_event(event: dict):
    """保存天气事件"""
    conn = get_conn()
    conn.execute("""
        INSERT INTO weather_events
        (event_date, event_type, region, severity, description, source, url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        event.get('event_date'), event.get('event_type'),
        event.get('region'), event.get('severity'),
        event.get('description'), event.get('source'), event.get('url')
    ))
    conn.commit()
    conn.close()

def get_weather_events_from_db(start_year, end_year):
    """获取天气事件"""
    conn = get_conn()
    df = pd.read_sql("""
        SELECT * FROM weather_events
        WHERE event_date BETWEEN ? AND ?
        ORDER BY event_date
    """, conn, params=(f"{start_year}-01-01", f"{end_year}-12-31"))
    conn.close()
    return df

if __name__ == "__main__":
    init_db()
    init_weather_db()
