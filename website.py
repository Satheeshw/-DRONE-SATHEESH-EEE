import streamlit as st
import time
import random
import plotly.graph_objects as go
import pandas as pd
import pydeck as pdk
from PIL import Image

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=[
        'Time', 'Battery Voltage', 'Temperature', 'Altitude', 'Running Time', 'Roll', 'Distance Travelled'
    ])

if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

if 'camera_on' not in st.session_state:
    st.session_state.camera_on = False

if 'total_distance' not in st.session_state:
    st.session_state.total_distance = 0.0

# Simulate drone data
def simulate_drone_data():
    return {
        'Battery Voltage': round(random.uniform(10.0, 12.6), 2),
        'Temperature': round(random.uniform(30.0, 40.0), 2),
        'Altitude': round(random.uniform(700, 900), 2),
        'Roll': round(random.uniform(-180, 180), 2),
        'Pitch': round(random.uniform(-90, 90), 2),
        'Yaw': round(random.uniform(0, 360), 2),
        'Latitude': 11.0256,
        'Longitude': 77.0027,
        'Connection Health': random.choice(['Excellent', 'Good', 'Poor', 'No Signal']),
        'Speed': round(random.uniform(1.0, 5.0), 2)  # Simulated speed in m/s
    }

# Home Page
def home_page():
    st.title("🛸Drone Status Monitoring Website")

    try:
        st.image("drone.jpg", width=700)
    except:
        st.image(Image.new('RGB', (700, 400), color='gray'))

    st.subheader("📘 About Our Drone")
    with st.expander("🔧 Drone Specifications"):
        st.markdown("""
        - *Model*: DJI Mavic 3 Enterprise  
        - *Type*: Quadcopter  
        - *Weight*: 920 g  
        - *Max Flight Time*: 45 minutes  
        - *Max Speed*: 21 m/s (47 mph)  
        - *Transmission Range*: Up to 15 km  
        - *Camera*: 4/3 CMOS, 20MP with mechanical shutter  
        - *Battery*: 5000 mAh LiPo (12V)  
        - *Navigation*: GPS + GLONASS + Galileo  
        - *Sensors*: IMU, Barometer, Vision Sensors, Obstacle Avoidance  
        - *Special Features*: RTK Module, Thermal Camera, Night Operations
        """)

    st.subheader("🚀 Key Features")
    with st.expander("🧩 Show Key Features"):
        st.markdown("""
        - Real-time telemetry monitoring  
        - Long-range communication up to 15 km  
        - High-resolution thermal and RGB imaging  
        - GPS and vision-based navigation  
        - Obstacle avoidance and fail-safe return  
        - Modular payload support (e.g., camera, sensors)  
        - Live camera toggle functionality  
        - Data logging and analysis capabilities  
        """)

    st.subheader("🖥️ Monitoring Capabilities")
    with st.expander("📡 Show Monitoring Capabilities"):
        st.markdown("""
        - Battery voltage status and drop detection  
        - Altitude tracking and graphing  
        - Internal temperature tracking  
        - Roll, Pitch, and Yaw measurements  
        - Real-time location on map (Coimbatore, Tamil Nadu)  
        - Distance travelled and drone running time  
        - Connection health monitoring  
        """)

# Dashboard Page
def dashboard_page():
    st.title("📡 Drone Telemetry Dashboard")

    drone_data = simulate_drone_data()
    timestamp = pd.Timestamp.now()
    runtime = round(min(time.time() - st.session_state.start_time, 3600), 2)

    # Simulate distance = speed * 1 second
    distance_increment = drone_data['Speed'] * 1 / 1000  # convert to km
    st.session_state.total_distance += distance_increment
    distance_km = round(st.session_state.total_distance, 3)

    new_entry = pd.DataFrame([{
        'Time': timestamp,
        'Battery Voltage': drone_data['Battery Voltage'],
        'Temperature': drone_data['Temperature'],
        'Altitude': drone_data['Altitude'],
        'Running Time': runtime,
        'Roll': drone_data['Roll'],
        'Distance Travelled': distance_km
    }])

    st.session_state.history = pd.concat([st.session_state.history, new_entry]).tail(100)

    col1, col2, col3 = st.columns(3)
    col1.metric("🔋 Battery Voltage", f"{drone_data['Battery Voltage']} V")
    col2.metric("🌡 Temperature", f"{drone_data['Temperature']}°C")
    col3.metric("🗻 Altitude", f"{drone_data['Altitude']} m")

    st.plotly_chart(go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=drone_data['Battery Voltage'],
        title={'text': "Battery Voltage"},
        delta={'reference': 12.0},
        gauge={
            'axis': {'range': [0, 12]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 4], 'color': "red"},
                {'range': [4, 8], 'color': "yellow"},
                {'range': [8, 12], 'color': "green"},
            ]
        }
    )), use_container_width=True)

    col4, col5, col6 = st.columns(3)
    col4.metric("🎚 Roll", f"{drone_data['Roll']}°")
    col5.metric("📐 Pitch", f"{drone_data['Pitch']}°")
    col6.metric("🧭 Yaw", f"{drone_data['Yaw']}°")

    col7, col8 = st.columns(2)
    col7.metric("🌍 Latitude", f"{drone_data['Latitude']}°")
    col8.metric("🌎 Longitude", f"{drone_data['Longitude']}°")

    st.metric("⏱ Running Time", f"{runtime:.2f} sec")
    st.metric("📍➡📍Distance Travelled", f"{distance_km} km")
    st.markdown(f"📶 Connection Health: {drone_data['Connection Health']}")

    # Camera toggle button
    if st.button("📸 Toggle Camera"):
        st.session_state.camera_on = not st.session_state.camera_on

    camera_status = "🟢 ON" if st.session_state.camera_on else "🔴 OFF"
    st.markdown(f"*Camera Status:* {camera_status}")

    time.sleep(1)
    st.rerun()

# Graph + Map Page
def graph_page():
    st.title("📈 Location and Graph Page")

    data = st.session_state.history
    if data.empty:
        st.warning("No telemetry data available yet.")
        return

    st.subheader("📊 Temperature, Battery, Altitude, Running Time, Roll, Distance Travelled")
    st.line_chart(data.set_index("Time")[[
        'Battery Voltage', 'Temperature', 'Altitude', 'Running Time', 'Roll', 'Distance Travelled'
    ]])

    st.subheader("📍 Drone Location (Coimbatore, Tamil Nadu)")
    latitude, longitude = 11.0256, 77.0027
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v11',
        initial_view_state=pdk.ViewState(
            latitude=latitude, longitude=longitude, zoom=15),
        layers=[
            pdk.Layer('ScatterplotLayer',
                      data=pd.DataFrame({'lat': [latitude], 'lon': [longitude]}),
                      get_position='[lon, lat]',
                      get_color='[200, 30, 0, 160]',
                      get_radius=100),
        ],
    ))
    st.markdown(f"📌 *Latitude:* {latitude}  \n📌 *Longitude:* {longitude}")

# Sidebar Navigation
st.sidebar.title("📂 Navigation")
page_choice = st.sidebar.radio("Go to", ["Home", "Dashboard", "Location and Graph Page"])

if page_choice == "Home":
    st.session_state.page = 'home'
elif page_choice == "Dashboard":
    st.session_state.page = 'dashboard'
elif page_choice == "Location and Graph Page":
    st.session_state.page = 'graph'

# Load selected page
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'dashboard':
    dashboard_page()
elif st.session_state.page == 'graph':
    graph_page()
