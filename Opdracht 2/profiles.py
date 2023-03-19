from pymongo import MongoClient
import psycopg2

# mongodb connectie
client = MongoClient()
db = client["huwebshop"]
profiles_collection = db["profiles"]

# pgadmin connectie
psql_conn = psycopg2.connect(
    host="localhost",
    database="huwebshop",
    user="postgres",
    password="1234",
    port=5432)

psql_cursor = psql_conn.cursor()


# get profile data
def get_profile_data():
    profile_list = []
    for doc in profiles_collection.find():
        try:
            profile_id = str(doc['_id'])
            count = doc['order']['count']
        except KeyError:
            continue  # skip if 'order' key not found
        buid_list = doc['buids']
        profile_dict = {'_id': profile_id, 'count': count, 'buids': buid_list}
        profile_list.append(profile_dict)
    return profile_list


get_profile_data()


# insert into database
def insert_profile_data(profiles):
    for profile in profiles:
        psql_cursor.execute(
            "INSERT INTO profile (profile_id, buids, count) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            (profile['_id'], profile['buids'], profile['count'])
        )
    psql_conn.commit()
    print("inserted!!")


insert_profile_data(get_profile_data())
