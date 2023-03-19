from pymongo import MongoClient
import psycopg2
import re

client = MongoClient()
db = client["huwebshop"]
profiles_collection = db["profiles"]

psql_conn = psycopg2.connect(
    host="localhost",
    database="huwebshop",
    user="postgres",
    password="1234",
    port=5432)

psql_cursor = psql_conn.cursor()


# get all product data
def get_profile_data():
    profile_list = []
    for doc in profiles_collection.find():
        try:
            count = doc['order']['count']
        except KeyError:
            continue  # skip if 'order' key is not present
        buid_list = doc['buids']
        profile_dict = {'count': count, 'buids': buid_list}
        profile_list.append(profile_dict)
    return profile_list


get_profile_data()


# insert into database
def insert_profile_data(profiles):
    for profile in profiles:
        psql_cursor.execute(
            "INSERT INTO profile (buids, count) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (profile['buids'], profile['count'])
        )
    psql_conn.commit()
    print("inserted!!")


insert_profile_data(get_profile_data())
