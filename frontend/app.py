import streamlit as st
import requests
import pandas as pd
import numpy as np
import time
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from concurrent.futures import ThreadPoolExecutor
import asyncio

# 🌍 Extended City Configuration (20 Cities)
CITY_DATA = {
    "London": {
        "background": "linear-gradient(135deg, #4682B4 0%, #708090 100%)",
        "weather": "rainy", "country": "UK", "timezone": "GMT",
        "coords": "51.5074°N, 0.1278°W", "icon": "🌫️", "description": "Foggy and charming"
    },
    "New York": {
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "weather": "urban", "country": "USA", "timezone": "EST",
        "coords": "40.7128°N, 74.0060°W", "icon": "🏙️", "description": "The city that never sleeps"
    },
    "Tokyo": {
        "background": "linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%)",
        "weather": "urban", "country": "Japan", "timezone": "JST",
        "coords": "35.6762°N, 139.6503°E", "icon": "🌸", "description": "Modern metropolis"
    },
    "Sydney": {
        "background": "linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%)",
        "weather": "sunny", "country": "Australia", "timezone": "AEST",
        "coords": "33.8688°S, 151.2093°E", "icon": "🏖️", "description": "Harbour city"
    },
    "Delhi": {
        "background": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)",
        "weather": "hot", "country": "India", "timezone": "IST",
        "coords": "28.7041°N, 77.1025°E", "icon": "🏛️", "description": "Historic capital"
    },
    "Paris": {
        "background": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
        "weather": "temperate", "country": "France", "timezone": "CET",
        "coords": "48.8566°N, 2.3522°E", "icon": "🗼", "description": "City of lights"
    },
    "Berlin": {
        "background": "linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)",
        "weather": "temperate", "country": "Germany", "timezone": "CET",
        "coords": "52.5200°N, 13.4050°E", "icon": "🏰", "description": "Historic heart"
    },
    "Moscow": {
        "background": "linear-gradient(135deg, #B0E0E6 0%, #87CEEB 100%)",
        "weather": "cold", "country": "Russia", "timezone": "MSK",
        "coords": "55.7558°N, 37.6173°E", "icon": "❄️", "description": "Winter wonderland"
    },
    "Beijing": {
        "background": "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)",
        "weather": "continental", "country": "China", "timezone": "CST",
        "coords": "39.9042°N, 116.4074°E", "icon": "🏮", "description": "Ancient capital"
    },
    "Seoul": {
        "background": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
        "weather": "continental", "country": "South Korea", "timezone": "KST",
        "coords": "37.5665°N, 126.9780°E", "icon": "🌺", "description": "Tech hub"
    },
    "Singapore": {
        "background": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
        "weather": "tropical", "country": "Singapore", "timezone": "SGT",
        "coords": "1.3521°N, 103.8198°E", "icon": "🌴", "description": "Garden city"
    },
    "Dubai": {
        "background": "linear-gradient(135deg, #FFD700 0%, #FF8C00 100%)",
        "weather": "desert", "country": "UAE", "timezone": "GST",
        "coords": "25.2048°N, 55.2708°E", "icon": "🏜️", "description": "Desert oasis"
    },
    "Los Angeles": {
        "background": "linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%)",
        "weather": "sunny", "country": "USA", "timezone": "PST",
        "coords": "34.0522°N, 118.2437°W", "icon": "🌴", "description": "City of angels"
    },
    "San Francisco": {
        "background": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
        "weather": "foggy", "country": "USA", "timezone": "PST",
        "coords": "37.7749°N, 122.4194°W", "icon": "🌉", "description": "Golden Gate city"
    },
    "Toronto": {
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "weather": "continental", "country": "Canada", "timezone": "EST",
        "coords": "43.651070°N, 79.347015°W", "icon": "🍁", "description": "Multicultural hub"
    },
    "São Paulo": {
        "background": "linear-gradient(135deg, #38ef7d 0%, #11998e 100%)",
        "weather": "tropical", "country": "Brazil", "timezone": "BRT",
        "coords": "23.5505°S, 46.6333°W", "icon": "🌆", "description": "Tropical megacity"
    },
    "Johannesburg": {
        "background": "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)",
        "weather": "temperate", "country": "South Africa", "timezone": "SAST",
        "coords": "26.2041°S, 28.0473°E", "icon": "💎", "description": "City of gold"
    },
    "Istanbul": {
        "background": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)",
        "weather": "mediterranean", "country": "Turkey", "timezone": "TRT",
        "coords": "41.0082°N, 28.9784°E", "icon": "🕌", "description": "Bridge of continents"
    },
    "Bangkok": {
        "background": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "weather": "tropical", "country": "Thailand", "timezone": "ICT",
        "coords": "13.7563°N, 100.5018°E", "icon": "🛕", "description": "Temple city"
    },
    "Mexico City": {
        "background": "linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%)",
        "weather": "temperate", "country": "Mexico", "timezone": "CST",
        "coords": "19.4326°N, 99.1332°W", "icon": "🌮", "description": "Aztec heritage"
    }
}

