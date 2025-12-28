import fastf1
import numpy as np
import streamlit as st
import time
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="F1 AI Telemetry Monitor", layout="wide")
st.title("🏎️ AI-Driven F1 Telemetry Monitoring Dashboard")

fastf1.Cache.enable_cache('cache')

# Load data
session = fastf1.get_session(2023, 'Monza', 'R')
session.load()

driver = st.selectbox("Select Driver", session.laps['Driver'].unique())
lap = session.laps.pick_driver(driver).pick_fastest()
telemetry = lap.get_telemetry()

# Feature engineering
window = 10
features = []
labels = []

for i in range(window, len(telemetry)-1):
    w = telemetry.iloc[i-window:i]
    avg_speed = w['Speed'].mean()
    speed_std = w['Speed'].std()
    avg_rpm = w['RPM'].mean()
    throttle = w['Throttle'].mean()
    next_speed = telemetry.iloc[i+1]['Speed']
    label = 1 if next_speed < avg_speed * 0.97 else 0
    features.append([avg_speed, speed_std, avg_rpm, throttle])
    labels.append(label)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(features, labels)

# Live monitoring
placeholder = st.empty()
chart_placeholder = st.empty()

for i in range(window, len(telemetry), 5):
    w = telemetry.iloc[i-window:i]

    avg_speed = w['Speed'].mean()
    speed_std = w['Speed'].std()
    avg_rpm = w['RPM'].mean()
    throttle = w['Throttle'].mean()

    prediction = model.predict([[avg_speed, speed_std, avg_rpm, throttle]])[0]

    with placeholder.container():
        col1, col2 = st.columns(2)

        status = "⚠️ PERFORMANCE DROPPING" if prediction == 1 else "✅ NORMAL OPERATION"
        col1.metric("AI Status", status)
        col2.metric("Average Speed (km/h)", f"{avg_speed:.1f}")

    with chart_placeholder.container():
        fig, ax = plt.subplots()
        ax.plot(w['Distance'], w['Speed'])
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Speed (km/h)")
        ax.set_title("Live Speed Profile")
        st.pyplot(fig)

    time.sleep(0.5)
