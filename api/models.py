from db.database import Base 
from sqlalchemy import Column, Integer, String, ForeignKey, VARCHAR, Boolean, TIMESTAMP, text
from sqlalchemy.orm import relationship 

class Status(Base):
    __tablename__ = "status_messages"
    id = Column(Integer, primary_key=True, nullable=False)
    device_id = Column(String, nullable=False)
    battery_level = Column(Integer, nullable=False)
    location = Column(String, default=True)
    network_status =Column(String, nullable=False)
    storage_usage = Column(String, nullable=False)
    last_response =  Column(String, nullable=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

