import fastf1

fastf1.Cache.enable_cache('cache')

session = fastf1.get_session(2023, 'Monza', 'R')
session.load()

laps = session.laps
print("Lap columns:\n", laps.columns)

lap = laps.pick_driver('VER').pick_fastest()
telemetry = lap.get_telemetry()

print("\nTelemetry columns:\n", telemetry.columns)
print("\nSample telemetry data:\n", telemetry.head())
