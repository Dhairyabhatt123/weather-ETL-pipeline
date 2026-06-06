from extract import extract_all_cities
from transform import transform_weather
from load import load_to_mysql
from datetime import datetime

def run_pipeline():
    print("=" * 50)
    print(f" Pipeline Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # Step 1 — Extract
    print("\n STEP 1: Extracting data from OpenWeatherMap API...")
    raw_data = extract_all_cities()

    # Step 2 — Transform
    print("\n STEP 2: Transforming & validating data...")
    df = transform_weather(raw_data)

    # Step 3 — Load
    print("\n STEP 3: Loading data to MySQL...")
    load_to_mysql(df)

    print("\n" + "=" * 50)
    print(f" Pipeline Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" {len(df)} cities loaded successfully")
    print("=" * 50)

if __name__ == "__main__":
    run_pipeline()