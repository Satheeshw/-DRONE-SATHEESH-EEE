import streamlit as st
import time
import random
import plotly.graph_objects as go
from PIL import Image
import os

# Initialize page state if not set
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Dummy drone telemetry data generator
def simulate_drone_data():
    return {
        'Battery Voltage': round(random.uniform(10.0, 12.6), 2),
        'Temperature': round(random.uniform(30.0, 40.0), 2),
        'Altitude': round(random.uniform(700, 800), 2),
        'Roll': round(random.uniform(-180, 180), 2),
        'Pitch': round(random.uniform(-90, 90), 2),
        'Yaw': round(random.uniform(0, 360), 2),
        'Latitude': round(random.uniform(-90, 90), 6),
        'Longitude': round(random.uniform(-180, 180), 6),
        'Connection Health': random.choice(['Excellent', 'Good', 'Poor', 'No Signal'])
    }

# Home Page
def home_page():
    st.title("Drone Telemetry Monitoring System")
    
    # Option 1: Use a placeholder image if your image isn't available
    try:
        st.image("drone.jpg", width=700)  # Changed to .jpg
    except:
        st.image(Image.new('RGB', (700, 400), color='gray'))  # Fallback gray placeholder
    
    # Option 2: Use an online image
    # st.image("https://example.com/drone_image.jpg", width=700)

    st.subheader("About Our Drone")
    with st.expander("Drone Specifications"):
        st.markdown("""
        Model: DJI Mavic 3 Enterprise  
        Type: Quadcopter  
        Weight: 920 g  
        Max Flight Time: 45 minutes  
        Max Speed: 21 m/s (47 mph)  
        Max Transmission Range: 15 km  
        Camera: 4/3 CMOS, 20MP  
        Battery: 5000 mAh LiPo (12V)  
        Sensors: GPS, IMU, Vision System, Barometer  
        """)

    with st.expander("Key Features"):
        st.markdown("""
        - Real-time telemetry monitoring  
        - Advanced flight control system  
        - High-precision GPS positioning  
        - Multiple safety features including obstacle avoidance  
        - Weather-resistant design  
        - Long-range transmission system  
        """)

    with st.expander("Monitoring Capabilities"):
        st.markdown("""
        Our system tracks and displays:
        - Battery status (voltage levels and health) 🔋  
        - Flight dynamics (roll, pitch, yaw) 🎚📐🧭  
        - Environmental data (temperature, altitude) 🌡🗻  
        - Position data (GPS coordinates) 🌍🌎  
        - Connection status (signal strength) 📶  
        """)

    st.markdown("""
    ### 📊 Real-time Telemetry Dashboard
    Access the dashboard to monitor all critical drone parameters in real-time.
    """)

    if st.button("Go to Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

# Dashboard Page with icons
def dashboard_page():
    st.title("📡 Drone Telemetry Dashboard")

    if st.button("⬅ Back to Home"):
        st.session_state.page = 'home'
        st.rerun()

    container = st.empty()

    while True:
        try:
            drone_data = simulate_drone_data()

            with container.container():
                col1, col2, col3 = st.columns(3)
                col1.metric("🔋 Battery Voltage", f"{drone_data['Battery Voltage']} V")
                col2.metric("🌡 Temperature", f"{drone_data['Temperature']}°C")
                col3.metric("🗻 Altitude", f"{drone_data['Altitude']} m")

                gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=drone_data['Battery Voltage'],
                    title={'text': "🔋 Battery Voltage"},
                    delta={'reference': 12},
                    gauge={
                        'axis': {'range': [0, 12]},
                        'bar': {'color': "black"},
                        'steps': [
                            {'range': [0, 4], 'color': "red"},
                            {'range': [4, 8], 'color': "yellow"},
                            {'range': [8, 12], 'color': "green"},
                        ],
                    }
                ))
                st.plotly_chart(gauge, use_container_width=True, key=f"gauge_{time.time()}")

                col4, col5, col6 = st.columns(3)
                col4.metric("🎚 Roll", f"{drone_data['Roll']}°")
                col5.metric("📐 Pitch", f"{drone_data['Pitch']}°")
                col6.metric("🧭 Yaw", f"{drone_data['Yaw']}°")

                col7, col8 = st.columns(2)
                col7.metric("🌍 Latitude", f"{drone_data['Latitude']}°")
                col8.metric("🌎 Longitude", f"{drone_data['Longitude']}°")

                st.markdown(f"📶 *Connection Health:* {drone_data['Connection Health']}")

            time.sleep(1)

        except Exception as e:
            st.error("Something went wrong:")
            st.exception(e)
            break

# Page Routing
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'dashboard':
    dashboard_page()