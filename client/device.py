import json
import asyncio
import threading
import paho.mqtt.client as mqtt
from shared.mqtt_client import MQTTClient
from typing import Any
from shared.models import Status, Command, Response


class Device:
    """
    Represents a device in an MQTT-based communication system.

    This class handles MQTT-based commands sent to the device and publishes responses and status updates.

    Attributes:
        device_id (int): The unique identifier for the device.
        mqtt_client (MQTTClient): An instance of MQTTClient for handling MQTT communication.
        status_topic (str): MQTT topic for publishing status updates.
        command_topic (str): MQTT topic to subscribe to for receiving commands.
        response_topic (str): MQTT topic for publishing responses to commands.
    """
    def __init__(self, device_id, mqtt_client: MQTTClient, status_topic: str, command_topic: str, response_topic: str):
        """
        Initialize the Device with MQTT topics and client.

        Args:
            device_id (int): The unique identifier for the device.
            mqtt_client (MQTTClient): An instance of MQTTClient for MQTT communication.
            status_topic (str): MQTT topic for publishing status updates.
            command_topic (str): MQTT topic to subscribe to for receiving commands.
            response_topic (str): MQTT topic for publishing responses to commands.
        """
        self.device_id: int = device_id
        self.mqtt_client: MQTTClient = mqtt_client
        self.status_topic: str = status_topic
        self.command_topic: str = command_topic
        self.response_topic: str = response_topic

        # Subscribe to the command topic with a callback
        self.mqtt_client.subscribe(self.command_topic, self.on_command)

    def on_command(self, client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage) -> None:
        """
        Callback for handling commands received via MQTT.

        Args:
            client (mqtt.Client): The MQTT client instance.
            userdata: User-defined data of any type.
            message (mqtt.MQTTMessage): The received MQTT message.
        """
        print(f"Command received: {message.topic} {str(message.payload)}")
        # Implement command handling logic here
        command = Command(**json.loads(message.payload))
        if command.action == "echo":
            self.handle_echo_command(command.parameters["message"])

    def handle_echo_command(self, message: str):
        """
        Handles the 'echo' command by responding with the received message.

        Args:
            message (str): The message to be echoed back.
        """
        response = Response.generate_fake_echo_response(device_id=f"{self.device_id}", message=message)
        self.mqtt_client.publish(self.response_topic, response.json())
        print(f"Generated response: {response.json()}")

    async def report_status(self) -> None:
        """
        Continuously reports the device's status at regular intervals.
        """
        while True:
            status = Status.generate_fake_status(device_id=f"{self.device_id}")  # Replace with actual device ID
            self.mqtt_client.publish(self.status_topic, status.json())
            await asyncio.sleep(1)  # Status update interval

    def start(self) -> None:
        """
        Starts the device operations including MQTT communication and status reporting.
        """
        # Start the MQTT client loop in a separate thread
        client_thread = threading.Thread(target=self.mqtt_client.start)
        client_thread.start()

        # Start the asyncio loop for report_status
        asyncio.run(self.report_status())
