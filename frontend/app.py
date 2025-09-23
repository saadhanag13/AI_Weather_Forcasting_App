# #frontend/app.py
# import streamlit as st
# import requests
# import numpy as np
# import pandas as pd
# import time
# from datetime import datetime
# import plotly.graph_objects as go
# import plotly.express as px
# from concurrent.futures import ThreadPoolExecutor
# import warnings
# warnings.simplefilter(action="ignore", category=FutureWarning)
# import os
# from dotenv import load_dotenv

# load_dotenv()
# # BACKEND_URL = "http://127.0.0.1:8000"

# BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

# # Add this after the BACKEND_URL definition:
# if "previous_backend_url" not in st.session_state:
#     st.session_state.previous_backend_url = BACKEND_URL
# elif st.session_state.previous_backend_url != BACKEND_URL:
#     st.cache_data.clear()  # Clear cache when URL changes
#     st.session_state.previous_backend_url = BACKEND_URL
    
# print(f"🔗 Backend URL: {BACKEND_URL}")
# print("🚀 Starting Smart Weather Decision Dashboard...")

# # 🌍 Enhanced City Configuration with Decision Context
# CITY_DATA = {
#     "London": {
#         "weather": "rainy", "country": "UK", "timezone": "GMT",
#         "coords": "51.5074°N, 0.1278°W", "icon": "🌫️", "description": "Foggy and charming"
#     },
#     "New York": {
#         "weather": "urban", "country": "USA", "timezone": "EST",
#         "coords": "40.7128°N, 74.0060°W", "icon": "🏙️", "description": "The city that never sleeps"
#     },
#     "Tokyo": {
#         "weather": "urban", "country": "Japan", "timezone": "JST",
#         "coords": "35.6762°N, 139.6503°E", "icon": "🌸", "description": "Modern metropolis"
#     },
#     "Sydney": {
#         "weather": "sunny", "country": "Australia", "timezone": "AEST",
#         "coords": "33.8688°S, 151.2093°E", "icon": "🏖️", "description": "Harbour city"
#     },
#     "Delhi": {
#         "weather": "hot", "country": "India", "timezone": "IST",
#         "coords": "28.7041°N, 77.1025°E", "icon": "🏛️", "description": "Historic capital"
#     },
#     "Paris": {
#         "weather": "temperate", "country": "France", "timezone": "CET",
#         "coords": "48.8566°N, 2.3522°E", "icon": "🗼", "description": "City of lights"
#     },
#     "Berlin": {
#         "weather": "temperate", "country": "Germany", "timezone": "CET",
#         "coords": "52.5200°N, 13.4050°E", "icon": "🏰", "description": "Historic heart"
#     },
#     "Moscow": {
#         "weather": "cold", "country": "Russia", "timezone": "MSK",
#         "coords": "55.7558°N, 37.6173°E", "icon": "❄️", "description": "Winter wonderland"
#     },
#     "Beijing": {
#         "weather": "continental", "country": "China", "timezone": "CST",
#         "coords": "39.9042°N, 116.4074°E", "icon": "🏮", "description": "Ancient capital"
#     },
#     "Seoul": {
#         "weather": "continental", "country": "South Korea", "timezone": "KST",
#         "coords": "37.5665°N, 126.9780°E", "icon": "🌺", "description": "Tech hub"
#     },
#     "Singapore": {
#         "weather": "tropical", "country": "Singapore", "timezone": "SGT",
#         "coords": "1.3521°N, 103.8198°E", "icon": "🌴", "description": "Garden city"
#     },
#     "Dubai": {
#         "weather": "desert", "country": "UAE", "timezone": "GST",
#         "coords": "25.2048°N, 55.2708°E", "icon": "🏜️", "description": "Desert oasis"
#     },
#     "Los Angeles": {
#         "weather": "sunny", "country": "USA", "timezone": "PST",
#         "coords": "34.0522°N, 118.2437°W", "icon": "🌴", "description": "City of angels"
#     },
#     "San Francisco": {
#         "weather": "foggy", "country": "USA", "timezone": "PST",
#         "coords": "37.7749°N, 122.4194°W", "icon": "🌉", "description": "Golden Gate city"
#     },
#     "Toronto": {
#         "weather": "continental", "country": "Canada", "timezone": "EST",
#         "coords": "43.651070°N, 79.347015°W", "icon": "🍁", "description": "Multicultural hub"
#     },
#     "São Paulo": {
#         "weather": "tropical", "country": "Brazil", "timezone": "BRT",
#         "coords": "23.5505°S, 46.6333°W", "icon": "🌆", "description": "Tropical megacity"
#     },
#     "Johannesburg": {
#         "weather": "temperate", "country": "South Africa", "timezone": "SAST",
#         "coords": "26.2041°S, 28.0473°E", "icon": "💎", "description": "City of gold"
#     },
#     "Istanbul": {
#         "weather": "mediterranean", "country": "Turkey", "timezone": "TRT",
#         "coords": "41.0082°N, 28.9784°E", "icon": "🕌", "description": "Bridge of continents"
#     },
#     "Bangkok": {
#         "weather": "tropical", "country": "Thailand", "timezone": "ICT",
#         "coords": "13.7563°N, 100.5018°E", "icon": "🛕", "description": "Temple city"
#     },
#     "Mexico City": {
#         "weather": "temperate", "country": "Mexico", "timezone": "CST",
#         "coords": "19.4326°N, 99.1332°W", "icon": "🌮", "description": "Aztec heritage"
#     }
# }

# # 📊 User Persona Configurations
# USER_PERSONAS = {
#     "Commuter": {
#         "icon": "🚗", 
#         "priorities": ["temperature", "precipitation", "wind", "visibility"],
#         "key_times": ["7-9", "17-19"],
#         "decisions": ["Route planning", "Transport mode", "Departure time"]
#     },
#     "Event Planner": {
#         "icon": "🎪", 
#         "priorities": ["temperature", "precipitation", "humidity", "uv_index"],
#         "key_times": ["10-22"],
#         "decisions": ["Venue choice", "Equipment needs", "Backup plans"]
#     },
#     "Outdoor Activity": {
#         "icon": "👷", 
#         "priorities": ["temperature", "heat_index", "uv_index", "precipitation"],
#         "key_times": ["6-18"],
#         "decisions": ["Safety measures", "Work schedules", "Equipment needs"]
#     },
#     "Tourist": {
#         "icon": "📸", 
#         "priorities": ["temperature", "precipitation", "visibility", "comfort"],
#         "key_times": ["9-17"],
#         "decisions": ["Activity planning", "Clothing choice", "Itinerary changes"]
#     }
# }

# # 🚨 Smart Alert Configuration
# ALERT_THRESHOLDS = {
#     "extreme_heat": {"temp": 35, "color": "#FF4444", "icon": "🔥", "priority": "HIGH"},
#     "extreme_cold": {"temp": -10, "color": "#4444FF", "icon": "❄️", "priority": "HIGH"},
#     "high_humidity": {"humidity": 80, "color": "#FF8800", "icon": "💧", "priority": "MEDIUM"},
#     "strong_wind": {"wind": 25, "color": "#8844FF", "icon": "💨", "priority": "MEDIUM"},
#     "poor_air": {"aqi": 150, "color": "#AA4444", "icon": "😷", "priority": "HIGH"}
# }

# # 🎨 Streamlit Configuration
# st.set_page_config(
#     page_title="Smart Weather Decisions",
#     page_icon="🎯",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize Enhanced Session State
# if 'weather_data' not in st.session_state:
#     st.session_state.weather_data = {}
# if 'selected_city' not in st.session_state:
#     st.session_state.selected_city = "London"
# if 'user_persona' not in st.session_state:
#     st.session_state.user_persona = "Commuter"
# if 'hourly_data' not in st.session_state:
#     st.session_state.hourly_data = {}
# if 'last_fetch_time' not in st.session_state:
#     st.session_state.last_fetch_time = None

# # 🤖 Enhanced Weather Data Generation with Hourly Forecasts
# def generate_hourly_forecast(city, base_temp):
#     """Generate realistic hourly weather data"""
#     current_hour = datetime.now().hour
#     hourly_data = []
    
#     for i in range(24):
#         hour = (current_hour + i) % 24
#         # Simulate daily temperature curve
#         temp_variation = 5 * np.sin((hour - 14) * np.pi / 12)
#         temp = base_temp + temp_variation + np.random.normal(0, 2)
        
