from pymongo import MongoClient
import psycopg2
import re

client = MongoClient()
db = client["huwebshop"]
order_collection = db["sessions"]

psql_conn = psycopg2.connect(
    host="localhost",
    database="huwebshop",
    user="postgres",
    password="1234",
    port=5432)

psql_cursor = psql_conn.cursor()


# get event data
def get_order_data():
    test_order = []
    counter = 0  # counter

    for doc in order_collection.find():
        if counter >= 10:  # Stop loop 10 items
            break

        try:
            order_list = doc['order']['products']

            for order in order_list:
                order_id = order['id']

                test_order.append(
                    {'order_id': order_id})

                counter += 1  # add the counter

                if counter >= 10:  # break loop 10 items
                    break

        except KeyError:
            continue

    return test_order


get_order_data()


# insert into database
def insert_data(orders):
    for order in orders:
        psql_cursor.execute(
            "INSERT INTO orders (order_id) VALUES (%s) ON CONFLICT DO NOTHING",
            (order['order_id'])
        )
    psql_conn.commit()
    print("inserted!!")


insert_data(get_order_data())
