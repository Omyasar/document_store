from pymongo import MongoClient
from db_conn import db_connection

# mongodb connectie
client = MongoClient()
db = client["huwebshop"]
profiles_collection = db["profiles"]

psql_conn, psql_cursor = db_connection()


# get profile data
def get_profile_data():
    profile_list = []
    for doc in profiles_collection.find().limit(10000):
        profile_id = str(doc['_id'])
        profile_list.append(doc)
    return profile_list


# insert into database
def insert_profile_data(profiles):
    for profile in profiles:
        if "recommendations" not in profile or "buids" not in profile or "order" not in profile:
            continue
        print(profile)
        psql_cursor.execute(
            "INSERT INTO profile (profile_id, buids, count, previously_recommended, viewed_before, similars) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (str(profile['_id']),
                ';'.join(profile.get('buids', [])),
             profile.get('order', {}).get('count', 0),
             ','.join(profile.get('previously_recommended', [])),
             ','.join(profile.get('recommendations', {}).get('viewed_before', [])),
             ','.join(profile.get('recommendations', {}).get('similars', [])))
        )
    psql_conn.commit()
    print("inserted!!")


if __name__ == '__main__':
    get_profile_data()
    insert_profile_data(get_profile_data())