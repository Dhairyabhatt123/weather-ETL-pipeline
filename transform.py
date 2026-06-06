import pandas as pd
from datetime import datetime

def transform_weather(raw_data):
    records = []

    for data in raw_data:
        record = {
            # Location
            "city":             data["name"],
            "country":          data["sys"]["country"],
            "latitude":         data["coord"]["lat"],
            "longitude":        data["coord"]["lon"],

            # Temperature
            "temp_celsius":     data["main"]["temp"],
            "feels_like":       data["main"]["feels_like"],
            "temp_min":         data["main"]["temp_min"],
            "temp_max":         data["main"]["temp_max"],

            # Conditions
            "humidity":         data["main"]["humidity"],
            "pressure":         data["main"]["pressure"],
            "weather_main":     data["weather"][0]["main"],
            "weather_desc":     data["weather"][0]["description"],
            "wind_speed":       data["wind"]["speed"],
            "cloudiness":       data["clouds"]["all"],
            "visibility":       data.get("visibility", 0),

            # Timestamp
            "recorded_at":      datetime.utcfromtimestamp(data["dt"]),
            "extracted_at":     datetime.utcnow()
        }
        records.append(record)

    df = pd.DataFrame(records)

    # Data quality checks
    df = df.dropna(subset=["city", "temp_celsius"])
    df = df[df["temp_celsius"].between(-60, 60)]
    df = df[df["humidity"].between(0, 100)]

    print(f" Transformed {len(df)} records")
    print(df[["city", "country", "temp_celsius", "humidity", "weather_main"]].to_string(index=False))
    return df

if __name__ == "__main__":
    from extract import extract_all_cities
    raw = extract_all_cities()
    df = transform_weather(raw)