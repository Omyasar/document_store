from pymongo import MongoClient
import psycopg2

# mongodb connectie
client = MongoClient()
db = client["huwebshop"]
session_collection = db['sessions']

# pgadmin connectie
psql_conn = psycopg2.connect(
    host="localhost",
    database="document_store",
    user="postgres",
    password="1234",
    port=5433)

psql_cursor = psql_conn.cursor()

test_sessions = []


# get all product data
def get_sessions_data():
    for doc in session_collection.find():
        try:
            session_id = doc['_id']
            session_buid = doc['buid']
            session_start = doc['session_start']
            session_end = doc['session_end']
            session_has_sale = doc['has_sale']
            sessions_segment = doc['segment']
        except KeyError:
            continue
        test_sessions.append(
            {'_id': session_id, 'buid': session_buid, 'session_start': session_start,
             'session_end': session_end, 'has_sale': session_has_sale,
             'segment': sessions_segment})


get_sessions_data()


# insert into database
def insert_data(sessions):
    for session in sessions:
        psql_cursor.execute(
            "INSERT INTO sessions (sessions_id, buid, session_start,session_end, has_sale, segment) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            (session['_id'], session['buid'], session['session_start'], session['session_end'],
             session['has_sale'], session['segment'])
        )
    psql_conn.commit()
    print("inserted!!")


insert_data(test_sessions)
