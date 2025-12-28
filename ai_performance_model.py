import fastf1
import numpy as np
from sklearn.ensemble import RandomForestClassifier

fastf1.Cache.enable_cache('cache')

# Load session
session = fastf1.get_session(2023, 'Monza', 'R')
session.load()

lap = session.laps.pick_driver('VER').pick_fastest()
telemetry = lap.get_telemetry()

window = 10
features = []
labels = []

# Build dataset
for i in range(window, len(telemetry)-1):
    window_data = telemetry.iloc[i-window:i]

    avg_speed = window_data['Speed'].mean()
    speed_std = window_data['Speed'].std()
    avg_rpm = window_data['RPM'].mean()
    throttle_use = window_data['Throttle'].mean()

    # Simple degradation rule (labeling)
    next_speed = telemetry.iloc[i+1]['Speed']
    label = 1 if next_speed < avg_speed * 0.97 else 0  # 1 = degrading

    features.append([avg_speed, speed_std, avg_rpm, throttle_use])
    labels.append(label)

X = np.array(features)
y = np.array(labels)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

print("AI model trained successfully!")
