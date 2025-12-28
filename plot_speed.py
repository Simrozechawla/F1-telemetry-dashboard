import fastf1
import matplotlib.pyplot as plt

fastf1.Cache.enable_cache('cache')

session = fastf1.get_session(2023, 'Monza', 'R')
session.load()

lap = session.laps.pick_driver('VER').pick_fastest()
telemetry = lap.get_telemetry()

plt.plot(telemetry['Distance'], telemetry['Speed'])
plt.xlabel("Distance (m)")
plt.ylabel("Speed (km/h)")
plt.title("Speed vs Distance (Fastest Lap)")
plt.show()
