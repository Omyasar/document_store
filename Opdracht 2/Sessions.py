import psycopg2
from pymongo import MongoClient

# Globale variabele voor mongodb
CLIENT = MongoClient()
mongo_db = CLIENT["huwebshop"]
profile_collection = mongo_db['profiles']
session_collection = mongo_db['sessions']

# Postgres connectie maken
psql_conn = psycopg2.connect(
    host="localhost",
    database="document_store",
    user="postgres",
    password="farmainterim",
    port=5433)

test_profiles = []
psql_cursor = psql_conn.cursor()


def all_sessions_info():
    for i,doc in enumerate(session_collection.find()):
        if i >= 1000:
            break
        try:
            session_sale = doc['has_sale']
        except KeyError:
            continue
        test_profiles.append({'has_sale': session_sale, })
        psql_cursor.execute(
            "INSERT INTO profiles VALUES (%s)",
            (session_sale,)
        )
        psql_conn.commit()
    print('Database succesvol gevuld. :)')


all_sessions_info()