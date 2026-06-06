import requests

API_KEY = "216cdd8d10f0aae8f9d448893794f5e3"  # paste your OpenWeatherMap API key here

CITIES = [
    "London", "New York", "Tokyo", "Paris", "Dubai",
    "Mumbai", "Sydney", "Toronto", "Berlin", "Singapore"
]

def extract_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f" Failed to fetch data for {city}: {response.status_code}")
        return None

def extract_all_cities():
    raw_data = []
    for city in CITIES:
        data = extract_weather(city)
        if data:
            raw_data.append(data)
            print(f" Extracted: {city}")
    print(f"\n Total cities extracted: {len(raw_data)}")
    return raw_data

if __name__ == "__main__":
    data = extract_all_cities()
    print(data[0])  # preview first city raw data