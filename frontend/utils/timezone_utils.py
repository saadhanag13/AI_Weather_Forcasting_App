#frontend/utils/timezone_utils.py
import pytz
from datetime import datetime
from typing import Tuple
import streamlit as st
import streamlit.components.v1 as components

class TimezoneManager:
    COMMON_TIMEZONES= [
        "UTC",
        "America/New_York",
        "Europe/London",
        "Asia/Tokyo",
        "Australia/Sydney",
        "Asia/Kolkata",
        "Europe/Paris",
        "Europe/Berlin",
        "Europe/Moscow",
        "Asia/Shanghai",
        "Asia/Seoul",
        "Asia/Singapore",
        "Asia/Dubai",
        "America/Los_Angeles",
        "America/Toronto",
        "America/Sao_Paulo",
        "Africa/Johannesburg",
        "Europe/Istanbul",
        "Asia/Bangkok",
        "America/Mexico_City"
    ]
    
    COORDINATE_TIMEZONE_MAP = {
        (51.5085, -0.1257): "Europe/London",
        (40.7128, -74.0060): "America/New_York",
        (35.6895, 139.6917): "Asia/Tokyo",
        (-33.8688, 151.2093): "Australia/Sydney",
        (28.6139, 77.2090): "Asia/Kolkata",
        (48.8566, 2.3522): "Europe/Paris",
        (52.5200, 13.4050): "Europe/Berlin",
        (55.7558, 37.6173): "Europe/Moscow",
        (39.9042, 116.4074): "Asia/Shanghai",
        (37.5665, 126.9780): "Asia/Seoul",
        (1.3521, 103.8198): "Asia/Singapore",
        (25.276987, 55.296249): "Asia/Dubai",
        (34.0522, -118.2437): "America/Los_Angeles",
        (37.7749, -122.4194): "America/Los_Angeles",
        (43.651070, -79.347015): "America/Toronto",
        (-23.5505, -46.6333): "America/Sao_Paulo",
        (-26.2041, 28.0473): "Africa/Johannesburg",
        (41.0082, 28.9784): "Europe/Istanbul",
        (13.7563, 100.5018): "Asia/Bangkok",
        (19.4326, -99.1332): "America/Mexico_City"
    }
    
    @staticmethod
    def get_javascript_timezone_detector() -> str:
        """Returns JavaScript code to detect user's timezone"""
        return """
        <script>
            function detectUserTimezone() {
                try {
                    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
                    console.log('Detected timezone:', timezone);
                    
                    // Store in sessionStorage for persistence
                    sessionStorage.setItem('detectedTimezone', timezone);
                    
                    return timezone;
                } catch (error) {
                    console.error('Error detecting timezone:', error);
                    return 'UTC';
                }
            }
            
            // Auto-detect and log
            const detectedTz = detectUserTimezone();
            
            // Display in a div for easy copying
            document.body.innerHTML = `
                # <div style="font-family: Arial; padding: 20px; background: #f0f2f6; border-radius: 8px;">
                #     <h3>🌍 Detected Timezone</h3>
                #     # <p><strong>Your timezone:</strong> <code>${detectedTz}</code></p>
                #     <p style="color: #666; font-size: 14px;">
                #         Copy the timezone above and paste it in the sidebar input field.
                #     </p>
                # </div>
            `;
        </script>
        """

    @staticmethod
    def get_timezone_from_coordinates(lat: float, lon: float, tolerance: float = 5.0) -> str:
        
        for (coord_lat, coord_lon), timezone in TimezoneManager.COORDINATE_TIMEZONE_MAP.items():
            if (abs(lat - coord_lat) < tolerance and 
                abs(lon - coord_lon) < tolerance):
                return timezone
        
        return "UTC"  # Default fallback
    
    @staticmethod
    def render_timezone_selector() -> str:
    
        st.sidebar.header("🌍 Timezone Settings")
        
        # Detection method selection
        detection_method = st.sidebar.radio( "Choose timezone detection method:", ["Manual Selection", "By Location"], index=0 )
        
        user_timezone = "UTC"  # Default
        
        if detection_method == "Manual Selection":
            user_timezone = st.sidebar.selectbox("Select your timezone:", TimezoneManager.COMMON_TIMEZONES, index=1, help="Choose your local timezone from the list")

                
        else:  # By Location
            st.sidebar.markdown("### 📍 Location-based Detection")
            st.sidebar.info("Enter your approximate coordinates")
            
            col1, col2 = st.sidebar.columns(2)
            with col1:
                lat = st.number_input("Latitude:", value=28.6, format="%.2f", key="lat")
            with col2:
                lon = st.number_input("Longitude:", value=77.2, format="%.2f", key="lon")
            
            user_timezone = TimezoneManager.get_timezone_from_coordinates(lat, lon)
            st.sidebar.success(f"📍 Detected: {user_timezone}")

        return user_timezone
    
    @staticmethod
    def convert_utc_to_timezone(utc_time: datetime, target_timezone: str) -> datetime:

        if utc_time.tzinfo is None:
            utc_time = pytz.UTC.localize(utc_time)
        
        target_tz = pytz.timezone(target_timezone)
        return utc_time.astimezone(target_tz)
    
    @staticmethod
    def format_time_for_display(utc_time: datetime, target_timezone: str, format_string: str = '%H:%M:%S') -> Tuple[str, str, datetime]:

        if isinstance(utc_time, str):
            # Handle ISO format strings
            utc_time = datetime.fromisoformat(utc_time.replace('Z', '+00:00'))
        
        local_time = TimezoneManager.convert_utc_to_timezone(utc_time, target_timezone)
        
        formatted_time = local_time.strftime(format_string)
        timezone_abbr = local_time.strftime('%Z')
        
        return formatted_time, timezone_abbr, local_time
    
    @staticmethod
    def get_current_time_in_timezone(timezone_str: str) -> datetime:
        utc_now = datetime.now(pytz.UTC)
        return TimezoneManager.convert_utc_to_timezone(utc_now, timezone_str)
    
    @staticmethod
    def calculate_time_ago(past_time: datetime, current_time: datetime) -> str:
        time_diff = current_time - past_time
        total_seconds = int(time_diff.total_seconds())
        
        if total_seconds < 60:
            return f"{total_seconds} seconds ago"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif total_seconds < 86400:
            hours = total_seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = total_seconds // 86400
            return f"{days} day{'s' if days != 1 else ''} ago"
    
    @staticmethod
    def render_timezone_info(user_timezone: str):
        current_local = TimezoneManager.get_current_time_in_timezone(user_timezone)
        return current_local


# Convenience functions for easy import
def get_user_timezone() -> str:
    return TimezoneManager.render_timezone_selector()

def format_timestamp(utc_time: datetime, timezone: str) -> Tuple[str, str, datetime]:
    return TimezoneManager.format_time_for_display(utc_time, timezone)

def get_current_user_time(timezone: str) -> datetime:
    return TimezoneManager.get_current_time_in_timezone(timezone)