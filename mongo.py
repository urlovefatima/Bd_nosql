from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[MONGO_DB_NAME]
    users_collection = db['users']
    reservations_collection = db['reservations']
    events_collection = db['events']
    print("Connexion à MongoDB établie avec succès")
except Exception as e:
    print(f"Erreur de connexion MongoDB: {e}")
    db = None
    users_collection = None
    reservations_collection = None
    events_collection = None

print(f"MONGO_DB_NAME: {MONGO_DB_NAME}")