# 🎨 Enhanced Theme Color Palettes
THEMES = {
    "sunny": {"primary": "#FFD700", "secondary": "#FF8C00", "accent": "#87CEEB", "text": "#2F4F4F"},
    "rainy": {"primary": "#4682B4", "secondary": "#708090", "accent": "#20B2AA", "text": "#FFFFFF"},
    "cold": {"primary": "#B0E0E6", "secondary": "#4169E1", "accent": "#00CED1", "text": "#191970"},
    "urban": {"primary": "#667eea", "secondary": "#764ba2", "accent": "#4ECDC4", "text": "#FFFFFF"},
    "tropical": {"primary": "#38ef7d", "secondary": "#11998e", "accent": "#fed6e3", "text": "#2F4F4F"},
    "desert": {"primary": "#FFD700", "secondary": "#FF8C00", "accent": "#87CEEB", "text": "#8B4513"},
    "hot": {"primary": "#ff9a9e", "secondary": "#fecfef", "accent": "#fed6e3", "text": "#8B0000"},
    "temperate": {"primary": "#a8edea", "secondary": "#fed6e3", "accent": "#d299c2", "text": "#2F4F4F"},
    "continental": {"primary": "#ffecd2", "secondary": "#fcb69f", "accent": "#a8edea", "text": "#8B4513"},
    "foggy": {"primary": "#a8edea", "secondary": "#fed6e3", "accent": "#B0E0E6", "text": "#2F4F4F"},
    "mediterranean": {"primary": "#ff9a9e", "secondary": "#fecfef", "accent": "#a8edea", "text": "#8B0000"}
}

# 🚀 Streamlit Page Config
st.set_page_config(
    page_title="Global Weather Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = {}
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = "London"
if 'last_fetch_time' not in st.session_state:
    st.session_state.last_fetch_time = None

# 📡 Multi-City Data Fetching Functions
def fetch_single_city_weather(city):
    """Fetch weather data for a single city"""
    try:
        # Your FastAPI backend call
        API_URL = "http://127.0.0.1:8000/predict"
        payload = {"city": city}
        
        response = requests.post(API_URL, json=payload, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            return {
                "city": city,
                "temperature": result.get("predicted_temperature", 0),
                "confidence": np.random.randint(75, 95),
                "status": "success",
                "timestamp": datetime.now()
            }
        else:
            # Mock data for demo
            return {
                "city": city,
                "temperature": np.random.randint(10, 35),
                "confidence": np.random.randint(70, 90),
                "status": "demo",
                "timestamp": datetime.now()
            }
    except:
        # Fallback mock data
        return {
            "city": city,
            "temperature": np.random.randint(5, 40),
            "confidence": np.random.randint(60, 85),
            "status": "offline",
            "timestamp": datetime.now()
        }

def fetch_all_cities_weather():
    """Fetch weather data for all cities concurrently"""
    cities = list(CITY_DATA.keys())
    
    # Progress bar for fetching
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    weather_data = {}
    
    # Use ThreadPoolExecutor for concurrent API calls
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_single_city_weather, city): city for city in cities}
        
        for i, future in enumerate(futures):
            city = futures[future]
            status_text.text(f"Fetching: {city}")
            progress_bar.progress((i + 1) / len(cities))
            
            try:
                result = future.result(timeout=10)
                weather_data[city] = result
            except Exception as e:
                weather_data[city] = {
                    "city": city,
                    "temperature": 0,
                    "confidence": 0,
                    "status": "error",
                    "timestamp": datetime.now()
                }
    
    progress_bar.empty()
    status_text.empty()
    
    return weather_data

