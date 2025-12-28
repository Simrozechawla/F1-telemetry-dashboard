import fastf1
import numpy as np
import time

fastf1.Cache.enable_cache('cache')

session = fastf1.get_session(2023, 'Monza', 'R')
session.load()

lap = session.laps.pick_driver('VER').pick_fastest()
telemetry = lap.get_telemetry()

window = 10  # sliding window size

for i in range(window, len(telemetry), 5):
    window_data = telemetry.iloc[i-window:i]

    avg_speed = window_data['Speed'].mean()
    speed_std = window_data['Speed'].std()
    avg_rpm = window_data['RPM'].mean()
    throttle_use = window_data['Throttle'].mean()

    print(
        f"AvgSpeed: {avg_speed:.1f} | "
        f"SpeedVar: {speed_std:.2f} | "
        f"AvgRPM: {avg_rpm:.0f} | "
        f"ThrottleUse: {throttle_use:.2f}"
    )

    time.sleep(0.5)
