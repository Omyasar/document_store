from pymongo import MongoClient
import psycopg2

# mongodb connectie
client = MongoClient()
db = client["huwebshop"]
recommendation_collection = db["profiles"]

# pgadmin connectie
psql_conn = psycopg2.connect(
    host="localhost",
    database="huwebshop",
    user="postgres",
    password="1234",
    port=5432)

psql_cursor = psql_conn.cursor()


# get recommendation data
def get_recommendation_data():
    test_recommendation = []
    for doc in recommendation_collection.find():
        try:
            segment = doc['recommendations']['segment']
            viewed_before = doc['recommendations']['viewed_before']
            previously_recommended = doc['previously_recommended']

            test_recommendation.append(
                {'segment': segment, 'viewed_before': viewed_before, 'previously_recommended': previously_recommended})
        except KeyError:
            continue
    return test_recommendation


get_recommendation_data()


# insert into database
def insert_data(recommendations):
    for recommended in recommendations:
        psql_cursor.execute(
            "INSERT INTO recommendations (segment, viewed_before, previously_recommended) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            (recommended['segment'], recommended['viewed_before'], recommended['previously_recommended'])
        )
    psql_conn.commit()
    print("inserted!!")


insert_data(get_recommendation_data())
