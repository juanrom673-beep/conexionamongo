import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

usuario = os.getenv("Mongo_User")
password = os.getenv("Mongo_Password")
cluster = os.getenv("Mongo_Cluster")
base_datos = os.getenv("Mongo_db")
coleccion_nombre = os.getenv("Mongo_Colleccion")

database = base_datos
collection = coleccion_nombre

uri = f"mongodb+srv://{usuario}:{password}@{cluster}/"