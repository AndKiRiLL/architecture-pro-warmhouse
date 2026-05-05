from fastapi import FastAPI, Query
import random
import uvicorn
from datetime import datetime, timezone

app = FastAPI(title="Temperature API")

# Локации
LOCATION_TO_SENSOR = {
    "Living Room": "1",
    "Bedroom": "2",
    "Kitchen": "3"
}

# Датчики
SENSOR_TO_LOCATION = {
    "1": "Living Room",
    "2": "Bedroom",
    "3": "Kitchen"
}

def generate_temperature_response(sensor_id: str, location: str):
    temperature = round(random.uniform(15.0, 35.0), 2)
    now = datetime.now(timezone.utc)
    
    return {
        "sensor_id": sensor_id,
        "sensor_type": "temperature",
        "location": location,
        "value": temperature,
        "unit": "С°",
        "status": "active",
        "timestamp": now.isoformat(),
        "description": f"Temperature sensor in {location}"
    }

@app.get("/temperature")
async def get_temperature(
    location: str = Query(default=""),
    sensorId: str = Query(default="")
):
    location = location or SENSOR_TO_LOCATION.get(sensorId, "Unknown")
    sensor_id = sensorId or LOCATION_TO_SENSOR.get(location, "0")
    
    return generate_temperature_response(sensor_id, location)

@app.get("/temperature/{sensor_id}")
async def get_temperature_by_id(sensor_id: str):
    location = SENSOR_TO_LOCATION.get(sensor_id, "Unknown")
    return generate_temperature_response(sensor_id, location)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)