#         # Generate conditions based on temperature and time
#         if temp > 30:
#             condition = np.random.choice(["sunny", "hot"], p=[0.7, 0.3])
#             icon = "☀️" if condition == "sunny" else "🔥"
#         elif temp < 5:
#             condition = np.random.choice(["cold", "snow"], p=[0.6, 0.4])
#             icon = "❄️" if condition == "cold" else "🌨️"
#         elif 6 <= hour <= 18:
#             condition = np.random.choice(["sunny", "cloudy", "rainy"], p=[0.5, 0.3, 0.2])
#             icon = {"sunny": "☀️", "cloudy": "☁️", "rainy": "🌧️"}[condition]
#         else:
#             condition = np.random.choice(["clear", "cloudy"], p=[0.6, 0.4])
#             icon = "🌙" if condition == "clear" else "☁️"
        
#         # Generate alerts and recommendations
#         alerts = []
#         if temp > 35:
#             alerts.append({"type": "extreme_heat", "message": "Extreme heat warning"})
#         elif temp < -5:
#             alerts.append({"type": "extreme_cold", "message": "Extreme cold warning"})
        
#         humidity = max(30, min(90, 60 + np.random.normal(0, 15)))
#         if humidity > 80:
#             alerts.append({"type": "high_humidity", "message": "High humidity levels"})
        
#         hourly_data.append({
#             "hour": f"{hour:02d}:00",
#             "temperature": round(temp, 1),
#             "condition": condition,
#             "icon": icon,
#             "humidity": round(humidity),
#             "wind_speed": max(0, round(10 + np.random.normal(0, 5), 1)),
#             "uv_index": max(0, round((10 * np.sin((hour - 12) * np.pi / 12)) if 6 <= hour <= 18 else 0)),
#             "alerts": alerts,
#             "comfort_index": round(max(0, min(10, 10 - abs(temp - 22) / 3)), 1)
#         })
    
#     return hourly_data

# @st.cache_data(ttl=300)
# def fetch_enhanced_weather(city):
#     """Fetch enhanced weather data with hourly forecasts"""
#     try:
#         # Your FastAPI backend call
#         API_URL = f"{BACKEND_URL}/predict"
#         payload = {"city": city}
        
#         print(f"Calling API {API_URL} with city {city}")
#         response = requests.post(API_URL, json=payload, timeout=10)
        
#         print(f"📡 API Response Status: {response.status_code}")
        
#         if response.status_code == 200:
#             result = response.json()
#             base_temp = result.get("predicted_temperature", 20)
#             print(f"Got real prediction: {base_temp}°C  for {city}")
        
#         # # Generate comprehensive weather data
#             current_temp = base_temp + np.random.normal(0, 1)
#             hourly_forecast = generate_hourly_forecast(city, base_temp)
        
#         # # Calculate key metrics
#             today_temps = [h["temperature"] for h in hourly_forecast[:12]]
#             tomorrow_temps = [h["temperature"] for h in hourly_forecast[12:]]
        
#             return {
#                 "city": city,
#                 "current_temperature": round(current_temp, 1),
#                 "predicted_temperature": base_temp,  # Add the real prediction
#                 "api_source": "real",  # Flag to show data source
#                 "confidence": result.get("confidence", 85),
#                 "feels_like": round(current_temp + np.random.normal(0, 2), 1),
#                 "today_high": round(max(today_temps), 1),
#                 "today_low": round(min(today_temps), 1),
#                 "tomorrow_high": round(max(tomorrow_temps), 1),
#                 "tomorrow_low": round(min(tomorrow_temps), 1),
#                 "humidity": round(60 + np.random.normal(0, 20)),
#                 "wind_speed": round(max(0, 15 + np.random.normal(0, 8)), 1),
#                 "uv_index": np.random.randint(0, 11),
#                 "air_quality": np.random.randint(50, 200),
#                 "hourly_forecast": hourly_forecast,
#                 "confidence": np.random.randint(85, 98),
#                 "status": "success",
#                 "timestamp": datetime.now(),
#                 "trend": "rising" if np.random.random() > 0.5 else "falling"
#             }
#         else:
#             error_msg = f"API returned {response.status_code}: {response.text}"
#             print(f"❌ API Error: {error_msg}")
#             st.error(f"Weather API Error: {error_msg}")
#             return None
        
#     except requests.exceptions.Timeout:
#         st.error("⏰ API timeout - backend is taking too long to respond")
#         return None
#     except requests.exceptions.ConnectionError:
#         st.error("🔌 Cannot connect to weather API - check if backend is running")
#         return None
#     except Exception as e:
#         st.error(f"❌ Weather fetch failed: {str(e)}")
#         print(f"❌ Exception: {e}")
#         return None
    


# # 📱 Smart Sidebar - User-Focused Controls
# with st.sidebar:
#     st.markdown("# 🎯 Weather Command Center")
    
#     # Location Selection
#     if 'selected_city' not in st.session_state:
#         st.session_state['selected_city'] = list(CITY_DATA.keys())[0]
#     st.markdown("### 📍 Your Location")
#     cities_list = list(CITY_DATA.keys())
#     city_options = [f"{CITY_DATA[city]['icon']} {city}" for city in cities_list]
    
#     default_city = st.session_state.get("selected_city", cities_list[0])
#     try:
#         default_index = cities_list.index(default_city)
#     except ValueError:
#         default_index = 0
    
#     selected_display = st.selectbox("Where are you?", city_options, index=default_index, key="city_select")
    
#     # Extract city name from selection
#     new_selected_city = selected_display.split(" ", 1)[1]
    
#     # Check if city has changed
#     city_changed = st.session_state.selected_city != new_selected_city
    
#     # Update the selected city
#     st.session_state.selected_city = new_selected_city
    
#     # If city changed or no weather data exists, fetch new data
#     if city_changed or st.session_state.selected_city not in st.session_state.weather_data:
#         with st.spinner("Getting latest data..."):
#             weather_data = fetch_enhanced_weather(st.session_state.selected_city)
#             if weather_data:
#                 st.session_state.weather_data[st.session_state.selected_city] = weather_data
#                 st.session_state.last_fetch_time = datetime.now()
#                 # Clear insights when city changes so they get regenerated
#                 st.session_state["insights"] = None
    
#     # st.markdown("---")
    
#     # User Persona Selection
#     persona_options = [f"{USER_PERSONAS[p]['icon']} {p}" for p in USER_PERSONAS.keys()]
#     selected_persona = st.selectbox("Select your role:", persona_options, key="persona_select")
#     st.session_state.user_persona = selected_persona.split(" ", 1)[1]
    
#     current_persona = USER_PERSONAS[st.session_state.user_persona]
#     st.info(f"**Key decisions:** {', '.join(current_persona['decisions'])}")
    
#     # Generate insights after weather data is fetched
#     def get_city_insights(city):
#         """Generate insights based on current weather data"""
#         weather_data = st.session_state.weather_data.get(city)
#         if not weather_data:
#             return f"Weather data for {city} is loading..."
        
#         current_temp = weather_data.get('current_temperature', 20)
#         humidity = weather_data.get('humidity', 50)
#         air_quality = weather_data.get('air_quality', 50)
        
#         insights = []
        
#         # Temperature insights
#         if current_temp > 30:
#             insights.append(f"🔥 Very hot in {city} - stay hydrated")
#         elif current_temp < 5:
#             insights.append(f"❄️ Very cold in {city} - dress warmly")
#         else:
#             insights.append(f"🌡️ Comfortable temperature in {city}")
        
#         # Humidity insights
#         if humidity > 75:
#             insights.append("💧 High humidity - may feel muggy")
#         elif humidity < 30:
#             insights.append("🏜️ Low humidity - stay moisturized")
        
#         # Air quality insights
#         if air_quality > 150:
#             insights.append("😷 Poor air quality - limit outdoor activity")
#         elif air_quality < 50:
#             insights.append("🌿 Excellent air quality")
        
#         return " • ".join(insights[:3])  # Return top 3 insights
    
#     # Generate or retrieve insights
#     if st.session_state.get("insights") is None or city_changed:
#         st.session_state["insights"] = get_city_insights(st.session_state.selected_city)
    
#     # Display insights
#     if st.session_state.get("insights"):
#         st.info(f"💡 **Quick insights:** {st.session_state['insights']}")
    
#     # Quick Actions
#     if st.button("🔄 Refresh", type="primary"):        
#         with st.spinner("Getting latest data..."):
#             weather_data = fetch_enhanced_weather(st.session_state.selected_city)
#             if weather_data:
#                 st.session_state.weather_data[st.session_state.selected_city] = weather_data
#                 st.session_state.last_fetch_time = datetime.now()
#                 # Regenerate insights with new data
#                 st.session_state["insights"] = get_city_insights(st.session_state.selected_city)
#                 st.experimental_rerun()
#                 st.success("Updated!")
                

    
# # 🎨 Dynamic Styling

