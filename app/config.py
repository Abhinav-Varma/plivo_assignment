import os
from dotenv import load_dotenv

load_dotenv()

PLIVO_AUTH_ID = os.getenv("PLIVO_AUTH_ID")
PLIVO_AUTH_TOKEN = os.getenv("PLIVO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("FROM_NUMBER")
TO_NUMBER = os.getenv("TO_NUMBER")
ASSOCIATE_NUMBER = os.getenv("ASSOCIATE_NUMBER")
BASE_URL = os.getenv("BASE_URL")
