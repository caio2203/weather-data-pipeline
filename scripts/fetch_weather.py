# scripts/fetch_weather.py
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import os

def fetch_weather():
    # Setup do cliente
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=3, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Parâmetros de localização e variáveis
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -14.8661,
        "longitude": -40.8394,
        "daily": [
            "temperature_2m_max", "temperature_2m_min", "apparent_temperature_min",
            "apparent_temperature_max", "sunset", "daylight_duration",
            "sunshine_duration", "sunrise", "uv_index_max"
        ],
        "hourly": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "precipitation_probability", "rain"
        ],
        "current": [
            "temperature_2m", "apparent_temperature", "relative_humidity_2m",
            "is_day", "rain"
        ],
        "timezone": "America/Sao_Paulo"
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Current
    current = response.Current()
    current_data = {
        "temperature_2m": current.Variables(0).Value(),
        "apparent_temperature": current.Variables(1).Value(),
        "relative_humidity_2m": current.Variables(2).Value(),
        "is_day": current.Variables(3).Value(),
        "rain": current.Variables(4).Value(),
        "timestamp": pd.to_datetime(current.Time(), unit="s")
    }

    # Hourly
    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
        "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
        "apparent_temperature": hourly.Variables(2).ValuesAsNumpy(),
        "precipitation_probability": hourly.Variables(3).ValuesAsNumpy(),
        "rain": hourly.Variables(4).ValuesAsNumpy()
    }
    hourly_df = pd.DataFrame(hourly_data)

    # Daily
    daily = response.Daily()
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s"),
            end=pd.to_datetime(daily.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ),
        "temperature_2m_max": daily.Variables(0).ValuesAsNumpy(),
        "temperature_2m_min": daily.Variables(1).ValuesAsNumpy(),
        "apparent_temperature_min": daily.Variables(2).ValuesAsNumpy(),
        "apparent_temperature_max": daily.Variables(3).ValuesAsNumpy(),
        "sunset": daily.Variables(4).ValuesInt64AsNumpy(),
        "daylight_duration": daily.Variables(5).ValuesAsNumpy(),
        "sunshine_duration": daily.Variables(6).ValuesAsNumpy(),
        "sunrise": daily.Variables(7).ValuesInt64AsNumpy(),
        "uv_index_max": daily.Variables(8).ValuesAsNumpy(),
    }
    daily_df = pd.DataFrame(daily_data)

    return current_data, hourly_df, daily_df

# Teste local
if __name__ == "__main__":
    c, h, d = fetch_weather()
    print("CURRENT:")
    print(c)
    print("HOURLY:")
    print(h.head())
    print("DAILY:")
    print(d.head())

def save_to_csv(current_data, hourly_df, daily_df):
    os.makedirs("data", exist_ok=True)

    # Current: salva como CSV de uma linha
    pd.DataFrame([current_data]).to_csv("data/weather_current.csv", index=False)

    # Hourly
    hourly_df.to_csv("data/weather_hourly.csv", index=False)

    # Daily
    daily_df.to_csv("data/weather_daily.csv", index=False)

    print("✔️ Arquivos CSV salvos em /data")

# Teste local
if __name__ == "__main__":
    c, h, d = fetch_weather()
    save_to_csv(c, h, d)