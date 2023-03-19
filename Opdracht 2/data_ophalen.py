import psycopg2

# pgadmin connectie
psql_conn = psycopg2.connect(
    host="localhost",
    database="huwebshop",
    user="postgres",
    password="1234",
    port=5432)

psql_cursor = psql_conn.cursor()


# dit zijn test queries om te laten zien dat er eenvouding en effectief gezocht kan worden  zoals aangegeven bij punt 4 in de rubriek
# Een effectieve relationele database opzetten en bijbehorende functies in de gekozen programmeertaal te realiseren.


def nagellak_names_id_query():
    psql_cursor.execute("SELECT name, product_id FROM products WHERE sub_sub_category = 'Tandpasta'")
    result = psql_cursor.fetchall()
    nagellak_names = []
    for row in result:
        data = {
            "name": row[0],
            "product_id": row[1]
        }
        nagellak_names.append(data)
    return nagellak_names


print(nagellak_names_id_query())


def category_name_id_query():
    psql_cursor.execute("SELECT nme, product_id FROM products WHERE categorie = 'Gezond & verzorging' ")
    result = psql_cursor.fetchall()
    all_categorie_data = []
    for row in result:
        data = {
            "name": row[0],
            "product_id": row[1]
        }
        all_categorie_data.append(data)
    return all_categorie_data


print(category_name_id_query())


def all_profile_date_query():
    psql_cursor.execute("SELECT profiel_id, buids, count FROM profile")
    result = psql_cursor.fetchall()
    print(result)
    all_profiel_data = []
    for row in result:
        data = {
            "profiel_id": row[0],
            "buids": row[1],
            "count": row[2]
        }
        all_profiel_data.append(data)
    return all_profiel_data


print(all_profile_date_query())
