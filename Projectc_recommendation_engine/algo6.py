from db_conn import db_connection

psql_conn, psql_cursor = db_connection()

def previously_recommended_id_query(profileid):
    psql_cursor.execute(f"select previously_recommended from profile where profile_id = '{profileid}'")
    result = psql_cursor.fetchall()
    previously_recommended = [int(id) for id in result[0][0].strip('{}').split(',')]
    return previously_recommended

# query kenmerken data
def kenmerken_product_ids(kenmerken_list):
    psql_cursor.execute(f"SELECT soort, gender FROM products WHERE product_id IN ({','.join([str(f) for f in kenmerken_list])})")
    result = psql_cursor.fetchall()
    soort_value = []
    gender_value = []

    for row in result:
        if row[0] is None or row[1] is None:
            continue
        soort_value.append(row[0])
        gender_value.append(row[1])
    return soort_value, gender_value


def soort_gender_query(gender_value, soort_value):
    psql_cursor.execute(
        "select product_id from products where soort = %s AND gender = %s ORDER BY BRAND ASC limit 4",
        (soort_value, gender_value))
    result = psql_cursor.fetchall()
    soort_gender_list = []
    for row in result:
        soort_gender_list.append(str(row[0]))
    return soort_gender_list