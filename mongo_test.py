from pymongo import MongoClient

CLIENT = MongoClient()

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


















