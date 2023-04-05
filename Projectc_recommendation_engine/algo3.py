from db_conn import db_connection
import random

psql_conn, psql_cursor = db_connection()

def viewed_before_id_query(profileid):
    psql_cursor.execute(f"select viewed_before from profile where profile_id = '{profileid}'")
    result = psql_cursor.fetchall()
    previously_recommended = [int(id) for id in result[0][0].strip('{}').split(',')]
    random_viewed_before = random.choice(previously_recommended)
    return random_viewed_before

def brand_name(product_id):
    psql_cursor.execute(
        f"SELECT brand FROM products WHERE product_id = '{product_id}'")
    result = psql_cursor.fetchone()[0]
    return result

def brand_product_ids(brand_name):
    psql_cursor.execute(
        f"SELECT product_id FROM products WHERE brand = '{brand_name}'limit 4")
    result = psql_cursor.fetchall()
    return result

profile_id = '5a393d68ed295900010384ca'
viewed_before_id = viewed_before_id_query(profile_id)
result = brand_name(viewed_before_id)
brand_ids = brand_product_ids(result)
print(brand_ids)