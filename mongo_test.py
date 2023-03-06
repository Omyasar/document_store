from pymongo import MongoClient
import psycopg2

client = MongoClient()
print(client) #mongoclient
print(client.sp_db.products.find())

producten = [product for product in client.sp_db.products.find()]
print(f'er zijn in toaal {len(producten)} producten')

print(f'het eerste product is {(client.sp_db.products.find_one())}')