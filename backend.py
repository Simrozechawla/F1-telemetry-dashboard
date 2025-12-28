from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/telemetry")
def get_telemetry():
    """
    SAFE telemetry endpoint
    - No ML training
    - No undefined variables
    - Always returns valid JSON
    """

    # --- Simulated live telemetry ---
    avg_speed = random.uniform(220, 300)
    avg_rpm = random.uniform(8000, 11000)

    # --- AI STATUS ---
    status = "DROPPING" if avg_speed < 240 else "NORMAL"

    # --- SPEED PREDICTION (SAFE LOGIC) ---
    if avg_speed > 270:
        predicted_speed = avg_speed - random.uniform(5, 15)
    elif avg_speed < 230:
        predicted_speed = avg_speed + random.uniform(5, 15)
    else:
        predicted_speed = avg_speed + random.uniform(-5, 5)

    predicted_speed = round(max(0, predicted_speed), 1)

    # --- DRIVER BEHAVIOR CLASSIFICATION ---
    throttle_proxy = (avg_speed / 330) * 100

    if avg_speed > 270 and throttle_proxy > 70:
        driver_behavior = "AGGRESSIVE"
    elif avg_speed < 220 and throttle_proxy < 40:
        driver_behavior = "CONSERVATIVE"
    elif abs(predicted_speed - avg_speed) < 5:
        driver_behavior = "SMOOTH"
    else:
        driver_behavior = "ERRATIC"

    return {
        "avg_speed": round(avg_speed, 1),
        "avg_rpm": round(avg_rpm),
        "status": status,
        "predicted_speed": predicted_speed,
        "driver_behavior": driver_behavior
    }
