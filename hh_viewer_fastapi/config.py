import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

url = "asyncpg://"+db_user+":"+db_password+"@"+db_host+":"+db_port+"/"+db_name

TORTOISE_ORM = {
    "connections": {"default": url},
    "apps": {
        "models": {
            "models": ["vacancies.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}