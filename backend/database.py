# backend/database.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["dietDB"]

meals_collection = db["meals"]
users_collection = db["users"]
