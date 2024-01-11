import paho.mqtt.client as mqtt
from typing import Callable, Dict


class MQTTClient:
    """
    MQTTClient facilitates communication with an MQTT broker.

    It manages connections, subscriptions, and message handling for specified topics.

    Attributes:
        broker_address (str): The address of the MQTT broker.
        client (mqtt.Client): The Paho MQTT client instance.
        topic_handlers (Dict[str, Callable]): A dictionary mapping topics to callback functions.
    """

    def __init__(self, broker_address: str):
        """
        Initialize the MQTTClient with a broker address.

        Args:
            broker_address (str): The address of the MQTT broker.
        """
        self.broker_address: str = broker_address
        self.client: mqtt.Client = mqtt.Client()
        self.topic_handlers: Dict[str, Callable] = {}

        # Set the universal on_message callback
        self.client.on_message = self.on_message_dispatcher

        # Connect to the MQTT broker
        self.client.connect(broker_address, 1883, 60)

    def on_message_dispatcher(self, client, userdata, message):
        """
        Dispatch incoming MQTT messages to the appropriate handler based on the topic.

        Args:
            client: The MQTT client instance.
            userdata: User-defined data of any type.
            message: The MQTT message instance.
        """
        handler = self.topic_handlers.get(message.topic)
        if handler:
            handler(client, userdata, message)
            print(f"handler : {handler}")
            print(f"Messg: {str(message.payload.decode('utf-8'))}")

    def publish(self, topic: str, message: str) -> None:
        """
        Publish a message to a specified MQTT topic.

        Args:
            topic (str): The MQTT topic to publish to.
            message (str): The message to publish.
        """
        self.client.publish(topic, message)

    def subscribe(self, topic: str, callback: Callable) -> None:
        """
        Subscribe to a specified MQTT topic and register a callback for handling messages.

        Args:
            topic (str): The MQTT topic to subscribe to.
            callback (Callable): The callback function to be called when a message is received.
        """
        self.topic_handlers[topic] = callback
        self.client.subscribe(topic)

    def start(self) -> None:
        """
        Start the MQTT client loop to begin processing network events.
        """
        self.client.loop_start()