# city_info = CITY_DATA[st.session_state.selected_city]
# city_name = st.session_state.selected_city

# st.markdown(f"""
# <style>
# .stApp {{
#     background-attachment: fixed;
# }}

# /* Enhanced readability */
# .main-content {{
#     background: rgba(255, 255, 255, 0.05);
#     border-radius: 20px;
#     padding: 2rem;
#     backdrop-filter: blur(10px);
#     margin: 1rem 0;
# }}

# .decision-card {{
#     background: rgba(255, 255, 255, 0.95);
#     padding: 1.5rem;
#     border-radius: 15px;
#     box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
#     border-left: 5px solid #00AA00;
#     margin: 1rem 0;
#     transition: all 0.3s ease;
# }}

# .decision-card:hover {{
#     transform: translateY(-3px);
#     box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
# }}

# .alert-card {{
#     background: rgba(255, 0, 0, 0.1);
#     border: 2px solid #FF4444;
#     border-radius: 10px;
#     padding: 1rem;
#     margin: 0.5rem 0;
# }}

# .hourly-card {{
#     background: rgba(255, 255, 255, 0.9);
#     border-radius: 10px;
#     padding: 1rem;
#     text-align: center;
#     margin: 0.5rem;
#     min-width: 120px;
#     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
# }}

# .metric-big {{
#     font-size: 3rem;
#     font-weight: bold;
#     text-align: center;
#     margin: 1rem 0;
# }}

# .metric-label {{
#     font-size: 1.2rem;
#     color: #666;
#     text-align: center;
# }}

# /* Text visibility */
# .stApp, .stApp * {{
#     color: #FFFFFF !important;
# }}

# .decision-card *, .hourly-card * {{
#     color: #000000 !important;
# }}

# .stButton button {{
#     color: #ffffff !important;
# }}

# #MainMenu {{visibility: hidden;}}
# footer {{visibility: hidden;}}
# .stDeployButton {{display:none;}}
# </style>
# """, unsafe_allow_html=True)

# # 🌟 Conditional Dashboard Header
# weather_data = st.session_state.weather_data.get(st.session_state.selected_city)

# if weather_data:
#     # Show personalized header when data is available
#     st.markdown(f"""
#     <div class="main-content">
#         <h1 style="text-align: center; font-size: 2.5rem; margin-bottom: 0;">
#             Weather Insights for {st.session_state.user_persona} in {city_name} {city_info['icon']}
#         </h1>
#     </div>
#     """, unsafe_allow_html=True)
# else:
#     # Show generic header for new users
#     st.markdown(f"""
#         <div class="main-content">
#             <h1 style="text-align: center; font-size: 2.5rem; margin-bottom: 0;">
#                 Smart Weather Forecast Dashboard
#             </h1>
#         </div>
#     """, unsafe_allow_html=True)

# if weather_data:
    
#     current_time = datetime.now()

    
#     # 🚨 Priority Alerts Section (Most Important)
#     alerts = []
#     current_temp = weather_data.get("current_temperature", 20)
    
#     if current_temp > 35:
#         alerts.append({"type": "extreme_heat", "message": f"🔥 HEAT WARNING: {current_temp}°C - Take cooling measures", "priority": "HIGH"})
#     elif current_temp < 0:
#         alerts.append({"type": "extreme_cold", "message": f"❄️ FREEZE WARNING: {current_temp}°C - Risk of hypothermia", "priority": "HIGH"})
    
#     if weather_data.get("air_quality", 50) > 150:
#         alerts.append({"type": "poor_air", "message": f"😷 AIR QUALITY ALERT: AQI {weather_data.get('air_quality', 0)} - Limit outdoor activity", "priority": "HIGH"})
    
#     if weather_data.get("uv_index", 0) > 8:
#         alerts.append({"type": "high_uv", "message": f"☀️ UV WARNING: Index {weather_data.get('uv_index', 0)} - Sun protection essential", "priority": "MEDIUM"})
    
#     # Display Priority Alerts
#     if alerts:
#         st.markdown("## 🚨 IMMEDIATE ATTENTION NEEDED")
#         for alert in alerts:
#             color = "#FF4444" if alert["priority"] == "HIGH" else "#FF8800"
#             st.markdown(f"""
#             <div class="alert-card" style="border-color: {color};">
#                 <h3 style="color: {color} !important;">{alert['message']}</h3>
#             </div>
#             """, unsafe_allow_html=True)
    
#     # 🎯 Key Decision Metrics (Only 3-5 that matter)
#     st.markdown("## 🎯 Your Key Numbers Right Now")
    
#     col1, col2, col3, col4, col5 = st.columns(5)
    
#     with col1:
#         trend_icon = "📈" if weather_data.get("trend", "rising") == "rising" else "📉"
#         st.metric(
#             label="🌡️ Current Temp",
#             value=f"{weather_data.get('current_temperature', 0)}°C",
#             delta=f"Feels {weather_data.get('feels_like', 0)}°C",
#             help="What it feels like right now"
#         )
    
#     with col2:
#         today_high= weather_data.get('today_high', 0)
#         today_low= weather_data.get('today_low', 0)
#         today_range = today_high - today_low
#         st.metric(
#             label="📅 Today's Range",
#             value=f"{today_low}° to {today_high}°",
#             delta=f"{today_range}° swing",
#             help="Temperature variation today"
#         )
    
#     with col3:
#         tomorrow_high= weather_data.get('tomorrow_high', 0)
#         today_high= weather_data.get('today_high', 0)
#         tomorrow_change = tomorrow_high - today_high
#         st.metric(
#             label="🌅 Tomorrow's High",
#             value=f"{tomorrow_high}°C",
#             delta=f"{tomorrow_change:+.1f}° vs today",
#             help="How tomorrow compares to today"
#         )
    
#     with col4:
#         current_temp= weather_data.get('current_temperature', 22)
#         comfort_score = max(0, min(10, 10 - abs(current_temp - 22) / 3))
#         confidence = weather_data.get('confidence', 0)
#         st.metric(
#             label="😊 Comfort Score",
#             value=f"{comfort_score:.1f}/10",
#             delta=f"{confidence}% confident",
#             help="How comfortable you'll feel outside"
#         )
    
#     with col5:
#         # Air quality color coding
#         aqi = weather_data.get('air_quality', 50)
#         aqi_color = "#00AA00" if aqi < 100 else "#FFAA00" if aqi < 150 else "#FF4444"
#         aqi_status = "Good" if aqi < 100 else "Satisfactory" if aqi < 150 else "Poor"
#         st.metric(
#             label="🌬️ Air Quality",
#             value=f"{aqi} ({aqi_status})",
#             delta=f"{aqi_status}",
#             help="Air pollution levels"
#         )
    
#     # 📊 Persona-Specific Decision Support
#     st.markdown(f"## 💡 Smart Recommendations for {st.session_state.user_persona}s")
    
#     persona = USER_PERSONAS[st.session_state.user_persona]
#     recommendations = []
    
#     # Generate persona-specific recommendations
#     if st.session_state.user_persona == "Commuter":
#         current_temp = weather_data.get('current_temperature', 20)
#         wind_speed = weather_data.get('wind_speed', 0)
#         air_quality = weather_data.get('air_quality', 50)
        
#         if current_temp < 5:
#             recommendations.append("🚗 Consider driving instead of walking - very cold conditions")
#         if wind_speed > 20:
#             recommendations.append("🌪️ Allow extra travel time - strong winds may cause delays")
#         if air_quality > 100:
#             recommendations.append("😷 Consider indoor routes or wear a mask during commute")
        
#     elif st.session_state.user_persona == "Event Planner":
#         humidity = weather_data.get('humidity', 50)
#         tomorrow_high = weather_data.get('tomorrow_high', 20)
#         uv_index = weather_data.get('uv_index', 3)
        
#         if humidity > 75:
#             recommendations.append("💧 High humidity - ensure adequate ventilation and cooling")
#         if tomorrow_high > 30:
#             recommendations.append("☀️ Hot tomorrow - arrange shade, water stations, and cooling areas")
#         if uv_index > 6:
#             recommendations.append("🕶️ Provide sunscreen and recommend protective clothing")
        