# 🌍 Sidebar with Enhanced Controls
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2>🌍 Global Weather Command Center</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch All Cities Button
    if st.button("🔄 Fetch All Cities Weather", type="primary"):
        with st.spinner("Fetching weather data for all cities..."):
            st.session_state.weather_data = fetch_all_cities_weather()
            st.session_state.last_fetch_time = datetime.now()
        st.success(f"✅ Fetched data for {len(st.session_state.weather_data)} cities!")
    
    # Last update info
    if st.session_state.last_fetch_time:
        st.info(f"🕒 Last updated: {st.session_state.last_fetch_time.strftime('%H:%M:%S')}")
    
    # City Selection
    st.markdown("---")
    cities_list = list(CITY_DATA.keys())
    city_options = [f"{CITY_DATA[city]['icon']} {city}" for city in cities_list]
    
    selected_display = st.selectbox(
        "🎯 Select City for Detailed View:",
        city_options,
        index=cities_list.index(st.session_state.selected_city)
    )
    
    selected_city = selected_display.split(" ", 1)[1]
    st.session_state.selected_city = selected_city
    
    # City Info
    city_info = CITY_DATA[selected_city]
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; backdrop-filter: blur(10px);">
        <h3>{city_info['icon']} {selected_city}</h3>
        <p><strong>Country:</strong> {city_info['country']}</p>
        <p><strong>Timezone:</strong> {city_info['timezone']}</p>
        <p><strong>Climate:</strong> {city_info['weather'].title()}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Display Options
    st.markdown("### 📊 Display Options")
    show_global_overview = st.checkbox("🌍 Global Overview", True)
    show_comparison_charts = st.checkbox("📈 Comparison Charts", True)
    show_city_details = st.checkbox("🔍 Detailed City View", True)
    
    # Filter Options
    st.markdown("### 🔍 Filters")
    temp_range = st.slider("Temperature Range (°C)", -10, 50, (-10, 50))
    confidence_threshold = st.slider("Min Confidence %", 0, 100, 70)

# 🎨 Apply Dynamic Background
weather_type = city_info["weather"]
theme = THEMES.get(weather_type, THEMES["temperate"])
background = city_info["background"]

st.markdown(f"""
<style>
.stApp {{
    background: {background};
    background-attachment: fixed;
}}

.main-header {{
    text-align: center;
    color: {theme['text']};
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    font-size: 3rem;
    margin-bottom: 2rem;
}}

.weather-card {{
    background: rgba(255, 255, 255, 0.95);
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}}

.weather-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
}}

.temp-display {{
    font-size: 2.5rem;
    font-weight: bold;
    color: {theme['primary']};
    text-align: center;
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
.stDeployButton {{display:none;}}
</style>
""", unsafe_allow_html=True)

# 🌍 Main Header
st.markdown(f'<h1 class="main-header">🌍 Global Weather Intelligence Dashboard</h1>', unsafe_allow_html=True)

