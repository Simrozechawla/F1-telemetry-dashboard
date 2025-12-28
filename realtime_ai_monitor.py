import fastf1
import numpy as np
import time
from sklearn.ensemble import RandomForestClassifier

fastf1.Cache.enable_cache('cache')

session = fastf1.get_session(2023, 'Monza', 'R')
session.load()

lap = session.laps.pick_driver('VER').pick_fastest()
telemetry = lap.get_telemetry()

window = 10
features = []
labels = []

# Prepare training data
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

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(features, labels)

# Real-time simulation
print("Starting AI-powered real-time monitoring...\n")

for i in range(window, len(telemetry), 5):
    w = telemetry.iloc[i-window:i]
    feature = [[
        w['Speed'].mean(),
        w['Speed'].std(),
        w['RPM'].mean(),
        w['Throttle'].mean()
    ]]

    prediction = model.predict(feature)[0]

    status = "⚠️ PERFORMANCE DROPPING" if prediction == 1 else "✅ NORMAL"
    print(status)

    time.sleep(0.5)
