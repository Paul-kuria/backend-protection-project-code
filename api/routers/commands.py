from fastapi import APIRouter, HTTPException, status, Depends
from shared.models import  Command
from mqtt_config import mqtt, topic_response, topic_command
from datetime import datetime 
from typing import List 
import json 
import schemas 
from datetime import datetime 

router = APIRouter(prefix="/commands", tags=["Commands"])
response_messages = []


@router.post("/post-command", response_model=schemas.CommandResponseView, status_code=status.HTTP_201_CREATED)
async def send_command_to_topic(command: Command): 
    """
    Endpoint to broadcast a command to devices via MQTT topic device/command

    This endpoint takes a Command object as input and publishes it to the specified MQTT topic.
    The Command object should adhere to the Command model structure. Action should be "echo", and Parameters should be a dict, with the key as "message" for this to work as expected.

    Args:
        command (Command): The Command object containing the action and parameters.

    Returns:
        dict: A dictionary indicating the status of the command sending process.
              If successful, returns {"status": "Command sent successfully!"}
              If unsuccessful, an exception is raised.

    Raises:
        Exception: Any exception encountered during the MQTT publish process, or schema not followed.
    """
    payload = command.model_dump() 
    
    # Publish the JSON payload to the MQTT topic
    try:
        mqtt.publish(topic_command, payload) #publishing mqtt topic
        # print(f"Sent {payload}!")
        return  {"status": "Command sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")


''' RESPONSE MESSAGES '''
@mqtt.subscribe(f"{topic_response}/#")
async def response_to_topic(client, topic, payload, qos, properties):
    """
    MQTT Subscription Callback for Response Messages.

    This function is called when an MQTT message is received on the specified response topic.
    It is triggered once a command message has been sent by the API.
    It decodes the payload, adds a timestamp, and appends the message to the response_messages list.

    Args:
        client: The MQTT client instance.
        topic (str): The topic on which the message was received.
        payload (bytes): The binary payload of the MQTT message.
        qos: The Quality of Service level.
        properties: Additional properties of the MQTT message.

    Returns:
        None

    Raises:
        Exception: Any exception raised during the processing of the MQTT message.
                   The exception details are logged.

    Notes:
        The decoded message is expected to be in JSON format.
        The timestamp is added to the message for tracking when the response was received.
    """
    decoded_message = str(payload.decode("utf-8")) 
    message = json.loads(decoded_message)
    message['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response_messages.append(message)



@router.get("/responses", response_model=List[schemas.ResponseView], status_code=status.HTTP_200_OK)
def mqtt_responses_to_command():
    """
    Endpoint to retrieve MQTT responses after command is sent.

    This endpoint returns a list of MQTT responses that have been received by the devices.
    The responses are expected to adhere to the ResponseView model structure.

    Returns:
        List[schemas.ResponseView]: A list of MQTT responses.

    Raises:
        HTTPException: If there is an issue retrieving the responses,
                       it raises an HTTPException with a 400 status code.
    """
    try:
        return response_messages
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
