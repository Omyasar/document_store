from db_conn import db_connection

psql_conn, psql_cursor = db_connection()

def similar_products_id_query(category_p):
    psql_cursor.execute(f"select price from products where categorie = '{category_p}'")
    result = psql_cursor.fetchall()
    similar_category = [float(x[0]) for x in result]
    average_similar = sum(similar_category) / len(similar_category)
    return average_similar


def get_product_ids_above_avg_price(category_p):
    avg_price = similar_products_id_query(category_p)
    psql_cursor.execute(f"SELECT product_id FROM products WHERE categorie='{category_p}' AND price > {avg_price} LIMIT 4")
    result = psql_cursor.fetchall()
    products_above_avg = [x[0] for x in result]
    return products_above_avg


category_name = 'Make-up & geuren'
similar_products_id_query(category_name)
print(get_product_ids_above_avg_price(category_name))
