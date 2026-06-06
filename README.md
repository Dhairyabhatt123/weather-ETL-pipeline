# 🌍 Global Weather Intelligence Dashboard
## Real-Time ETL Pipeline: API → Python → MySQL → Power BI

![Dashboard Preview](dashboard_preview.png)

## 🏗️ Pipeline Architecture
API (OpenWeatherMap) → extract.py → transform.py → load.py → MySQL → Power BI

## 📦 Tech Stack
- **Data Ingestion:** OpenWeatherMap REST API
- **ETL:** Python, Pandas
- **Database:** MySQL
- **Visualization:** Microsoft Power BI
- **Orchestration:** pipeline.py

## 📊 Dashboard Features
- Live temperature comparison across 10 global cities
- Interactive world map with weather conditions
- KPI cards (Avg Temp, Humidity, Wind Speed)
- Weather condition distribution (Pie Chart)
- Interactive slicer for filtering by weather type

## 🚀 How to Run
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your OpenWeatherMap API key in `extract.py`
4. Run: `python pipeline.py`
5. Open Power BI and connect to MySQL `weather_pipeline` database

## 📈 Results
- 10 cities monitored in real-time
- Pipeline runs in under 5 seconds
- Data stored in structured MySQL schema
