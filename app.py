import streamlit as st
import pandas as pd
import numpy as np
import time
import joblib
import os
from rpa_engine import trigger_emergency_rpa
from train_model import train_and_save_model

# Ensure model exists for easy running
if not os.path.exists("random_forest_flood_model.pkl"):
    train_and_save_model()

rf_model = joblib.load("random_forest_flood_model.pkl")

st.set_page_config(page_title="Flood Early Warning System", layout="wide")

st.title("🌊 Live Flood Detection & Early Warning System")
st.markdown("**Student:** Durga Bahadur Basnet")

st.sidebar.header("System Controls")
live_refresh = st.sidebar.checkbox("Enable Live Refresh (Simulate ESP32)", value=False)

# ESP32 Sensor Simulation (No external API integration)
def get_sensor_data():
    return {
        "water_level": np.random.uniform(20.0, 120.0),
        "rainfall_rate": np.random.uniform(0.0, 20.0),
        "soil_saturation": np.random.uniform(40.0, 95.0),
        "temperature": np.random.uniform(20.0, 30.0)
    }

sensor_data = get_sensor_data()
features = pd.DataFrame([sensor_data])

predicted_class = rf_model.predict(features)[0]
confidence_scores = rf_model.predict_proba(features)[0]
flood_prob = confidence_scores[predicted_class] * 100

state_map = {
    0: ("NORMAL", "low", "green"),
    1: ("ADVISORY", "moderate", "blue"),
    2: ("WARNING", "high", "orange"),
    3: ("SEVERE DANGER", "critical", "red")
}

state_name, risk_text, color = state_map.get(predicted_class, state_map[0])

st.success(f"✅ {state_name} CONDITIONS: River levels within calculated margins. Risk is {risk_text}.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Water Level", f"{sensor_data['water_level']:.1f} cm", "Live Flow")
col2.metric("Flood Probability", f"{flood_prob:.1f} %", f"Risk: {risk_text.upper()}")
col3.metric("API Soil Saturation", f"{sensor_data['soil_saturation']:.1f} mm", "7-Day Memory")
col4.metric("Environment", f"{sensor_data['temperature']:.1f} °C", "Active")

st.subheader("Automation Audit Logs")
if predicted_class >= 2:
    st.error(f"⚠️ High Risk Detected (Class {predicted_class})!")
    pdf_file = trigger_emergency_rpa(predicted_class, sensor_data['water_level'], flood_prob)
    st.warning("SMS Alerts dispatched (Simulated internally).")
    with open(pdf_file, "rb") as f:
        st.download_button("Download Critical Advisory PDF", f, file_name=pdf_file)
else:
    st.info("System operating normally. No alerts triggered.")

st.subheader("📈 Real-Time Telemetry Trend")
chart_data = pd.DataFrame(
    np.random.randn(20, 2) * 5 + [sensor_data['water_level'], sensor_data['soil_saturation']],
    columns=['water_level_cm', 'api_index']
)
st.line_chart(chart_data)

if live_refresh:
    time.sleep(3)
    st.rerun()