#     elif st.session_state.user_persona == "Outdoor Activity":
#         current_temp = weather_data.get('current_temperature', 20)
#         uv_index = weather_data.get('uv_index', 3)
#         wind_speed = weather_data.get('wind_speed', 0)
        
#         if current_temp > 32:
#             recommendations.append("🔥 Heat safety protocol - frequent breaks and hydration required")
#         if uv_index > 7:
#             recommendations.append("☀️ High UV exposure - protective clothing and sunscreen mandatory")
#         if wind_speed > 25:
#             recommendations.append("💨 Strong winds - secure equipment and avoid high work")
    
#     elif st.session_state.user_persona == "Tourist":
#         current_temp = weather_data.get('current_temperature', 20)
#         humidity = weather_data.get('humidity', 50)
#         tomorrow_high = weather_data.get('tomorrow_high', 20)
#         today_high = weather_data.get('today_high', 20)
        
#         if current_temp > 25:
#             recommendations.append("👕 Perfect weather for outdoor sightseeing")
#         if humidity < 50:
#             recommendations.append("📸 Low humidity - great conditions for photography")
#         if tomorrow_high < today_high - 5:
#             recommendations.append("🧥 Pack layers - tomorrow will be significantly cooler")
    
#     # Display recommendations
#     if recommendations:
#         for i, rec in enumerate(recommendations[:3]):  # Limit to 3 most important
#             st.markdown(f"""
#             <div class="decision-card">
#                 <h4 style="color: #000000 !important; margin-bottom: 0.5rem;">{rec}</h4>
#             </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.markdown(f"""
#         <div class="decision-card">
#             <h4 style="color: #000000 !important;">✅ Weather conditions are optimal for your activities today!</h4>
#         </div>
#         """, unsafe_allow_html=True)
    
#     # ⏰ Hourly Forecast (Google Weather Style)
#     st.markdown("## ⏰ Next 12 Hours - Plan Your Day")
    
#     # Create horizontal scrollable hourly forecast
#     hourly_data = weather_data.get("hourly_forecast", [])[:12]  # Next 12 hours
    
#     # Create columns for horizontal layout
#     cols = st.columns(min(6, len(hourly_data)))  # Max 6 columns for mobile compatibility
#     hourly_data= weather_data.get("hourly_forecast", [])[:12]
#     if hourly_data and len(hourly_data) > 6:
        
#         cols = st.columns(min(6, len(hourly_data)))
    
#         for i, hour_data in enumerate(hourly_data[:6]):  # Show first 6 hours
#             with cols[i]:
#                 temp = hour_data["temperature"]
#                 temp_color = "#FF4444" if temp > 30 else "#4444FF" if temp < 5 else "#00AA00"
                
#                 st.markdown(f"""
#                 <div class="hourly-card">
#                     <div style="font-size: 0.9rem; color: #666 !important;">{hour_data['hour']}</div>
#                     <div style="font-size: 2rem; margin: 0.5rem 0;">{hour_data['icon']}</div>
#                     <div style="font-size: 1.3rem; font-weight: bold; color: {temp_color} !important;">{temp}°</div>
#                     <div style="font-size: 0.8rem; color: #888 !important;">UV {hour_data['uv_index']}</div>
#                     {f'<div style="font-size: 0.7rem; color: #FF4444 !important;">⚠️ Alert</div>' if hour_data['alerts'] else ''}
#                 </div>
#                 """, unsafe_allow_html=True)
#     else:
#         st.info("Hourly forecast data is not available. Click '🔄 Refresh' to fetch the latest data.")
    
#     # 📈 Smart Trend Analysis
#     if len(hourly_data) >= 12:
#         st.markdown("## 📈 Temperature Trend Analysis")
        
