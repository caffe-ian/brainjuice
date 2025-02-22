import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("MONGO")
cluster = motor.motor_asyncio.AsyncIOMotorClient(db_url, serverSelectionTimeoutMS=20000)
db = cluster['maindb']
print("Connected to Database")