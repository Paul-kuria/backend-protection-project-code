from shared.mqtt_client import MQTTClient
from fastapi import FastAPI, HTTPException, status, Depends
# from .routers import status
from routers import commands, messages, devices
from typing import List 
from mqtt_config import mqtt

# Create an instance of the fastapi framework
app = FastAPI(
    title="Backend Protection Project",
    description="This is the backend api implementation to communicate to the device instances created. It connects to the mqtt client and handles the topic subscriptions and publishing to either send / receive commands and status updates.",
    version="1.0",
)
# Initialize the MQTT client and attach it to the FastAPI app
mqtt.init_app(app)

# Include routers for different endpoints
app.include_router(commands.router)
app.include_router(messages.router)
app.include_router(devices.router)

@app.get("/")
def home():
    """
    Home endpoint.

    Returns:
        dict: A welcome message.
    """
    return {"Message": "Welcome to the http api wrapper for mqtt devices"}


if __name__ == "__main__":
    # Run the FastAPI app using uvicorn
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=5000, reload=True)
