import pymongo
from pymongo import MongoClient
import psycopg2
import random

# Globale variabele voor mongodb
CLIENT = MongoClient()
mongo_db = CLIENT["huwebshop"]
product_collection = mongo_db["products"]

# Postgres connectie maken
psql_conn = psycopg2.connect(
    host="localhost",
    database="document_store",
    user="postgres",
    password="farmainterim",
    port=5433)

psql_cursor = psql_conn.cursor()

psql_cursor.execute("""
    CREATE TABLE product_test(
        _id serial PRIMARY KEY,
        brand VARCHAR,
        colour VARCHAR,
        fast_mover bool
    )
""")

psql_conn.commit()

psql_cursor.close()
psql_conn.close()