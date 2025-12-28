import fastf1
import time

fastf1.Cache.enable_cache('cache')

session = fastf1.get_session(2023, 'Monza', 'R')
session.load()

lap = session.laps.pick_driver('VER').pick_fastest()
telemetry = lap.get_telemetry()

for i in range(0, len(telemetry), 15):
    row = telemetry.iloc[i]
    print(f"Speed: {row['Speed']:.1f} km/h | RPM: {row['RPM']} | Throttle: {row['Throttle']}")
    time.sleep(0.5)
