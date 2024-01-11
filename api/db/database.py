from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 

from .config import settings 

username = settings.db_username
ip_address = settings.hostname
password = settings.password 
db_name = settings.database

SQLALCHEMY_DB_URL = f"postgresql://{username}:{password}@{ip_address}/{db_name}"

engine = create_engine(SQLALCHEMY_DB_URL)

# To talk to the sql database:
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 

# Dependency:
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()