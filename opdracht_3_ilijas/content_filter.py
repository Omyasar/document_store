import random
from db import db_connection

# connectie zetten vannuit db file
psql_conn, psql_cursor = db_connection()

'''
bijvoorbeeld als er een item in de cart pak ik het id van het product bekijk ik de kenmerken(dit haal ik dan op en zet ik in variables)
zodat ik die kan gebruiken voor een query search 
'''


# kenmerken ophalen met een id
# line 36 zetten we de id dit is de id die we pakken vannuit de website bvb cart item / categorie / click op item op de website
def kenmerken_product_id(kenmerk):
    psql_cursor.execute("SELECT soort, doelgroep FROM products WHERE product_id = %s",
                        kenmerk)
    result = psql_cursor.fetchall()
    soort_value = []
    doelgroep_value = []
    for row in result:
        soort_value.append(row[0])
        doelgroep_value.append(row[1])
    return soort_value, doelgroep_value


# ids ophalen met de kenmerken van kenmerken_product_id function
def navulmesjes_id_query(soort_value, doelgroep_value):
    psql_cursor.execute("SELECT product_id FROM products WHERE soort = ANY(%s) AND doelgroep = ANY(%s)",
                        (soort_value, doelgroep_value))

    result = psql_cursor.fetchall()
    navulmesjes_list = []
    for row in result:
        navulmesjes_list.append(row)
    return navulmesjes_list


test_id = (31158,)
soort_value, doelgroep_value = kenmerken_product_id(test_id)
navulmesjes_list = navulmesjes_id_query(soort_value, doelgroep_value)
random_products = random.sample(navulmesjes_list, 4)
print(random_products)


# clear records + insert aanbevolen producten in database
def insert_content(content_ids):
    psql_cursor.execute("delete from recommended_content_products")
    for id_content in content_ids:
        psql_cursor.execute("INSERT INTO recommended_content_products (product_id) VALUES (%s)", id_content)
    psql_conn.commit()


insert_content(content_ids=random_products)
