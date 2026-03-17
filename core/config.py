from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("DB_USER")
password =  os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")


DATABASE_URL="postgresql+asyncpg://{user}:{password}@{db_host}:{port}/{db_name}".format(
    user = user,
    password = password,
    db_host = db_host,
    port = port,
    db_name = db_name
)

@dataclass
class Config:
    telegram_token: str
    gemini_api_key: str
    database_url: str


config = Config(
    telegram_token=os.getenv("T_BOT_KEY"),
    gemini_api_key=os.getenv("GEMINI_KEY"),
    database_url=DATABASE_URL
)

print(config)
