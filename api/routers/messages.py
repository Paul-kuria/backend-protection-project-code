from fastapi import APIRouter, HTTPException, status, Depends
from mqtt_config import mqtt, topic_status
from db import database
from typing import List 
import json 
import schemas 
import models
from psycopg2.errors import UniqueViolation
from pydantic import ValidationError
from db.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime 

router = APIRouter(prefix="/message", tags=["Messages"])
received_messages = []
last_message_received = []

# Global variable to store latest MQTT message
latest_mqtt_message = None 

# Set up database instance
db = database.get_db()

@mqtt.subscribe(f"{topic_status}/#")
async def status_message_to_topic(client, topic, payload, qos, properties):
    """
    MQTT Subscription Callback for Response Messages.

    This function is called when an MQTT message is received from the device/status topic
    It is triggered once the devices begin broadcasting their status information which is continuous.
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

    received_messages.append(message)


@router.get("/all-status-messages", response_model=List[schemas.StatusView], status_code=status.HTTP_200_OK)
def get_all_mqtt_messages():
    """
    Endpoint to retrieve all MQTT device status details.

    This endpoint returns a list of MQTT device status responses that have been received.
    The responses are expected to adhere to the ResponseView model structure.

    Returns:
        List[schemas.StatusView]: A list of MQTT responses.

    Raises:
        HTTPException: If there is an issue retrieving the responses,
                       it raises an HTTPException with a 400 status code.
    """
    try:
        return received_messages[::-1]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)

@router.post("/post-all-status-messages", response_model=List[schemas.StatusView], status_code=status.HTTP_201_CREATED)
async def post_all_mqtt_messages(db: Session = Depends(get_db)):
    """
    Endpoint to bulk insert messages received from devices via MQTT topic device/status to the database
    This endpoint takes the list of status messages received from the status topic as input and stores it in the database. The list is in descending order of creation datetime.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        list:  List[schemas.StatusView]: List of inserted status messages.

    Raises:
        HTTPException: If an error occurs during the insertion process.
    """
    message_jsons = []
    batch_size = 100
    # Process messages received in descending order and store in database object format
    for row in received_messages[::-1]:
        try:
            # print(row)
            post = models.Status(**row)
            message_jsons.append(post)
        except Exception as e:
            print(e)
    
    # Bulk insert messages in batches
    try:
        for i in range(0, len(received_messages), batch_size):
            batch = message_jsons[i : i + batch_size]
            try:
                db.bulk_save_objects(batch)
                db.commit()
                # received_messages = []
            except UniqueViolation:
                db.rollback()
        return message_jsons
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while uploading records",
        )