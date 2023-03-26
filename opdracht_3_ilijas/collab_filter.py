import random
from db import db_connection

psql_conn, psql_cursor = db_connection()


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


viewed_before_id_query()

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
kenmerken_product_ids(kenmerken_list=test_id_list)


# de kenmerken function gaf terug haarverzorging producten dus die gaan we aanbevelen
# query aanbeveling top 4 duurste haarverzorging producten
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


# clear records + insert aanbevolen producten in database
def insert_collab(haarverzorging_ids):
    psql_cursor.execute("delete from recommended_collab_products")
    for id_tuple in haarverzorging_ids:
        psql_cursor.execute("INSERT INTO recommended_collab_products (product_id) VALUES (%s)", id_tuple)
    psql_conn.commit()


haarverzorging_ids = haarverzorging_id_query()
print(haarverzorging_ids)
insert_collab(haarverzorging_ids)