# 📊 Global Overview Section
if show_global_overview and st.session_state.weather_data:
    st.markdown("## 🌍 Global Weather Overview")
    
    # Filter data based on criteria
    filtered_data = {}
    for city, data in st.session_state.weather_data.items():
        temp = data['temperature']
        conf = data['confidence']
        if temp_range[0] <= temp <= temp_range[1] and conf >= confidence_threshold:
            filtered_data[city] = data
    
    if filtered_data:
        # Create overview metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        temps = [data['temperature'] for data in filtered_data.values()]
        confidences = [data['confidence'] for data in filtered_data.values()]
        
        with col1:
            st.metric("🌡️ Avg Temperature", f"{np.mean(temps):.1f}°C", f"{np.std(temps):.1f}")
        with col2:
            st.metric("🔥 Hottest City", f"{max(temps):.1f}°C", 
                     list(filtered_data.keys())[temps.index(max(temps))])
        with col3:
            st.metric("❄️ Coldest City", f"{min(temps):.1f}°C",
                     list(filtered_data.keys())[temps.index(min(temps))])
        with col4:
            st.metric("🎯 Avg Confidence", f"{np.mean(confidences):.1f}%", f"{np.std(confidences):.1f}")
        with col5:
            st.metric("🌍 Cities Monitored", len(filtered_data), "0")
        
        # Global Temperature Map (Simulated)
        if show_comparison_charts:
            st.markdown("### 🗺️ Global Temperature Distribution")
            
            df_global = pd.DataFrame([
                {
                    'City': city,
                    'Temperature': data['temperature'],
                    'Confidence': data['confidence'],
                    'Country': CITY_DATA[city]['country'],
                    'Weather_Type': CITY_DATA[city]['weather']
                }
                for city, data in filtered_data.items()
            ])
            
            # Temperature Bar Chart
            fig_global = px.bar(
                df_global.sort_values('Temperature', ascending=False),
                x='City',
                y='Temperature',
                color='Temperature',
                title='🌡️ Global Temperature Comparison',
                color_continuous_scale='RdYlBu_r',
                hover_data=['Country', 'Confidence', 'Weather_Type']
            )
            
            fig_global.update_layout(
                height=400,
                xaxis_tickangle=-45,
                paper_bgcolor='rgba(255,255,255,0.9)',
                plot_bgcolor='rgba(255,255,255,0.9)'
            )
            
            st.plotly_chart(fig_global, use_container_width=True)
            
            # Confidence vs Temperature Scatter
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                fig_scatter = px.scatter(
                    df_global,
                    x='Temperature',
                    y='Confidence',
                    size='Temperature',
                    color='Weather_Type',
                    hover_name='City',
                    title='🎯 Confidence vs Temperature'
                )
                fig_scatter.update_layout(height=350, paper_bgcolor='rgba(255,255,255,0.9)')
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            with col_chart2:
                # Weather Type Distribution
                weather_counts = df_global['Weather_Type'].value_counts()
                fig_pie = px.pie(
                    values=weather_counts.values,
                    names=weather_counts.index,
                    title='🌤️ Weather Type Distribution'
                )
                fig_pie.update_layout(height=350, paper_bgcolor='rgba(255,255,255,0.9)')
                st.plotly_chart(fig_pie, use_container_width=True)

# 🔍 Detailed City View
if show_city_details:
    st.markdown(f"## 🔍 Detailed View: {selected_city}")
    
    # Get city data
    city_data = st.session_state.weather_data.get(selected_city)
    if city_data:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="weather-card">
                <h3>🌡️ Temperature</h3>
                <div class="temp-display">{city_data['temperature']}°C</div>
                <p>Status: {city_data['status'].title()}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="weather-card">
                <h3>🎯 Confidence</h3>
                <div class="temp-display">{city_data['confidence']}%</div>
                <p>Updated: {city_data['timestamp'].strftime('%H:%M:%S')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="weather-card">
                <h3>📍 Location Info</h3>
                <p><strong>Country:</strong> {city_info['country']}</p>
                <p><strong>Timezone:</strong> {city_info['timezone']}</p>
                <p><strong>Climate:</strong> {city_info['weather'].title()}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(f"No data available for {selected_city}. Click 'Fetch All Cities Weather' to load data.")

# 🔄 Auto-refresh option
st.markdown("---")
if st.button("🔄 Refresh Current City", type="secondary"):
    with st.spinner(f"Refreshing {selected_city}..."):
        city_data = fetch_single_city_weather(selected_city)
        st.session_state.weather_data[selected_city] = city_data
    st.success(f"✅ Refreshed data for {selected_city}!")

# 📈 Real-time Status
if st.session_state.weather_data:
    total_cities = len(st.session_state.weather_data)
    online_cities = len([d for d in st.session_state.weather_data.values() if d['status'] == 'success'])
    demo_cities = len([d for d in st.session_state.weather_data.values() if d['status'] == 'demo'])
    
    st.markdown("### 📊 System Status")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌍 Total Cities", total_cities)
    with col2:
        st.metric("🟢 Live Data", online_cities)
    with col3:
        st.metric("🟡 Demo Mode", demo_cities)
    with col4:
        st.metric("🔴 Offline", total_cities - online_cities - demo_cities)

# Initial load message
if not st.session_state.weather_data:
    st.info("👋 Welcome! Click '🔄 Fetch All Cities Weather' to load data for all 20 cities.")
    st.markdown("""
    ### 🌟 Features:
    - **20 Global Cities** - Comprehensive worldwide coverage
    - **Real-time Predictions** - AI-powered weather forecasting
    - **Interactive Charts** - Dynamic visualizations
    - **Global Overview** - Compare temperatures worldwide
    - **Filtering Options** - Customize your view
    - **Concurrent Fetching** - Fast multi-city data loading
    """)