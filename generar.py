import random
from pymongo import MongoClient
from conexion import usuario, password, cluster, database, collection

if not all([usuario, password, cluster, database, collection]):
    raise Exception("Por favor establecer todas las variables de entorno")

uri = f"mongodb+srv://{usuario}:{password}@{cluster}/"
client = MongoClient(uri)
db = client[database]
coleccion = db[collection]

productos = ["Laptop", "Tablet", "Smartphone", "Smartwatch", "Auriculares"]

print("Insertando ventas en MongoDB Atlas...")

for i in range(10):
    venta = {
        "producto": random.choice(productos),
        "cantidad": random.randint(1, 10),
        "precio": random.randint(100, 1000),
    }
    resultado = coleccion.insert_one(venta)
    print(f"[{i+1}/10] Insertado: {venta} | ID: {resultado.inserted_id}")

print("Los 10 registros fueron insertados exitosamente")