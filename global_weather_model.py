import tensorflow as tf
import numpy as np
import pandas as pd
import sklearn 
import seaborn 
import keras_tuner as kt
import openmeteo_requests
import requests_cache
from retry_requests import retry
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential
from keras_tuner import HyperModel
from keras_tuner.tuners import RandomSearch
from tensorflow.keras.optimizers import Adam
import joblib
import os


# Setup retry + cache for API calls
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# List of global cities (lat, lon, timezone)
cities = {
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

variables = [
    "temperature_2m",
    "relative_humidity_2m",
    "dew_point_2m",
    "apparent_temperature",
    "precipitation",
    "windspeed_10m",
    "surface_pressure"
]

def fetch_weather_data(lat, lon, timezone):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join(variables),
        "timezone": timezone
    }
    responses = openmeteo.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    response = responses[0]
    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
    }
    for i, var in enumerate(variables):
        hourly_data[var] = hourly.Variables(i).ValuesAsNumpy()

    df = pd.DataFrame(hourly_data)
    df = df.dropna()
    return df

# ✅ Initialize hourly_df_dict to avoid NameError
hourly_df_dict = {}

# Combine all cities' data into one dataset
all_data = pd.DataFrame()
for city, (lat, lon, tz) in cities.items():
    print(f"Fetching: {city}")
    df = fetch_weather_data(lat, lon, tz)
    df["city"] = city
    hourly_df_dict[city] = df.copy()  # ✅ Save each city's DataFrame for testing later
    all_data = pd.concat([all_data, df], ignore_index=True)
    
# Normalize features
features = variables
scaler = MinMaxScaler()
scaled = scaler.fit_transform(all_data[features])
joblib.dump(scaler, "scaler_global.pkl")  # Save for backend

# Prepare sequence data for LSTM (e.g., 6 time steps)
def create_sequences(data, time_steps=6):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:i+time_steps])
        y.append(data[i+time_steps][0])  # Temperature prediction
    return np.array(X), np.array(y)

X, y = create_sequences(scaled, time_steps=6)
X = X.reshape((X.shape[0], X.shape[1], X.shape[2]))
y = y.reshape(-1, 1)

# Build LSTM model
model = Sequential()
model.add(LSTM(64, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(32))
model.add(Dense(1))

model.compile(optimizer="adam", loss="mse", metrics=["mae"])
model.fit(X, y, epochs=25, batch_size=32, verbose=1)

# Save the model
model.save("global_weather_saved_model.keras", save_format="keras")
print("✅ Model trained and saved as `global_weather_saved_model.keras`")

# Model Tuner- Keras Tuner
# Split into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True
)

print("Training shape:", X_train.shape, y_train.shape)
print("Validation shape:", X_val.shape, y_val.shape)

class WeatherBiLSTMHyperModel(HyperModel):
    def __init__(self, input_shape):
        self.input_shape = input_shape

    def build(self, hp):
        model = Sequential()
        model.add(
            LSTM(
                units=hp.Int('lstm_units_1', 32, 128, step=16),
                return_sequences=True,
                input_shape=self.input_shape
            )
        )
        model.add(Dropout(hp.Float('dropout_1', 0.1, 0.5, step=0.1)))

        model.add(
            LSTM(
                units=hp.Int('lstm_units_2', 16, 64, step=16)
            )
        )
        model.add(Dropout(hp.Float('dropout_2', 0.1, 0.5, step=0.1)))
        model.add(Dense(1))

        model.compile(
            optimizer=Adam(
                hp.Choice('learning_rate', [1e-2, 1e-3, 1e-4])
            ),
            loss='mse',
            metrics=['mae']
        )
        return model

input_shape = (X.shape[1], X.shape[2])  # e.g., (6, 7)
hypermodel = WeatherBiLSTMHyperModel(input_shape)

tuner = RandomSearch(
    hypermodel,
    objective='val_mae',
    max_trials=10,
    executions_per_trial=1,
    directory='tuning_logs',
    project_name='weather_bilstm'
)

tuner.search(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=20,
    batch_size=32,
    verbose=1
)

best_model = tuner.get_best_models(num_models=1)[0]
best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]

print("✅ Best Hyperparameters Found:")
print(f"LSTM 1 units: {best_hps.get('lstm_units_1')}")
print(f"LSTM 2 units: {best_hps.get('lstm_units_2')}")
print(f"Dropout 1: {best_hps.get('dropout_1')}")
print(f"Dropout 2: {best_hps.get('dropout_2')}")
print(f"Learning rate: {best_hps.get('learning_rate')}")

# Save the best model
best_model.save("tuned_saved_model.keras", save_format="keras")
print("✅ Tuned model saved as `tuned_saved_model.keras`")