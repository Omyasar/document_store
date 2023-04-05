from db_conn import db_connection

psql_conn, psql_cursor = db_connection()


# nog niet af
def has_sale_id_query(profileid):
    psql_cursor.execute(f"select preferences from session where fk_profile_id = '{profileid}' AND has_sale = TRUE")
    result = psql_cursor.fetchall()
    has_sale_categorie = result
    return has_sale_categorie


# query kenmerken data
def product_id_has_sale_ids(category_name):
    psql_cursor.execute(f"SELECT product_id FROM products WHERE categorie = '{category_name}'")
    result = psql_cursor.fetchall()
    product_ids = result
    return product_ids


def get_most_expensive_product_id(product_ids):
    psql_cursor.execute(
        f"SELECT product_id FROM products WHERE product_id IN {product_ids} AND price = (SELECT MAX(price) FROM products WHERE product_id IN {product_ids})")
    result = psql_cursor.fetchone()
    return result[0] if result else None


product_id_has_sale_ids(kenmerken_list=has_sale_id_query)
print(get_most_expensive_product_id(product_id_has_sale_ids))
