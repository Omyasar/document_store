import random
from db import db_connection

psql_cursor = db_connection()

'''
bijvoorbeeld als er een item in de cart pak ik het id van het product bekijk ik de kenmerken(dit haal ik dan op en zet ik in variables)
zodat ik die kan gebruiken voor een query search in dit geval vul ik het alvast in met navulmesjes en doelgroep vrouwen
dus soort =  en doelgroep = . kan ik vervangen met een variable naam en zo de search doen 
'''


# alle ids met soort navulmesjes en doelgroep vrouwen
def navulmesjes_id_query():
    psql_cursor.execute("select product_id from products where soort = 'Navulmesjes' and doelgroep = 'Vrouwen'")
    result = psql_cursor.fetchall()
    navulmesjes_list = []
    for row in result:
        navulmesjes_list.append(row)
    return navulmesjes_list


navulmesjes_id_query()

# random aanbevolen producten met gekozen kenmerken op basis van product id
random_products = random.sample(navulmesjes_id_query(), 4)


print(random_products)


# als je de profiel_id 5a393d68ed295900010384ca gebruikt en de viewed_before items bekijkt krijg je deze ids
# {45281,20371,39793} dit zijn shampoos en conditioners dus haarverzorging producten hierop search ik naar haarverzorging
# met de hoogste prijs in die categorie

# query voor viewed before items recommendations_id = '1' is eigelijk de profiel_id 5a393d68ed295900010384ca
# door een klein foutje in de database moet het even op deze manier

def viewed_before_id_query():
    psql_cursor.execute("select viewed_before from recommendations where recommendations_id = '1'")
    result = psql_cursor.fetchall()
    viewed_before = []
    for row in result:
        viewed_before.append(row)
    return viewed_before


test_id_list = [45281, 20371, 39793]


# query kenmerken data
def kenmerken_product_ids(kenmerken_list):
    psql_cursor.execute("SELECT sub_category, price, name, soort FROM products WHERE product_id IN ({})".format(
        ",".join(str(int(id)) for id in kenmerken_list)))
    result = psql_cursor.fetchall()
    kenmerken = []
    for row in result:
        kenmerken.append(row)
    return kenmerken


# hier pak ik list test_id_list dit is voor het testen zodat ik in de functie de kenmerken kan ophalen
# NOTE de daadwerkelijk lijst komt van viewed_before_id_query je kan elke lijst met product IDS gebruiken
print(kenmerken_product_ids(kenmerken_list=test_id_list))


# query aanbeveling top 4 duurste haarverzorging producten
#
def haarverzorging_id_query():
    psql_cursor.execute(
        "select product_id from products where sub_category = 'Haarverzorging' ORDER BY price DESC limit 4")
    result = psql_cursor.fetchall()
    haarverzorging = []
    for row in result:
        haarverzorging.append(row)
    return haarverzorging


# 4 duurste ids dit zijn de aanbevelingen
haarverzorging_id_query()
