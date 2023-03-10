import pymongo
from pymongo import MongoClient
import psycopg2
import random

CLIENT = MongoClient()
mongo_db = CLIENT["huwebshop"]
product_collection = mongo_db["products"]

psql_conn = psycopg2.connect(
    host="localhost",
    database="document_store",
    user="postgres",
    password="farmainterim",
    port=5433)

psql_cursor = psql_conn.cursor()
test_products = []


def all_product_info():
    for doc in product_collection.find():
        try:
            product_name = doc['name']
            product_price = doc['price']['selling_price']
        except KeyError:
            continue
        test_products.append({'name': product_name, 'selling_price': product_price})
        psql_cursor.execute(
            "INSERT INTO products VALUES (%s, %s)", (product_name, product_price)
        )
        psql_conn.commit()
    print('Database succesvol gevuld. :)')


all_product_info()
print('==' * 65)


def fetched_products(products):
    random_product = random.choice(products)

    # Zoek het product met de grootste absolute afwijking in prijs ten opzichte van het geselecteerde product
    max_diff = 0
    max_diff_product = None
    for product in products:
        if product != random_product:
            diff = abs(product["selling_price"] - random_product["selling_price"])
            if diff > max_diff:
                max_diff = diff
                max_diff_product = product

    # Geef het geselecteerde product en het product met de grootste absolute afwijking terug
    return random_product, max_diff_product


selected_product, max_diff_product = fetched_products(test_products)
print("Geselecteerd product:", selected_product)
print("Product met grootste afwijking:", max_diff_product)

print('==' * 65)
# List comprehension
producten = [product for product in CLIENT.huwebshop.products.find()]

# Eerste product & prijs
query_eerstep = ({'name': 'Korg RP-G1 Rimpitch tuner voor klankgat gitaar'})
eerste_product = CLIENT.huwebshop.products.find_one()
eerste_prijs = eerste_product['price']

print('het eerste product naam uit de database is;', eerste_product['name'])
print('Het prijs van dit product is $', eerste_prijs['selling_price'])
print('==' * 65)

# Eerste product met letter R in de naam
query_r = ({"name": {"$regex": "^R"}})
product = CLIENT.huwebshop.products.find_one(query_r)
print('Eerste product met letter R in het begin van de naam;', product['name'])
print('==' * 65)


# Gemiddelde prijs van alle producten
def average_price(products):
    totale = []
    for prijs in products:
        try:
            totale.append(prijs['selling_price'])
        except KeyError:
            continue
    totale = sum(totale) / len(totale)
    return totale


print("De gemiddelde prijs van onze producten zijn:", average_price(products=test_products))
print("==" * 65)
