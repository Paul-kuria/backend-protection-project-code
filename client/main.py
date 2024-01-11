from shared.mqtt_client import MQTTClient
from device import Device
import socket

# MQTT settings
BROKER_ADDRESS: str = "mosquitto"  # Docker-compose service name for the broker
STATUS_TOPIC: str = "device/status"  # Topic to publish status
COMMAND_TOPIC: str = "device/command"  # Topic to subscribe for commands
RESPONSE_TOPIC: str = "device/response"  # Topic to subscribe for responses

def get_device_id():
    container_id = socket.gethostname()
    return container_id

if __name__ == "__main__":
    mqtt_client: MQTTClient = MQTTClient(BROKER_ADDRESS)
    device_id = get_device_id()
    print(device_id)
    device: Device = Device(device_id, mqtt_client, STATUS_TOPIC, COMMAND_TOPIC, RESPONSE_TOPIC)
    print("Starting device")
    device.start()
