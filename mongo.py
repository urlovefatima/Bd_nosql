# from pymongo import MongoClient
# import os
# from dotenv import load_dotenv

# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI")
# MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# try:
#     mongo_client = MongoClient(MONGO_URI)
#     db = mongo_client[MONGO_DB_NAME]
#     print("Connexion à MongoDB établie avec succès")
# except Exception as e:
#     print(f"Erreur de connexion MongoDB: {e}")
#     db = None

# print(f"MONGO_DB_NAME: {MONGO_DB_NAME}")


from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = "mongodb://localhost:27017"
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(
    MONGO_URI,
    connect=False,  
    serverSelectionTimeoutMS=3000
)
db = client[MONGO_DB_NAME]

def check_connection():
    try:
        client.server_info()
        print("MongoDB prêt")
    except Exception as e:
        print(f"MongoDB indisponible: {e}")