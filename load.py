from sqlalchemy import create_engine, text
import pandas as pd

DB_USER = "root"
DB_PASSWORD = "root123"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "weather_pipeline"

def get_engine():
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(url)
    return engine

def load_to_mysql(df):
    engine = get_engine()

    # Write to MySQL table
    df.to_sql(
        name="weather_data",
        con=engine,
        if_exists="append",  # append new data each run
        index=False
    )
    print(f" Loaded {len(df)} records to MySQL table 'weather_data'")

    # Verify by reading back
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM weather_data"))
        count = result.fetchone()[0]
        print(f" Total records in database: {count}")

if __name__ == "__main__":
    from extract import extract_all_cities
    from transform import transform_weather
    raw = extract_all_cities()
    df = transform_weather(raw)
    load_to_mysql(df)