#         # Create trend chart
#         times = [h.get("hour", f"{i}:00") for i, h in enumerate(hourly_data[:12])]
#         temps = [h.get("temperature", 20) for h in hourly_data[:12]]
        
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(
#             x=times,
#             y=temps,
#             mode='lines+markers',
#             name='Temperature',
#             line=dict(width=3, color='#00AA00'),
#             marker=dict(size=8)
#         ))
        
#         # Add comfort zone
#         fig.add_hline(y=22, line_dash="dash", line_color="green", annotation_text="Comfort Zone", annotation_position="bottom right")
        
#         fig.update_layout(
#         title="Next 12 Hours Temperature Trend",
#         title_font=dict(size=18, color="white"),  # Make title bigger & white
#         xaxis=dict(
#             title=dict(
#                 text="Time (Next 12 Hours)",
#                 font=dict(size=16, color="white")
#             ),
#             tickfont=dict(size=12, color="white"),  # x-axis labels white
#             showgrid=True,
#             gridcolor="gray"
#         ),
#         yaxis=dict(
#             title=dict(
#                 text="Temperature (°C)",
#                 font=dict(size=16, color="white")
#             ),
#             tickfont=dict(size=12, color="white"),  # y-axis labels white
#             showgrid=True,
#             gridcolor="gray"
#         ),
#         legend=dict(
#             font=dict(size=12, color="white"),  # legend text white
#             bgcolor="rgba(0,0,0,0)"  # transparent background
#         ),
#         plot_bgcolor="rgba(0,0,0,0)",  
#         paper_bgcolor="rgba(0,0,0,0)" 
#     )

        
#         st.plotly_chart(fig, use_container_width=True)
        
#         # Smart insights from the trend
#         temp_change = temps[-1] - temps[0]
#         if abs(temp_change) > 5:
#             direction = "rising" if temp_change > 0 else "falling"
#             st.info(f"🌡️ **Temperature Alert**: {abs(temp_change):.1f}°C {direction} over next 12 hours. Plan accordingly!")

# else:
#     # First-time user experience
#     st.markdown("""
#     <div class="main-content">
#         <h2>👋 Welcome to Smart Weather Decisions!</h2>
#         <p>Get weather insights that actually help you make better decisions.</p>
#         <p>🎯 <strong>What makes this different?</strong></p>
#         <ul>
#             <li>✅ Shows only the 3-5 numbers that matter for YOUR role</li>
#             <li>🚨 Immediate alerts for conditions that need your attention</li>
#             <li>💡 Specific recommendations based on what you need to decide</li>
#             <li>📱 Mobile-friendly design that works everywhere</li>
#             <li>⏰ Hourly forecasts to plan your entire day</li>
#         </ul>
#         <p><strong>Click "🔄 Refresh" to get started!</strong></p>
#     </div>
#     """, unsafe_allow_html=True)

# # 📱 Mobile-optimized footer with last update
# if st.session_state.last_fetch_time and weather_data is not None: 
#     st.markdown(f"""
#     <div style="text-align: center; padding: 1rem; opacity: 0.7;">
#         Last updated: {st.session_state.last_fetch_time.strftime('%H:%M:%S')} | 
#         Data accuracy: {weather_data.get('confidence', 'N/A')}%
#     </div>
#     """, unsafe_allow_html=True)






# frontend/app.py- New script 
import streamlit as st
import requests
import numpy as np
import pandas as pd
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from concurrent.futures import ThreadPoolExecutor
import warnings
import pytz
warnings.simplefilter(action="ignore", category=FutureWarning)
import os
from dotenv import load_dotenv

# Import timezone utilities
from timezone_utils import TimezoneManager, get_user_timezone, format_timestamp, get_current_user_time

load_dotenv()
# BACKEND_URL = "http://127.0.0.1:8000"

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

# Add this after the BACKEND_URL definition:
if "previous_backend_url" not in st.session_state:
    st.session_state.previous_backend_url = BACKEND_URL
elif st.session_state.previous_backend_url != BACKEND_URL:
    st.cache_data.clear()  # Clear cache when URL changes
    st.session_state.previous_backend_url = BACKEND_URL
    
print(f"🔗 Backend URL: {BACKEND_URL}")
print("🚀 Starting Smart Weather Decision Dashboard...")

# 🌍 Enhanced City Configuration with Decision Context and Timezone Integration
CITY_DATA = {
    "London": {
        "weather": "rainy", "country": "UK", "timezone": "GMT",
        "timezone_proper": "Europe/London",
        "coords": "51.5074°N, 0.1278°W", 
        "coords_decimal": (51.5074, -0.1278),
        "icon": "🌫️", "description": "Foggy and charming"
    },
    "New York": {
        "weather": "urban", "country": "USA", "timezone": "EST",
        "timezone_proper": "America/New_York",
        "coords": "40.7128°N, 74.0060°W", 
        "coords_decimal": (40.7128, -74.0060),
        "icon": "🏙️", "description": "The city that never sleeps"
    },
    "Tokyo": {
        "weather": "urban", "country": "Japan", "timezone": "JST",
        "timezone_proper": "Asia/Tokyo",
        "coords": "35.6762°N, 139.6503°E", 
        "coords_decimal": (35.6762, 139.6503),
        "icon": "🌸", "description": "Modern metropolis"
    },
    "Sydney": {
        "weather": "sunny", "country": "Australia", "timezone": "AEST",
        "timezone_proper": "Australia/Sydney",
        "coords": "33.8688°S, 151.2093°E", 
        "coords_decimal": (-33.8688, 151.2093),
        "icon": "🏖️", "description": "Harbour city"
    },
    "Delhi": {
        "weather": "hot", "country": "India", "timezone": "IST",
        "timezone_proper": "Asia/Kolkata",
        "coords": "28.7041°N, 77.1025°E", 
        "coords_decimal": (28.7041, 77.1025),
        "icon": "🏛️", "description": "Historic capital"
    },
    "Paris": {
        "weather": "temperate", "country": "France", "timezone": "CET",
        "timezone_proper": "Europe/Paris",
        "coords": "48.8566°N, 2.3522°E", 
        "coords_decimal": (48.8566, 2.3522),
        "icon": "🗼", "description": "City of lights"
    },
    "Berlin": {
        "weather": "temperate", "country": "Germany", "timezone": "CET",
        "timezone_proper": "Europe/Berlin",
        "coords": "52.5200°N, 13.4050°E", 
        "coords_decimal": (52.5200, 13.4050),
        "icon": "🏰", "description": "Historic heart"
    },
    "Moscow": {
        "weather": "cold", "country": "Russia", "timezone": "MSK",
        "timezone_proper": "Europe/Moscow",
        "coords": "55.7558°N, 37.6173°E", 
        "coords_decimal": (55.7558, 37.6173),
        "icon": "❄️", "description": "Winter wonderland"
    },
    "Beijing": {
        "weather": "continental", "country": "China", "timezone": "CST",
        "timezone_proper": "Asia/Shanghai",
        "coords": "39.9042°N, 116.4074°E", 
        "coords_decimal": (39.9042, 116.4074),
        "icon": "🏮", "description": "Ancient capital"
    },
    "Seoul": {
        "weather": "continental", "country": "South Korea", "timezone": "KST",
        "timezone_proper": "Asia/Seoul",
        "coords": "37.5665°N, 126.9780°E", 
        "coords_decimal": (37.5665, 126.9780),
        "icon": "🌺", "description": "Tech hub"
    },
    "Singapore": {
        "weather": "tropical", "country": "Singapore", "timezone": "SGT",
        "timezone_proper": "Asia/Singapore",
        "coords": "1.3521°N, 103.8198°E", 
        "coords_decimal": (1.3521, 103.8198),
        "icon": "🌴", "description": "Garden city"
    },
    "Dubai": {
        "weather": "desert", "country": "UAE", "timezone": "GST",
        "timezone_proper": "Asia/Dubai",
        "coords": "25.2048°N, 55.2708°E", 
        "coords_decimal": (25.2048, 55.2708),
        "icon": "🏜️", "description": "Desert oasis"
    },
    "Los Angeles": {
        "weather": "sunny", "country": "USA", "timezone": "PST",
        "timezone_proper": "America/Los_Angeles",
        "coords": "34.0522°N, 118.2437°W", 
        "coords_decimal": (34.0522, -118.2437),
        "icon": "🌴", "description": "City of angels"
    },
    "San Francisco": {
        "weather": "foggy", "country": "USA", "timezone": "PST",
        "timezone_proper": "America/Los_Angeles",
        "coords": "37.7749°N, 122.4194°W", 
        "coords_decimal": (37.7749, -122.4194),
        "icon": "🌉", "description": "Golden Gate city"
    },
    "Toronto": {
        "weather": "continental", "country": "Canada", "timezone": "EST",
        "timezone_proper": "America/Toronto",
        "coords": "43.651070°N, 79.347015°W", 
        "coords_decimal": (43.6511, -79.3470),
        "icon": "🍁", "description": "Multicultural hub"
    },
    "São Paulo": {
        "weather": "tropical", "country": "Brazil", "timezone": "BRT",
        "timezone_proper": "America/Sao_Paulo",
        "coords": "23.5505°S, 46.6333°W", 
        "coords_decimal": (-23.5505, -46.6333),
        "icon": "🌆", "description": "Tropical megacity"
    },
    "Johannesburg": {
        "weather": "temperate", "country": "South Africa", "timezone": "SAST",
        "timezone_proper": "Africa/Johannesburg",
        "coords": "26.2041°S, 28.0473°E", 
        "coords_decimal": (-26.2041, 28.0473),
        "icon": "💎", "description": "City of gold"
    },
    "Istanbul": {
        "weather": "mediterranean", "country": "Turkey", "timezone": "TRT",
        "timezone_proper": "Europe/Istanbul",
        "coords": "41.0082°N, 28.9784°E", 
        "coords_decimal": (41.0082, 28.9784),
        "icon": "🕌", "description": "Bridge of continents"
    },
    "Bangkok": {
        "weather": "tropical", "country": "Thailand", "timezone": "ICT",
        "timezone_proper": "Asia/Bangkok",
        "coords": "13.7563°N, 100.5018°E", 
        "coords_decimal": (13.7563, 100.5018),
        "icon": "🛕", "description": "Temple city"
    },
    "Mexico City": {
        "weather": "temperate", "country": "Mexico", "timezone": "CST",
        "timezone_proper": "America/Mexico_City",
        "coords": "19.4326°N, 99.1332°W", 
        "coords_decimal": (19.4326, -99.1332),
        "icon": "🌮", "description": "Aztec heritage"
    }
}

# 📊 User Persona Configurations
USER_PERSONAS = {
    "Commuter": {
        "icon": "🚗", 
        "priorities": ["temperature", "precipitation", "wind", "visibility"],
        "key_times": ["7-9", "17-19"],
        "decisions": ["Route planning", "Transport mode", "Departure time"]
    },
    "Event Planner": {
        "icon": "🎪", 
        "priorities": ["temperature", "precipitation", "humidity", "uv_index"],
        "key_times": ["10-22"],
        "decisions": ["Venue choice", "Equipment needs", "Backup plans"]
    },
    "Outdoor Activity": {
        "icon": "👷", 
        "priorities": ["temperature", "heat_index", "uv_index", "precipitation"],
        "key_times": ["6-18"],
        "decisions": ["Safety measures", "Work schedules", "Equipment needs"]
    },
    "Tourist": {
        "icon": "📸", 
        "priorities": ["temperature", "precipitation", "visibility", "comfort"],
        "key_times": ["9-17"],
        "decisions": ["Activity planning", "Clothing choice", "Itinerary changes"]
    }
}

# 🚨 Smart Alert Configuration
ALERT_THRESHOLDS = {
    "extreme_heat": {"temp": 35, "color": "#FF4444", "icon": "🔥", "priority": "HIGH"},
    "extreme_cold": {"temp": -10, "color": "#4444FF", "icon": "❄️", "priority": "HIGH"},
    "high_humidity": {"humidity": 80, "color": "#FF8800", "icon": "💧", "priority": "MEDIUM"},
    "strong_wind": {"wind": 25, "color": "#8844FF", "icon": "💨", "priority": "MEDIUM"},
    "poor_air": {"aqi": 150, "color": "#AA4444", "icon": "😷", "priority": "HIGH"}
}

# 🎨 Streamlit Configuration
st.set_page_config(
    page_title="Smart Weather Decisions",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Enhanced Session State with Timezone Support
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = {}
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = "London"
if 'user_persona' not in st.session_state:
    st.session_state.user_persona = "Commuter"
if 'hourly_data' not in st.session_state:
    st.session_state.hourly_data = {}
if 'last_fetch_time' not in st.session_state:
    st.session_state.last_fetch_time = None
if 'user_timezone' not in st.session_state:
    st.session_state.user_timezone = "UTC"

# 🤖 Enhanced Weather Data Generation with Hourly Forecasts and Timezone Awareness
def generate_hourly_forecast(city, base_temp, user_timezone):
    """Generate realistic hourly weather data with timezone awareness"""
    # Get current hour in user's timezone
    current_user_time = TimezoneManager.get_current_time_in_timezone(user_timezone)
    current_hour = current_user_time.hour
    
    hourly_data = []
    
    for i in range(24):
        hour = (current_hour + i) % 24
        # Create datetime for this hour in user's timezone
        hour_datetime = current_user_time.replace(hour=hour, minute=0, second=0, microsecond=0)
        if i > 0:
            hour_datetime = hour_datetime.replace(day=current_user_time.day + (current_hour + i) // 24)
        
        # Simulate daily temperature curve
        temp_variation = 5 * np.sin((hour - 14) * np.pi / 12)
        temp = base_temp + temp_variation + np.random.normal(0, 2)
        
        # Generate conditions based on temperature and time
        if temp > 30:
            condition = np.random.choice(["sunny", "hot"], p=[0.7, 0.3])
            icon = "☀️" if condition == "sunny" else "🔥"
        elif temp < 5:
            condition = np.random.choice(["cold", "snow"], p=[0.6, 0.4])
            icon = "❄️" if condition == "cold" else "🌨️"
        elif 6 <= hour <= 18:
            condition = np.random.choice(["sunny", "cloudy", "rainy"], p=[0.5, 0.3, 0.2])
            icon = {"sunny": "☀️", "cloudy": "☁️", "rainy": "🌧️"}[condition]
        else:
            condition = np.random.choice(["clear", "cloudy"], p=[0.6, 0.4])
            icon = "🌙" if condition == "clear" else "☁️"
        
        # Generate alerts and recommendations
        alerts = []
        if temp > 35:
            alerts.append({"type": "extreme_heat", "message": "Extreme heat warning"})
        elif temp < -5:
            alerts.append({"type": "extreme_cold", "message": "Extreme cold warning"})
        
        humidity = max(30, min(90, 60 + np.random.normal(0, 15)))
        if humidity > 80:
            alerts.append({"type": "high_humidity", "message": "High humidity levels"})
        
        hourly_data.append({
            "hour": hour_datetime.strftime('%H:%M'),
            "hour_display": format_timestamp(hour_datetime, st.session_state.user_timezone)[0],
            "datetime": hour_datetime,
            "temperature": round(temp, 1),
            "condition": condition,
            "icon": icon,
            "humidity": round(humidity),
            "wind_speed": max(0, round(10 + np.random.normal(0, 5), 1)),
            "uv_index": max(0, round((10 * np.sin((hour - 12) * np.pi / 12)) if 6 <= hour <= 18 else 0)),
            "alerts": alerts,
            "comfort_index": round(max(0, min(10, 10 - abs(temp - 22) / 3)), 1)
        })
    
    return hourly_data

@st.cache_data(ttl=300)
def fetch_enhanced_weather(city, user_timezone="UTC"):
    try:
        # Your FastAPI backend call
        API_URL = f"{BACKEND_URL}/predict"
        payload = {"city": city}
        
        print(f"Calling API {API_URL} with city {city}")
        response = requests.post(API_URL, json=payload, timeout=10)
        
        print(f"📡 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            base_temp = result.get("predicted_temperature", 20)
            print(f"Got real prediction: {base_temp}°C for {city}")
            
            # Get timestamp from backend (assume it's UTC)
            backend_timestamp = result.get("timestamp_utc")
            if backend_timestamp:
                if isinstance(backend_timestamp, str):
                    utc_time = datetime.fromisoformat(backend_timestamp.replace('Z', '+00:00'))
                else:
                    utc_time = backend_timestamp
            else:
                utc_time = datetime.now(pytz.UTC)
            
            # Convert to user timezone for display
            time_str, tz_abbr, local_time = format_timestamp(utc_time, user_timezone)
            
            # Generate comprehensive weather data
            current_temp = base_temp + np.random.normal(0, 1)
            city_timezone = get_city_timezone(city)
            hourly_forecast = generate_hourly_forecast(city, base_temp, user_timezone)
            
            for h in hourly_forecast:
                h["time_display"] = format_timestamp(h["datetime"], user_timezone)[0]
            
            # Calculate key metrics
            today_temps = [h["temperature"] for h in hourly_forecast[:12]]
            tomorrow_temps = [h["temperature"] for h in hourly_forecast[12:]]
            
            return {
                "city": city,
                "current_temperature": round(current_temp, 1),
                "predicted_temperature": base_temp,
                "api_source": "real",
                "confidence": result.get("confidence", 85),
                "feels_like": round(current_temp + np.random.normal(0, 2), 1),
                "today_high": round(max(today_temps), 1),
                "today_low": round(min(today_temps), 1),
                "tomorrow_high": round(max(tomorrow_temps), 1),
                "tomorrow_low": round(min(tomorrow_temps), 1),
                "humidity": round(60 + np.random.normal(0, 20)),
                "wind_speed": round(max(0, 15 + np.random.normal(0, 8)), 1),
                "uv_index": np.random.randint(0, 11),
                "air_quality": np.random.randint(50, 200),
                "hourly_forecast": hourly_forecast,
                "status": "success",
                "timestamp_utc": utc_time,
                "timestamp_local": local_time,
                "timestamp_display": f"{time_str} {tz_abbr}",
                "user_timezone": user_timezone,
                "trend": "rising" if np.random.random() > 0.5 else "falling"
            }
        else:
            error_msg = f"API returned {response.status_code}: {response.text}"
            print(f"❌ API Error: {error_msg}")
            st.error(f"Weather API Error: {error_msg}")
            return None
        
    except requests.exceptions.Timeout:
        st.error("⏰ API timeout - backend is taking too long to respond")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to weather API - check if backend is running")
        return None
    except Exception as e:
        st.error(f"❌ Weather fetch failed: {str(e)}")
        print(f"❌ Exception: {e}")
        return None

# Helper function to get city timezone
def get_city_timezone(city_name):
    """Get proper IANA timezone for a city"""
    city_info = CITY_DATA.get(city_name, {})
    return city_info.get("timezone_proper", "UTC")

# 📱 Smart Sidebar - User-Focused Controls with Timezone Management
with st.sidebar:
    st.markdown("# 🎯 Weather Command Center")
    
    # Timezone Selection (Top Priority)
    # st.markdown("### 🌍 Your Timezone")
    user_timezone = get_user_timezone()
    st.session_state.user_timezone = user_timezone
    
    # Display current time in user's timezone
    current_user_time = TimezoneManager.render_timezone_info(user_timezone)
    
    st.markdown("---")
    
    # Location Selection
    st.markdown("### 📍 Your Location")
    cities_list = list(CITY_DATA.keys())
    city_options = [f"{CITY_DATA[city]['icon']} {city}" for city in cities_list]
    
    default_city = st.session_state.get("selected_city", cities_list[0])
    try:
        default_index = cities_list.index(default_city)
    except ValueError:
        default_index = 0
    
    selected_display = st.selectbox("Where are you?", city_options, index=default_index, key="city_select")
    
    # Extract city name from selection
    new_selected_city = selected_display.split(" ", 1)[1]
    
    # Check if city has changed
    city_changed = st.session_state.selected_city != new_selected_city
    timezone_changed = st.session_state.get('previous_user_timezone') != user_timezone
    
    # Store previous timezone for comparison
    st.session_state.previous_user_timezone = user_timezone
    
    # Update the selected city
    st.session_state.selected_city = new_selected_city
    
    # Show city timezone info
    city_timezone = get_city_timezone(new_selected_city)
    city_current_time = TimezoneManager.get_current_time_in_timezone(city_timezone)
    city_info = CITY_DATA[new_selected_city]
    st.write(f"**Local Timezone:** {city_info['timezone']} ({city_timezone})")
    st.write(f"**Coordinates:** {city_info['coords']}")
    
    # with st.expander("🌍 City Information", expanded=False):
    #     st.write(f"**Country:** {city_info['country']}")
    #     st.write(f"**Local Timezone:** {city_info['timezone']} ({city_timezone})")
    #     st.write(f"**Current time there:** {city_current_time.strftime('%H:%M:%S %Z')}")
    #     st.write(f"**Description:** {city_info['description']}")
    #     st.write(f"**Coordinates:** {city_info['coords']}")
    
    # If city or timezone changed, fetch new data
    if city_changed or timezone_changed or st.session_state.selected_city not in st.session_state.weather_data:
        with st.spinner("Getting latest data..."):
            weather_data = fetch_enhanced_weather(st.session_state.selected_city, user_timezone)
            if weather_data:
                st.session_state.weather_data[st.session_state.selected_city] = weather_data
                st.session_state.last_fetch_time = weather_data['timestamp_local']
                # Clear insights when city changes so they get regenerated
                st.session_state["insights"] = None
    
    # st.markdown("---")
    
    # User Persona Selection
    # st.markdown("### 👤 Your Role")
    persona_options = [f"{USER_PERSONAS[p]['icon']} {p}" for p in USER_PERSONAS.keys()]
    selected_persona = st.selectbox("Select your role:", persona_options, key="persona_select")
    st.session_state.user_persona = selected_persona.split(" ", 1)[1]
    
    current_persona = USER_PERSONAS[st.session_state.user_persona]
    st.info(f"**Key decisions:** {', '.join(current_persona['decisions'])}")
    
    # Generate insights after weather data is fetched
    def get_city_insights(city):
        """Generate insights based on current weather data"""
        weather_data = st.session_state.weather_data.get(city)
        if not weather_data:
            return f"Weather data for {city} is loading..."
        
        current_temp = weather_data.get('current_temperature', 20)
        humidity = weather_data.get('humidity', 50)
        air_quality = weather_data.get('air_quality', 50)
        
        insights = []
        
        # Temperature insights
        if current_temp > 30:
            insights.append(f"🔥 Very hot in {city} - stay hydrated")
        elif current_temp < 5:
            insights.append(f"❄️ Very cold in {city} - dress warmly")
        else:
            insights.append(f"🌡️ Comfortable temperature in {city}")
        
        # Humidity insights
        if humidity > 75:
            insights.append("💧 High humidity - may feel muggy")
        elif humidity < 30:
            insights.append("🏜️ Low humidity - stay moisturized")
        
        # Air quality insights
        if air_quality > 150:
            insights.append("😷 Poor air quality - limit outdoor activity")
        elif air_quality < 50:
            insights.append("🌿 Excellent air quality")
        
        return " • ".join(insights[:3])  # Return top 3 insights
    
    # Generate or retrieve insights
    if st.session_state.get("insights") is None or city_changed or timezone_changed:
        st.session_state["insights"] = get_city_insights(st.session_state.selected_city)
    
    # Display insights
    if st.session_state.get("insights"):
        st.info(f"💡 **Quick insights:** {st.session_state['insights']}")
    
    # Quick Actions
    if st.button("🔄 Refresh", type="primary"):        
        with st.spinner("Getting latest data..."):
            weather_data = fetch_enhanced_weather(st.session_state.selected_city, user_timezone)
            if weather_data:
                st.session_state.weather_data[st.session_state.selected_city] = weather_data
                st.session_state.last_fetch_time = weather_data['timestamp_local']
                # Regenerate insights with new data
                st.session_state["insights"] = get_city_insights(st.session_state.selected_city)
                # st.experimental_rerun()
                st.success("Updated!")

# 🎨 Dynamic Styling
city_info = CITY_DATA[st.session_state.selected_city]
city_name = st.session_state.selected_city

st.markdown(f"""
<style>
.stApp {{
    background-attachment: fixed;
}}

/* Enhanced readability */
.main-content {{
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(10px);
    margin: 1rem 0;
}}

.decision-card {{
    background: rgba(255, 255, 255, 0.95);
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    border-left: 5px solid #00AA00;
    margin: 1rem 0;
    transition: all 0.3s ease;
}}

.decision-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
}}

.alert-card {{
    background: rgba(255, 0, 0, 0.1);
    border: 2px solid #FF4444;
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
}}

.hourly-card {{
    background: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    margin: 0.5rem;
    min-width: 120px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}}

.metric-big {{
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    margin: 1rem 0;
}}

.metric-label {{
    font-size: 1.2rem;
    color: #666;
    text-align: center;
}}

.timezone-info {{
    background: rgba(0, 255, 0, 0.1);
    border: 1px solid #00AA00;
    border-radius: 8px;
    padding: 0.5rem;
    margin: 0.5rem 0;
    font-size: 0.9rem;
}}

/* Text visibility */
.stApp, .stApp * {{
    color: #FFFFFF !important;
}}

.decision-card *, .hourly-card * {{
    color: #000000 !important;
}}

.stButton button {{
    color: #ffffff !important;
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
.stDeployButton {{display:none;}}
</style>
""", unsafe_allow_html=True)

# 🌟 Conditional Dashboard Header
weather_data = st.session_state.weather_data.get(st.session_state.selected_city)

if weather_data:
    # Show personalized header when data is available
    st.markdown(f"""
    <div class="main-content">
        <h1 style="text-align: center; font-size: 2.5rem; margin-bottom: 0;">
            Weather Insights for {st.session_state.user_persona} in {city_name} {city_info['icon']}
        </h1>
        <div class="timezone-info" style="text-align: center; margin-top: 1rem;">
            <strong>Your Time:</strong> {current_user_time.strftime('%H:%M:%S %Z')} |
            <strong>Your Timezone:</strong> {st.session_state.user_timezone} |
            <strong>City Time:</strong> {city_current_time.strftime('%H:%M:%S %Z')}
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Show generic header for new users
    st.markdown(f"""
        <div class="main-content">
            <h1 style="text-align: center; font-size: 2.5rem; margin-bottom: 0;">
                Smart Weather Forecast Dashboard
            </h1>
            <div class="timezone-info" style="text-align: center; margin-top: 1rem;">
                <strong>Your Time:</strong> {current_user_time.strftime('%H:%M:%S %Z')}
            </div>
        </div>
    """, unsafe_allow_html=True)

if weather_data:
    
    # 🚨 Priority Alerts Section (Most Important)
    alerts = []
    current_temp = weather_data.get("current_temperature", 20)
    
    if current_temp > 35:
        alerts.append({"type": "extreme_heat", "message": f"🔥 HEAT WARNING: {current_temp}°C - Take cooling measures", "priority": "HIGH"})
    elif current_temp < 0:
        alerts.append({"type": "extreme_cold", "message": f"❄️ FREEZE WARNING: {current_temp}°C - Risk of hypothermia", "priority": "HIGH"})
    
    if weather_data.get("air_quality", 50) > 150:
        alerts.append({"type": "poor_air", "message": f"😷 AIR QUALITY ALERT: AQI {weather_data.get('air_quality', 0)} - Limit outdoor activity", "priority": "HIGH"})
    
    if weather_data.get("uv_index", 0) > 8:
        alerts.append({"type": "high_uv", "message": f"☀️ UV WARNING: Index {weather_data.get('uv_index', 0)} - Sun protection essential", "priority": "MEDIUM"})
    
    # Display Priority Alerts
    if alerts:
        st.markdown("## 🚨 IMMEDIATE ATTENTION NEEDED")
        for alert in alerts:
            color = "#FF4444" if alert["priority"] == "HIGH" else "#FF8800"
            st.markdown(f"""
            <div class="alert-card" style="border-color: {color};">
                <h3 style="color: {color} !important;">{alert['message']}</h3>
            </div>
            """, unsafe_allow_html=True)
    
    # 🎯 Key Decision Metrics (Only 3-5 that matter)
    st.markdown("## 🎯 Your Key Numbers Right Now")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        trend_icon = "📈" if weather_data.get("trend", "rising") == "rising" else "📉"
        st.metric(
            label="🌡️ Current Temp",
            value=f"{weather_data.get('current_temperature', 0)}°C",
            delta=f"Feels {weather_data.get('feels_like', 0)}°C",
            help="What it feels like right now"
        )
    
    with col2:
        today_high= weather_data.get('today_high', 0)
        today_low= weather_data.get('today_low', 0)
        today_range = today_high - today_low
        st.metric(
            label="📅 Today's Range",
            value=f"{today_low}° to {today_high}°",
            delta=f"{today_range}° swing",
            help="Temperature variation today"
        )
    
    with col3:
        tomorrow_high= weather_data.get('tomorrow_high', 0)
        today_high= weather_data.get('today_high', 0)
        tomorrow_change = tomorrow_high - today_high
        st.metric(
            label="🌅 Tomorrow's High",
            value=f"{tomorrow_high}°C",
            delta=f"{tomorrow_change:+.1f}° vs today",
            help="How tomorrow compares to today"
        )
    
    with col4:
        current_temp= weather_data.get('current_temperature', 22)
        comfort_score = max(0, min(10, 10 - abs(current_temp - 22) / 3))
        confidence = weather_data.get('confidence', 0)
        st.metric(
            label="😊 Comfort Score",
            value=f"{comfort_score:.1f}/10",
            delta=f"{confidence}% confident",
            help="How comfortable you'll feel outside"
        )
    
    with col5:
        # Air quality color coding
        aqi = weather_data.get('air_quality', 50)
        aqi_color = "#00AA00" if aqi < 100 else "#FFAA00" if aqi < 150 else "#FF4444"
        aqi_status = "Good" if aqi < 100 else "Satisfactory" if aqi < 150 else "Poor"
        st.metric(
            label="🌬️ Air Quality",
            value=f"{aqi} ({aqi_status})",
            delta=f"{aqi_status}",
            help="Air pollution levels"
        )
    
    # 📊 Persona-Specific Decision Support
    st.markdown(f"## 💡 Smart Recommendations for {st.session_state.user_persona}s")
    
    persona = USER_PERSONAS[st.session_state.user_persona]
    recommendations = []
    
    # Generate persona-specific recommendations
    if st.session_state.user_persona == "Commuter":
        current_temp = weather_data.get('current_temperature', 20)
        wind_speed = weather_data.get('wind_speed', 0)
        air_quality = weather_data.get('air_quality', 50)
        
        if current_temp < 5:
            recommendations.append("🚗 Consider driving instead of walking - very cold conditions")
        if wind_speed > 20:
            recommendations.append("🌪️ Allow extra travel time - strong winds may cause delays")
        if air_quality > 100:
            recommendations.append("😷 Consider indoor routes or wear a mask during commute")
        
    elif st.session_state.user_persona == "Event Planner":
        humidity = weather_data.get('humidity', 50)
        tomorrow_high = weather_data.get('tomorrow_high', 20)
        uv_index = weather_data.get('uv_index', 3)
        
        if humidity > 75:
            recommendations.append("💧 High humidity - ensure adequate ventilation and cooling")
        if tomorrow_high > 30:
            recommendations.append("☀️ Hot tomorrow - arrange shade, water stations, and cooling areas")
        if uv_index > 6:
            recommendations.append("🕶️ Provide sunscreen and recommend protective clothing")
        
    elif st.session_state.user_persona == "Outdoor Activity":
        current_temp = weather_data.get('current_temperature', 20)
        uv_index = weather_data.get('uv_index', 3)
        wind_speed = weather_data.get('wind_speed', 0)
        
        if current_temp > 32:
            recommendations.append("🔥 Heat safety protocol - frequent breaks and hydration required")
        if uv_index > 7:
            recommendations.append("☀️ High UV exposure - protective clothing and sunscreen mandatory")
        if wind_speed > 25:
            recommendations.append("💨 Strong winds - secure equipment and avoid high work")
    
    elif st.session_state.user_persona == "Tourist":
        current_temp = weather_data.get('current_temperature', 20)
        humidity = weather_data.get('humidity', 50)
        tomorrow_high = weather_data.get('tomorrow_high', 20)
        today_high = weather_data.get('today_high', 20)
        
        if current_temp > 25:
            recommendations.append("👕 Perfect weather for outdoor sightseeing")
        if humidity < 50:
            recommendations.append("📸 Low humidity - great conditions for photography")
        if tomorrow_high < today_high - 5:
            recommendations.append("🧥 Pack layers - tomorrow will be significantly cooler")
    
    # Display recommendations
    if recommendations:
        for i, rec in enumerate(recommendations[:3]):  # Limit to 3 most important
            st.markdown(f"""
            <div class="decision-card">
                <h4 style="color: #000000 !important; margin-bottom: 0.5rem;">{rec}</h4>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="decision-card">
            <h4 style="color: #000000 !important;">✅ Weather conditions are optimal for your activities today!</h4>
        </div>
        """, unsafe_allow_html=True)
    
    # ⏰ Hourly Forecast (Google Weather Style) with Timezone Awareness
    st.markdown("## ⏰ Next 12 Hours - Plan Your Day")
    
    # Create horizontal scrollable hourly forecast
    hourly_data = weather_data.get("hourly_forecast", [])[:12]  # Next 12 hours
    
    if hourly_data and len(hourly_data) > 6:
        cols = st.columns(min(6, len(hourly_data)))
    
        for i, hour_data in enumerate(hourly_data[:6]):  # Show first 6 hours
            with cols[i]:
                temp = hour_data["temperature"]
                temp_color = "#FF4444" if temp > 30 else "#4444FF" if temp < 5 else "#00AA00"
                
                # Use timezone-aware time display
                hour_display = hour_data.get("hour", hour_data.get("hour_display", "00:00"))
                
                st.markdown(f"""
                <div class="hourly-card">
                    <div style="font-size: 0.9rem; color: #666 !important;">{hour_display}</div>
                    <div style="font-size: 2rem; margin: 0.5rem 0;">{hour_data['icon']}</div>
                    <div style="font-size: 1.3rem; font-weight: bold; color: {temp_color} !important;">{temp}°</div>
                    <div style="font-size: 0.8rem; color: #888 !important;">UV {hour_data['uv_index']}</div>
                    {f'<div style="font-size: 0.7rem; color: #FF4444 !important;">⚠️ Alert</div>' if hour_data['alerts'] else ''}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Hourly forecast data is not available. Click '🔄 Refresh' to fetch the latest data.")
    
    # 📈 Smart Trend Analysis with Timezone-Aware Labels
    if len(hourly_data) >= 12:
        st.markdown("## 📈 Temperature Trend Analysis")
        
        # Create trend chart with timezone-aware times
        times = []
        temps = []
        
        for i, h in enumerate(hourly_data[:12]):
            if 'datetime' in h:
                # Use the timezone-aware datetime for display
                times.append(h['datetime'].strftime('%H:%M'))
            else:
                times.append(h.get("hour", h.get("hour_display", f"{i}:00")))
            temps.append(h.get("temperature", 20))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=times,
            y=temps,
            mode='lines+markers',
            name='Temperature',
            line=dict(width=3, color='#00AA00'),
            marker=dict(size=8)
        ))
        
        # Add comfort zone
        fig.add_hline(y=22, line_dash="dash", line_color="green", annotation_text="Comfort Zone", annotation_position="bottom right")
        
        fig.update_layout(
            title=f"Next 12 Hours Temperature Trend (Your Time: {st.session_state.user_timezone})",
            title_font=dict(size=18, color="white"),
            xaxis=dict(
                title=dict(
                    text="Time (Next 12 Hours)",
                    font=dict(size=16, color="white")
                ),
                tickfont=dict(size=12, color="white"),
                showgrid=True,
                gridcolor="gray"
            ),
            yaxis=dict(
                title=dict(
                    text="Temperature (°C)",
                    font=dict(size=16, color="white")
                ),
                tickfont=dict(size=12, color="white"),
                showgrid=True,
                gridcolor="gray"
            ),
            legend=dict(
                font=dict(size=12, color="white"),
                bgcolor="rgba(0,0,0,0)"
            ),
            plot_bgcolor="rgba(0,0,0,0)",  
            paper_bgcolor="rgba(0,0,0,0)" 
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Smart insights from the trend
        temp_change = temps[-1] - temps[0]
        if abs(temp_change) > 5:
            direction = "rising" if temp_change > 0 else "falling"
            st.info(f"🌡️ **Temperature Alert**: {abs(temp_change):.1f}°C {direction} over next 12 hours. Plan accordingly!")

else:
    # First-time user experience
    st.markdown("""
    <div class="main-content">
        <h2>👋 Welcome to Smart Weather Decisions!</h2>
        <p>Get weather insights that actually help you make better decisions.</p>
        <p>🎯 <strong>What makes this different?</strong></p>
        <ul>
            <li>✅ Shows only the 3-5 numbers that matter for YOUR role</li>
            <li>🚨 Immediate alerts for conditions that need your attention</li>
            <li>💡 Specific recommendations based on what you need to decide</li>
            <li>🌍 Timezone-aware forecasts that show times in your local zone</li>
            <li>📱 Mobile-friendly design that works everywhere</li>
            <li>⏰ Hourly forecasts to plan your entire day</li>
        </ul>
        <p><strong>First, select your timezone in the sidebar, then click "🔄 Refresh" to get started!</strong></p>
    </div>
    """, unsafe_allow_html=True)

# 📱 Mobile-optimized footer with timezone-aware last update
if st.session_state.last_fetch_time and weather_data is not None: 
    # Calculate how long ago the update was
    time_ago = TimezoneManager.calculate_time_ago(st.session_state.last_fetch_time, current_user_time)
    
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; opacity: 0.7;">
        <strong>Last updated:</strong> {st.session_state.last_fetch_time.strftime('%H:%M:%S %Z')} ({time_ago}) | 
        <strong>Data accuracy:</strong> {weather_data.get('confidence', 'N/A')}% | 
        <strong>Your timezone:</strong> {st.session_state.user_timezone}
    </div>
    """, unsafe_allow_html=True)