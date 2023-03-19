from pymongo import MongoClient
import psycopg2

client = MongoClient()
db = client["huwebshop"]
session_collection = db['sessions']

psql_conn = psycopg2.connect(
    host="localhost",
    database="document_store",
    user="postgres",
    password="farmainterim",
    port=5433)

psql_cursor = psql_conn.cursor()

test_sessions = []


# get all product data
def get_sessions_data():
    for i, doc in enumerate(session_collection.find()):
        if i >= 10:
            try:
                session_id = doc['_id']
                session_buid = doc['buid']
                session_start = doc['session_start']
                session_end = doc['session_end']
                session_has_sale = doc['has_sale']
                sessions_segment = doc['segment']
                session_preferences = doc['preferences']
            except KeyError:
                continue
            test_sessions.append(
                {'_id': session_id, 'buid': session_buid, 'session_start': session_start,
                 'session_end': session_end, 'has_sale': session_has_sale,
                 'segment': sessions_segment, 'preferences': session_preferences
                 })
            print(test_sessions)


get_sessions_data()

# insert into database
