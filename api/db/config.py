import os 
import dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

class Settings():
    database: str = os.environ['POSTGRES_DB']
    hostname: str = os.environ['POSTGRES_HOST']
    db_username: str = os.environ['POSTGRES_USER']
    password: str = os.environ['POSTGRES_PASSWORD']
    port_id: int = int(os.environ['POSTGRES_PORT'])

settings = Settings()
