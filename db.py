from pymongo import MongoClient

import os
from dotenv import load_dotenv
load_dotenv()

Mongo_URL=os.getenv("MONGO_URL")
client=MongoClient(Mongo_URL)

db=client["Practice_1"]
resident=db["Residents"]

complaint=db["Complaints"]

issues=db["Issues"]