import asyncio
import threading
import unittest
from unittest.mock import patch, MagicMock
from shared.mqtt_client import MQTTClient
from device import Device  # Update the import path according to your project structure


class TestDevice(unittest.TestCase):

    def setUp(self):
        self.mock_mqtt_client = MagicMock(spec=MQTTClient)
        self.device_id = 123
        self.status_topic = "device/status"
        self.command_topic = "device/command"
        self.response_topic = "device/response"
        self.device = Device(self.device_id, self.mock_mqtt_client, self.status_topic, self.command_topic,
                             self.response_topic)

    @patch('device.Command')
    def test_on_command_echo(self, mock_command):
        # Mocking the incoming MQTT message
        mock_message = MagicMock()
        mock_message.payload.decode.return_value = '{"action": "echo", "parameters": {"message": "Test Message"}}'

        # Mocking the Command class to return a specific action
        mock_command.return_value.action = "echo"
        mock_command.return_value.parameters = {"message": "Test Message"}

        # Test on_command with an echo action
        self.device.on_command(None, None, mock_message)

        # Assert publish method called with correct arguments
        self.mock_mqtt_client.publish.assert_called_with(
            self.response_topic,
            '{"device_id": "123", "echoed_message": "Test Message"}'
        )

    @patch('device.Command')
    def test_on_command_unsupported(self, mock_command):
        """
        Test on_command method with an unsupported command action.
        """
        # Mocking the incoming MQTT message for an unsupported action
        mock_message = MagicMock()
        mock_message.payload.decode.return_value = '{"action": "unsupported", "parameters": {}}'

        mock_command.return_value.action = "unsupported"
        mock_command.return_value.parameters = {}

        self.device.on_command(None, None, mock_message)

        # Assert that publish is not called for an unsupported action
        self.mock_mqtt_client.publish.assert_not_called()

    def test_report_status(self):
        """
        Test report_status method for publishing status updates.
        """
        with patch('device.Status') as mock_status:
            # Prepare the fake status JSON
            mock_status.generate_fake_status.return_value.json.return_value = '{"status": "ok"}'

            # Run the report_status coroutine within an event loop
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.device.report_status())

            # Check if the publish method was called correctly
            self.mock_mqtt_client.publish.assert_called_with(
                self.status_topic,
                '{"status": "ok"}'
            )

    def test_start(self):
        """
        Test start method to ensure MQTT client loop and status report are started.
        """
        with patch('asyncio.run'):
            with patch.object(self.device, 'report_status'):
                self.device.start()
                self.device.mqtt_client.start.assert_called_once()
                self.device.report_status.assert_called_once()


if __name__ == '__main__':
    unittest.main()
