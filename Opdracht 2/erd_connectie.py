import pymongo
from pymongo import MongoClient
import psycopg2
import random

# Globale variabele voor mongodb
CLIENT = MongoClient()
mongo_db = CLIENT["huwebshop"]
product_collection = mongo_db["products"]

# Postgres connectie maken
psql_conn = psycopg2.connect(
    host="localhost",
    database="document_store",
    user="postgres",
    password="farmainterim",
    port=5433)

psql_cursor = psql_conn.cursor()
test_products = []
category_products = []
prices_for_category = []


# test = [{'selling_price': 1},{'selling_price': 2},{'selling_price': 3}]


# Postgres database vullen met de naam van het product en prijs van het product.
def all_product_info():
    for doc in product_collection.find():
        try:
            product_name = doc['name']
            product_price = doc['price']['selling_price']
            product_category = doc['category']
            product_gender = doc['gender']
        except KeyError:
            continue
        test_products.append({'name': product_name, 'selling_price': product_price, 'category': product_category,
                              'gender': product_gender})
        psql_cursor.execute(
            "INSERT INTO products VALUES (%s, %s, %s, %s)",
            (product_name, product_price, product_category, product_gender)
        )
        psql_conn.commit()
    print('Database succesvol gevuld. :)')


all_product_info()


def category_pakker():
    for doc in product_collection.find():
        try:
            product_category = doc['category']
            category_products.append(product_category)
        except KeyError:
            continue


category_pakker()

categories = [c for c in category_products if c is not None]

random_category = random.choice(categories)


def price_category():
    psql_cursor.execute("SELECT product_price FROM products WHERE product_category = %s", (random_category,))
    result = psql_cursor.fetchall()
    for row in result:
        prices_for_category.append(row[0])
    return prices_for_category

price_category()
print(prices_for_category)

# Call de functie
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
print("Geselecteerd product:", selected_product['name'])
print("Product met grootste afwijking:", max_diff_product['name'])
print('==' * 65)


# Gemiddelde prijs van alle producten
def average_price(products):
    prijzen = [p['selling_price'] for p in products if 'selling_price' in p.keys()]
    return sum(prijzen) / len(products)


print("De gemiddelde prijs van onze producten zijn:", average_price(products=test_products))
print("==" * 65)

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
