from fastapi import APIRouter, HTTPException, status, Depends
from db.database import get_db
from typing import List 

from sqlalchemy.orm import Session
import models
import schemas 
from sqlalchemy import desc 
# from messages import received_messages
router = APIRouter(prefix="/device", tags=["Devices"])




@router.get("/all-devices",  response_model=List[schemas.DevicesView], status_code=status.HTTP_200_OK)
def get_all_devices(
    db: Session = Depends(get_db),
    limit: int = 5
):
    """
    Endpoint to retrieve all unique, non-duplicated device ids from the database messages sent.

    This endpoint returns a list of unique device ids, by querying the database and creating a set of all devices found.
    The limit (5) can be changed depending on traffic and expected number of devices

    Args:
        db (Session): SQLAlchemy database session. Dependency injection 
        limit: Number of most recent message entries to fetch from the database table

    Returns:
        List[schemas.DevicesView]: A list of devices subscribed/publishing to the mqtt client.

    Raises:
        HTTPException: If there is an issue retrieving the devices,
                       it raises an HTTPException with a 400 status code.
    """
    # Setup a list to hold distinct devices
    distinct_device_ids = set()
    unique_devices: List[schemas.DevicesView] = []

    try:
        # Fetch message entries from the database
        # all_messages = db.query(models.Status).limit(limit).all()
        all_messages = db.query(models.Status).order_by(models.Status.timestamp.desc()).limit(limit).all()

        for entry in all_messages:
            if entry.device_id not in distinct_device_ids:
                distinct_device_ids.add(entry.device_id)
                unique_devices.append(schemas.DevicesView(id=entry.id, device_id=entry.device_id))

        return unique_devices
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get("/latest-status-update/{device_id}",  response_model=schemas.StatusView, status_code=status.HTTP_200_OK)
def latest_device_status_update(
    device_id: str,
    db: Session = Depends(get_db),
):
    """
    Endpoint to retrieve the latest status update for each device.
    You can get the ID from the '/all-device' post endpoint, to parse in as the api argument.
    
    Args:
        device_id (str): Unique identifier of the device.
        db (Session): SQLAlchemy database session.


    Returns:
        schemas.StatusView: Latest status update for the specified device.

    Raises:
        HTTPException: If there is an issue retrieving the responses,
                       it raises an HTTPException with a 400 status code.
    """
    try:
        # Query the database to get the latest status updates for the device
        latest_status = db.query(models.Status).filter(
            models.Status.device_id == device_id).order_by(models.Status.timestamp.desc()).limit(1).first()
        
        return latest_status
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)