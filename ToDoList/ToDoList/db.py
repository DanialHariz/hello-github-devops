#db.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(uri)
    client.server_info()  # Force connection on a request as the
                          # connect=True parameter of MongoClient seems
                          # to be useless here
    print("successfully connected")
except Exception as e:
    print("Connection failed:", e)

def get_db():
    return client["ToDo"]  # Change to your actual database name if different