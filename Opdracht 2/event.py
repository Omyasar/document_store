from pymongo import MongoClient
import psycopg2

# mongodb connectie
client = MongoClient()
db = client["huwebshop"]
event_collection = db["sessions"]

# pgadmin connectie
psql_conn = psycopg2.connect(
    host="localhost",
    database="huwebshop",
    user="postgres",
    password="1234",
    port=5432)

psql_cursor = psql_conn.cursor()


# get event data van mongodb
def get_event_data():
    test_event = []
    for doc in event_collection.find():
        try:
            events_list = doc['events']

            for event in events_list:
                events_action = event['action']
                events_pagetype = event['pagetype']

                test_event.append(
                    {'action': events_action, 'pagetype': events_pagetype})
        except KeyError:
            continue

    return test_event


get_event_data()


# insert into database
def insert_data(events):
    for event in events:
        psql_cursor.execute(
            "INSERT INTO events (action, pagetype) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (event['action'], event['pagetype'])
        )
    psql_conn.commit()
    print("inserted!!")


insert_data(get_event_data())
