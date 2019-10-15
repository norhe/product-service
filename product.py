from flask import Flask
from flask import jsonify
from pymongo import MongoClient

import os
import socket
_hostname = socket.gethostname()

DB_ADDR = 'DB_ADDR'
DB_PORT = 'DB_PORT'
DB_USER = 'DB_USER'
DB_PW = 'DB_PW'

DB_NAME = 'bbthe90s'
COL_NAME = 'products'

PRODUCT_PORT = 'PRODUCT_PORT'

def connect_to_db():
    db_addr = os.getenv(DB_ADDR, "127.0.0.1")
    db_port = int(os.getenv(DB_PORT, "5001"))
    db_username = os.getenv(DB_USER)
    db_pw = os.getenv(DB_PW)

    if not db_addr or not db_port:
        # try default connection settings
        client = MongoClient()
    else:
        client = MongoClient(db_addr, db_port)
    return client

db_client = connect_to_db()

app = Flask(__name__)

# these can be seeded into the DB for testing if necessary
prods = [{ 'inv_id': 1, 'name':'jncos', 'cost':35.57, 'img':None},
         { 'inv_id': 2, 'name':'denim vest', 'cost':22.50, 'img':None},
         { 'inv_id': 3, 'name':'pooka shell necklace', 'cost':12.37, 'img':None},
         { 'inv_id': 4, 'name':'shiny shirt', 'cost':17.95, 'img':None}]

@app.route("/product", methods=['GET'])
def get_products():
    res = get_products_from_db()
    res.insert(0, {'request_handled_by_host': _hostname })
    return jsonify(res)

@app.route("/product/healthz", methods=['GET'])
def get_health():
    return "OK"

def get_products_from_db():
    return [rec for rec in db_client[DB_NAME][COL_NAME].find({}, {'_id': False})]

if __name__ == '__main__':
    PORT = os.environ.get(PRODUCT_PORT)
    app.run(host='127.0.0.1', port=PORT)
