from pymongo import MongoClient
import psycopg2
import re

client = MongoClient()
db = client["huwebshop"]
product_collection = db["products"]

psql_conn = psycopg2.connect(
    host="localhost",
    database="huwebshop",
    user="postgres",
    password="1234",
    port=5432)

psql_cursor = psql_conn.cursor()

test_products = []


# get all product data
def get_products_data():
    for doc in product_collection.find():
        try:
            product_name = doc['name']
            product_brand = doc['brand']
            product_price = doc['price']['selling_price']
            product_category = doc['category']
            product_gender = doc['gender']
            product_id = doc['_id']
            product_recommendable = doc['recommendable']
            product_sub_category = doc.get('sub_category')
            product_sub_sub_category = doc.get('sub_sub_category')
            product_herhaalaankopen = doc.get('herhaalaankopen')
            product_properties = doc.get('properties')
            if product_properties:
                product_availability = product_properties.get('availability')
                product_doelgroep = product_properties.get('doelgroep')
                product_soort = product_properties.get('soort')
                product_stock = product_properties.get('stock')
            else:
                product_availability = None
                product_doelgroep = None
                product_soort = None
                product_stock = None
        except KeyError:
            continue
        test_products.append(
            {'name': product_name, 'brand': product_brand, 'selling_price': product_price, 'category': product_category,
             'gender': product_gender, '_id': product_id, 'recommendable': product_recommendable,
             'sub_category': product_sub_category,
             'sub_sub_category': product_sub_sub_category, 'herhaalaankopen': product_herhaalaankopen,
             'availability': product_availability, 'doelgroep': product_doelgroep,
             'soort': product_soort, 'stock': product_stock})


get_products_data()


# insert into database
def insert_data(products):
    for product in products:
        # only numeric ids
        product_id = re.sub("[^0-9]", "", product['_id'])
        if not product_id:
            continue
        psql_cursor.execute(
            "INSERT INTO products (name, brand, recommendable, price, categorie, gender, product_id, sub_category, sub_sub_category, herhaalaankopen, availability, doelgroep, soort, stock) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            (product['name'], product['brand'], product['recommendable'], product['selling_price'],
             product['category'], product['gender'], product_id,
             product['sub_category'], product['sub_sub_category'], product['herhaalaankopen'], product['availability'],
             product['doelgroep'], product['soort'], product['stock'])
        )
    psql_conn.commit()

    print("inserted!!")


insert_data(test_products)
