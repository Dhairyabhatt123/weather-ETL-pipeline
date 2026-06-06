import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
API_KEY = "216cdd8d10f0aae8f9d448893794f5e3"

CITIES = [
    "London", "New York", "Tokyo", "Paris", "Dubai",
    "Mumbai", "Sydney", "Toronto", "Berlin", "Singapore"
]

st.set_page_config(
    page_title="Global Weather Intelligence",
    page_icon="🌍",
    layout="wide"
)

# ── Extract & Transform ───────────────────────────────────────────────────────
@st.cache_data(ttl=600)  # refresh every 10 minutes
def fetch_weather():
    records = []
    for city in CITIES:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        if res.status_code == 200:
            d = res.json()
            records.append({
                "city":          d["name"],
                "country":       d["sys"]["country"],
                "latitude":      d["coord"]["lat"],
                "longitude":     d["coord"]["lon"],
                "temp_celsius":  round(d["main"]["temp"], 2),
                "feels_like":    round(d["main"]["feels_like"], 2),
                "temp_min":      round(d["main"]["temp_min"], 2),
                "temp_max":      round(d["main"]["temp_max"], 2),
                "humidity":      d["main"]["humidity"],
                "pressure":      d["main"]["pressure"],
                "wind_speed":    d["wind"]["speed"],
                "weather_main":  d["weather"][0]["main"],
                "weather_desc":  d["weather"][0]["description"].title(),
                "cloudiness":    d["clouds"]["all"],
                "visibility":    d.get("visibility", 0),
                "recorded_at":   datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
            })
    return pd.DataFrame(records)

# ── Load Data ─────────────────────────────────────────────────────────────────
df = fetch_weather()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🌍 Global Weather Intelligence Dashboard")
st.markdown("**Real-Time ETL Pipeline: OpenWeatherMap API → Python → MySQL → Streamlit**")
st.markdown(f"*Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*")
st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🌡️ Avg Temperature", f"{df['temp_celsius'].mean():.1f}°C")
k2.metric("💧 Avg Humidity",     f"{df['humidity'].mean():.1f}%")
k3.metric("💨 Avg Wind Speed",   f"{df['wind_speed'].mean():.1f} m/s")
k4.metric("🌤️ Most Common",      df['weather_main'].mode()[0])
k5.metric("🏙️ Cities Monitored", len(df))

st.markdown("---")

# ── Row 1: Bar Chart + Pie Chart ──────────────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    fig_bar = px.bar(
        df.sort_values("temp_celsius", ascending=True),
        x="temp_celsius", y="city",
        orientation="h",
        color="temp_celsius",
        color_continuous_scale="RdYlBu_r",
        text="temp_celsius",
        title="🌡️ Temperature by City (°C)",
        labels={"temp_celsius": "Temperature (°C)", "city": "City"}
    )
    fig_bar.update_traces(texttemplate="%{text:.1f}°C", textposition="outside")
    fig_bar.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_pie = px.pie(
        df, names="weather_main",
        title="🌤️ Weather Conditions Distribution",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4
    )
    fig_pie.update_traces(textinfo="label+percent")
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Row 2: World Map ──────────────────────────────────────────────────────────
fig_map = px.scatter_geo(
    df,
    lat="latitude", lon="longitude",
    size="temp_celsius",
    color="weather_main",
    hover_name="city",
    hover_data={"temp_celsius": True, "humidity": True,
                "weather_desc": True, "wind_speed": True},
    title="🗺️ Global Temperature Map",
    projection="natural earth",
    color_discrete_sequence=px.colors.qualitative.Set1
)
fig_map.update_layout(height=450)
st.plotly_chart(fig_map, use_container_width=True)

# ── Row 3: Humidity + Wind Speed ──────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    fig_hum = px.bar(
        df.sort_values("humidity", ascending=False),
        x="city", y="humidity",
        color="humidity",
        color_continuous_scale="Blues",
        title="💧 Humidity by City (%)",
        text="humidity"
    )
    fig_hum.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_hum.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig_hum, use_container_width=True)

with col4:
    fig_wind = px.bar(
        df.sort_values("wind_speed", ascending=False),
        x="city", y="wind_speed",
        color="wind_speed",
        color_continuous_scale="Greens",
        title="💨 Wind Speed by City (m/s)",
        text="wind_speed"
    )
    fig_wind.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig_wind.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig_wind, use_container_width=True)

# ── Row 4: Raw Data Table ─────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📋 Live Weather Data Table")
st.dataframe(
    df[[
        "city", "country", "temp_celsius", "feels_like",
        "humidity", "wind_speed", "weather_main", "weather_desc",
        "cloudiness", "recorded_at"
    ]].sort_values("temp_celsius", ascending=False),
    use_container_width=True,
    hide_index=True
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("Built with **Python · Pandas · MySQL · Streamlit · Plotly** | Data: OpenWeatherMap API")