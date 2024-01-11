from pydantic import BaseModel
from faker import Faker


class Command(BaseModel):
    """
    Model for a command message.
    """
    action: str
    parameters: dict = {}

    @staticmethod
    def create_echo_command(message: str) -> 'Command':
        """
        Creates an echo command with the specified message.

        Args:
            message (str): The message to be echoed back.

        Returns:
            Command: An echo command.
        """
        return Command(type="echo", payload={"message": message})


class Status(BaseModel):
    """
    Model for a status message from a mobile device.
    """
    device_id: str
    battery_level: int
    location: str
    network_status: str
    storage_usage: str
    last_response: str  = None

    @staticmethod
    def generate_fake_status(device_id: str) -> 'Status':
        """
        Generates a fake status message for a mobile device.

        Args:
            device_id (str): The ID of the device.

        Returns:
            Status: A fake status message.
        """
        faker = Faker()
        return Status(
            device_id=device_id,
            battery_level=faker.random_int(min=0, max=100),
            location=faker.address(),
            network_status=faker.random_element(elements=("Connected", "Disconnected", "Poor Connection")),
            storage_usage=f"{faker.random_int(min=10, max=128)} GB / {faker.random_int(min=128, max=512)} GB",
            last_response=""
        )


class Response(BaseModel):
    """
    Base model for responses from devices.
    """
    device_id: str
    response_type: str
    response_message: str = None

    @staticmethod
    def generate_fake_echo_response(device_id: str, message: str) -> "Response":
        """
        Create an echo response.

        Args:
            device_id (str): The ID of the responding device.
            message (str): The message to be echoed back.

        Returns:
            EchoResponse: An echo response.
        """
        return Response(device_id=device_id, response_type="echo", response_message=message)
