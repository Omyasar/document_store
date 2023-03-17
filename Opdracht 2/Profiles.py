import psycopg2
from pymongo import MongoClient

# Globale variabele voor mongodb
CLIENT = MongoClient()
mongo_db = CLIENT["huwebshop"]
profile_collection = mongo_db['profiles']

# Postgres connectie maken
psql_conn = psycopg2.connect(
    host="localhost",
    database="document_store",
    user="postgres",
    password="farmainterim",
    port=5433)

test_profiles = []
psql_cursor = psql_conn.cursor()


def all_profiles_info():
    for doc in profile_collection.find():
        try:
            profile_uniques = doc['unique_hash']
        except KeyError:
            continue
        test_profiles.append({'unique_hash': profile_uniques, })
        psql_cursor.execute(
            "INSERT INTO profiles VALUES (%s)",
            (profile_uniques,)
        )
        psql_conn.commit()
    print('Database succesvol gevuld. :)')


all_profiles_info()
