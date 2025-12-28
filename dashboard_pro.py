import fastf1
import numpy as np
import streamlit as st
import time
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="F1 AI Telemetry Monitor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- TITLE ----------
st.markdown(
    "<h1 style='text-align: center;'>🏎️ AI-Driven F1 Telemetry Monitoring Dashboard</h1>",
    unsafe_allow_html=True
)

fastf1.Cache.enable_cache('cache')

# ---------- SIDEBAR ----------
st.sidebar.header("⚙️ Controls")

season = st.sidebar.selectbox("Season", [2023])
track = st.sidebar.selectbox("Track", ["Monza"])
session_type = st.sidebar.selectbox("Session", ["R"])

session = fastf1.get_session(season, track, session_type)
session.load()

driver = st.sidebar.selectbox(
    "Driver",
    sorted(session.laps['Driver'].unique())
)

lap = session.laps.pick_driver(driver).pick_fastest()
telemetry = lap.get_telemetry()

# ---------- FEATURE ENGINEERING ----------
window = 10
features = []
labels = []

for i in range(window, len(telemetry) - 1):
    w = telemetry.iloc[i - window:i]

    avg_speed = w['Speed'].mean()
    speed_std = w['Speed'].std()
    avg_rpm = w['RPM'].mean()
    throttle = w['Throttle'].mean()

    next_speed = telemetry.iloc[i + 1]['Speed']
    label = 1 if next_speed < avg_speed * 0.97 else 0

    features.append([avg_speed, speed_std, avg_rpm, throttle])
    labels.append(label)

# ---------- MODEL ----------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(features, labels)

# ---------- PLACEHOLDERS ----------
status_placeholder = st.empty()
chart_placeholder = st.empty()

# ---------- REAL-TIME LOOP ----------
for i in range(window, len(telemetry), 5):
    w = telemetry.iloc[i - window:i]

    avg_speed = w['Speed'].mean()
    speed_std = w['Speed'].std()
    avg_rpm = w['RPM'].mean()
    throttle = w['Throttle'].mean()

    prediction = model.predict([[avg_speed, speed_std, avg_rpm, throttle]])[0]

    if prediction == 1:
        status_text = "⚠️ PERFORMANCE DROPPING"
        status_color = "#ff4b4b"
    else:
        status_text = "✅ NORMAL OPERATION"
        status_color = "#00c853"

    # ---------- KPI CARDS ----------
    with status_placeholder.container():
        col1, col2, col3 = st.columns(3)

        col1.markdown(
            f"<div style='padding:20px;border-radius:10px;background-color:{status_color};color:white;text-align:center;'>"
            f"<h3>AI Status</h3><h2>{status_text}</h2></div>",
            unsafe_allow_html=True
        )

        col2.metric("Average Speed (km/h)", f"{avg_speed:.1f}")
        col3.metric("Average RPM", f"{avg_rpm:.0f}")

    # ---------- LIVE CHART ----------
    with chart_placeholder.container():
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(w['Distance'], w['Speed'], color='blue')
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Speed (km/h)")
        ax.set_title("Live Speed Profile")
        st.pyplot(fig)

    time.sleep(0.5)
