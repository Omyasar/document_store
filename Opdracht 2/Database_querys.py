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
    CREATE TABLE products(
        _id serial PRIMARY KEY,
        name varchar not null unique,
        brand VARCHAR,
        gender VARCHAR,
        category  VARCHAR,
        sub_category VARCHAR,
        sub_sub_category VARCHAR,
        price int not null,
        target_group VARCHAR,
        doelgroep bool,
        stock INTEGER,
        herhaalaankopen bool,
        series VARCHAR,
        predict_out_of_stock_date date

    )
""")

psql_cursor.execute("""
    CREATE TABLE profiles(
    _id serial PRIMARY KEY,
    
    )
""")

psql_cursor.execute("""
    CREATE TABLE sessions(
    _id serial PRIMARY KEY char(50),
    
    
    )
""")

psql_conn.commit()

psql_cursor.close()
psql_conn.close()