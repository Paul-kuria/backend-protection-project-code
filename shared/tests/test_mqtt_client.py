import unittest
from unittest.mock import MagicMock, patch
from shared.mqtt_client import MQTTClient


class TestMQTTClient(unittest.TestCase):

    @patch('shared.mqtt_client.mqtt.Client')
    def setUp(self, mock_mqtt_client):
        """
        Set up the test case with a mocked MQTT client.
        """
        mock_mqtt_client.return_value.connect.return_value = True
        self.broker_address = "test_broker"
        self.mqtt_client = MQTTClient(self.broker_address)

    def test_publish(self):
        self.mqtt_client.client = MagicMock()
        self.mqtt_client.publish("test/topic", "test message")
        self.mqtt_client.client.publish.assert_called_with("test/topic", "test message")

    def test_subscribe(self):
        self.mqtt_client.client = MagicMock()
        callback = MagicMock()
        self.mqtt_client.subscribe("test/topic", callback)
        self.mqtt_client.client.subscribe.assert_called_with("test/topic")
        self.assertIn("test/topic", self.mqtt_client.topic_handlers)
        self.assertEqual(callback, self.mqtt_client.topic_handlers["test/topic"])

    def test_start(self):
        self.mqtt_client.client = MagicMock()
        self.mqtt_client.start()
        self.mqtt_client.client.loop_start.assert_called_once()


if __name__ == '__main__':
    unittest.main()
