from pymongo import MongoClient
import psycopg2

client = MongoClient()
print(client) #mongoclient
print(client.sp_db)
print(client.sp_db.products.find_one()) #eerste product


