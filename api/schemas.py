from datetime import datetime
from pydantic import BaseModel
from typing import Optional 


class StatusView(BaseModel):
    """
    Pydantic model representing the view of a device status message.
    """
    device_id: str  #"6eee65279d79",
    battery_level: int # 38 
    location: str #"8549 Chelsea Branch Apt. 257\nBatesmouth, UT 19458",
    network_status: str  #"Disconnected",
    storage_usage: str  # "121 GB / 272 GB",
    last_response: Optional[str]  #"",
    timestamp : datetime #"23-12-12 20:39:33"

    class Config:
        from_attributes = True

class CommandView(BaseModel):
    """
    Pydantic model representing a command to be sent to a device.
    """
    action: str # "echo"
    parameters: dict # {"message":"<>"}

class CommandResponseView(BaseModel):
    """
    Pydantic model representing the response to a command sent.
    """
    status: str

class ResponseView(BaseModel):
    """
    Pydantic model representing a response received once a command is successfully sent to the device.
    """
    device_id: str
    response_type: str
    response_message: str = None
    timestamp: datetime

class DevicesView(BaseModel):
    """
    Pydantic model representing a view of all devices sending/receiving messages
    """
    id: int
    device_id: str 
    
    class Config:
        from_attributes = True
