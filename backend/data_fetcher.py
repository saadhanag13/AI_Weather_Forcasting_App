import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd

# Setup session
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=3, backoff_factor=0.3)
client = openmeteo_requests.Client(session=retry_session)

# Define feature variables used during training
FEATURES = [
    "temperature_2m",
    "relative_humidity_2m",
    "dew_point_2m",
    "apparent_temperature",
    "precipitation",
    "windspeed_10m",
    "surface_pressure"
]

CITY_COORDS = {
    "London": (51.5085, -0.1257, "Europe/London"),
    "New York": (40.7128, -74.0060, "America/New_York"),
    "Tokyo": (35.6895, 139.6917, "Asia/Tokyo"),
    "Sydney": (-33.8688, 151.2093, "Australia/Sydney"),
    "Delhi": (28.6139, 77.2090, "Asia/Kolkata"),
    "Paris": (48.8566, 2.3522, "Europe/Paris"),
    "Berlin": (52.5200, 13.4050, "Europe/Berlin"),
    "Moscow": (55.7558, 37.6173, "Europe/Moscow"),
    "Beijing": (39.9042, 116.4074, "Asia/Shanghai"),
    "Seoul": (37.5665, 126.9780, "Asia/Seoul"),
    "Singapore": (1.3521, 103.8198, "Asia/Singapore"),
    "Dubai": (25.276987, 55.296249, "Asia/Dubai"),
    "Los Angeles": (34.0522, -118.2437, "America/Los_Angeles"),
    "San Francisco": (37.7749, -122.4194, "America/Los_Angeles"),
    "Toronto": (43.651070, -79.347015, "America/Toronto"),
    "São Paulo": (-23.5505, -46.6333, "America/Sao_Paulo"),
    "Johannesburg": (-26.2041, 28.0473, "Africa/Johannesburg"),
    "Istanbul": (41.0082, 28.9784, "Europe/Istanbul"),
    "Bangkok": (13.7563, 100.5018, "Asia/Bangkok"),
    "Mexico City": (19.4326, -99.1332, "America/Mexico_City")
}


def fetch_city_data(city):
    if city not in CITY_COORDS:
        raise ValueError(f"{city} not found.")
    
    lat, lon, timezone = CITY_COORDS[city]
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join(FEATURES),
        "timezone": timezone
    }
    responses = client.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    response = responses[0]
    hourly = response.Hourly()

    df = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
    }
    for i, var in enumerate(FEATURES):
        df[var] = hourly.Variables(i).ValuesAsNumpy()
    df = pd.DataFrame(df)
    return df.dropna().reset_index(drop=True)
