import pymongo
from pymongo import MongoClient
import psycopg2

CLIENT = MongoClient()
mongo_db = CLIENT["sp_db"]
product_collection = mongo_db["products"]

psql_conn = psycopg2.connect(
    host="localhost",
    database="document_store",
    user="postgres",
    password="farmainterim",
    port = 5433 )

psql_cursor = psql_conn.cursor()

for doc in product_collection.find():
    product_name = doc['category']['category_1']
    product_price = doc['price']['selling_price']
    psql_cursor.execute(
        "INSERT INTO products VALUES (%s, %s)", (product_name, product_price)
    )
    psql_conn.commit()

# List comprehension
producten = [product for product in CLIENT.sp_db.products.find()]

# Eerste product & prijs

query_eerstep = ({'name':'Korg RP-G1 Rimpitch tuner voor klankgat gitaar'})
eerste_product = CLIENT.sp_db.products.find_one()
eerste_prijs = eerste_product['price']

print('het eerste product naam uit de database is;', eerste_product['name'])
print('Het prijs van dit product is $', eerste_prijs['selling_price'])
print('=='*65)

# Eerste product met letter R in de naam
query_r = ({"name": {"$regex":"^R"}})
product = CLIENT.sp_db.products.find_one(query_r)
print('Eerste product met letter R in het begin van de naam;', product['name'])
print('=='* 65)

# Gemiddelde prijs van alle producten
totale = []
for prijs in producten:
    totale.append(prijs['price']['selling_price'])

print("De gemiddelde prijs van onze producten zijn:",sum(totale)/len(totale))
print("=="*65)


















