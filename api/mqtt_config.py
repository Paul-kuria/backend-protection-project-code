from fastapi_mqtt import FastMQTT, MQTTConfig 
from datetime import datetime 
# Declare the mqtt broker, and topics
mqtt_broker = "mosquitto"
topic_status = "device/status"
topic_response = "device/response"
topic_command = "device/command"


# Set the mqtt configuration commands. Use default port 1883 
mqtt_config = MQTTConfig(host = mqtt_broker,
    port= 1883,
    keepalive = 60,
)


# Create an instance of the fastmqtt library
mqtt = FastMQTT(
    config=mqtt_config,
    clean_session=False
    )