from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import psycopg2
import random
from db_conn import db_connection

psql_conn, psql_cursor = db_connection()

app = Flask(__name__)
api = Api(app)

# We define these variables to (optionally) connect to an external MongoDB
# instance.
envvals = ["MONGODBUSER", "MONGODBPASSWORD", "MONGODBSERVER"]
dbstring = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'

# Since we are asked to pass a class rather than an instance of the class to the
# add_resource method, we open the connection to the database outside of the 
# Recom class.
load_dotenv()
# if os.getenv(envvals[0]) is not None:
# envvals = list(map(lambda x: str(os.getenv(x)), envvals))
# client = MongoClient(dbstring.format(*envvals))
# else:
client = MongoClient()
database = client.huwebshop


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


class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""

    def get(self, profileid, count):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products. """
        soort_values, gender_values = kenmerken_product_ids(kenmerken_list=previously_recommended_id_query(profileid))

        categorie_doelgroep_ids = []

        while len(categorie_doelgroep_ids) < count:
            soort_value = (random.choice(soort_values))
            gender_value = (random.choice(gender_values))
            categorie_doelgroep_ids = soort_gender_query(gender_value, soort_value)

        randcursor = database.products.aggregate([{'$sample': {'size': count}}])
        prodids = list(map(lambda x: x['_id'], list(randcursor)))
        return categorie_doelgroep_ids, 200



# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>")