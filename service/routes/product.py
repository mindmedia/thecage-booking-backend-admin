from flask import request, jsonify
from service.models import Product, products_schema, product_schema, ProductValidDay
from service import app
from service import db
from sqlalchemy import exc
import json
import jwt
import xmlrpc.client
from instance.config import url, db_odoo as database, username, password


# get products and venues
@app.route("/products", methods=['GET'])
def get_products():
    product = Product.query.all()
    result = products_schema.dump(product)
    return jsonify(result)

# get product based on id
@app.route("/product/<Id>", methods=['GET'])
def get_products_by_id(Id):
    product = Product.query.get(Id)
    return product_schema.jsonify(product)


# create product
@app.route("/product", methods=['POST'])
def add_product():
    name = request.json["name"]
    price = request.json["price"]
    odoo_id = request.json["odooId"]
    start_time = request.json["startTime"]
    end_time = request.json["endTime"]
    tokenstr = request.headers["Authorization"]
    valid_days = request.json["validDay"]
    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        try:
            common = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/common")
            uid = common.authenticate(database, username, password, {})
            models = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/object")
            odoo_counterpart = models.execute_kw(
                database,
                uid,
                password,
                "product.template",
                "search",
                [
                    [['id', '=', odoo_id]]
                ],
            )
            if (odoo_counterpart == []):
                return json.dumps({'message': "ID '" + str(odoo_id) + "' does not exist in Odoo"}), 400, {'ContentType': 'application/json'}
            else:
                new_product = Product(name, price, odoo_id, start_time, end_time)

                db.session.add(new_product)
                db.session.commit()
        except exc.IntegrityError:
            return json.dumps({'message': "Name '" + name + "' already exists"}), 400, {'ContentType': 'application/json'}
        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})    
    else:
        return "You are not authorised to perform this action", 400
    return product_schema.jsonify(new_product)

# update product
@app.route("/product/<Id>", methods=['PUT'])
def update_product(Id):
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        try:
            product = Product.query.get(Id)

            name = request.json["name"]
            price = request.json["price"]
            odoo_id = request.json["odooId"]
            start_time = request.json["startTime"]
            end_time = request.json["endTime"]

            common = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/common")
            uid = common.authenticate(database, username, password, {})
            models = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/object")
            odoo_counterpart = models.execute_kw(
                database,
                uid,
                password,
                "product.template",
                "search",
                [
                    [['id', '=', odoo_id]]
                ],
            )
            if (odoo_counterpart == []):
                return json.dumps({'message': "ID '" + str(odoo_id) + "' does not exist in Odoo"}), 400, {'ContentType': 'application/json'}
            else:
                product.name = name
                product.price = price
                product.odoo_id = odoo_id
                product.start_time = start_time
                product.end_time = end_time

            # db.session.commit()
        except exc.IntegrityError:
            return json.dumps({'message': "Name '" + name + "' already exists"}), 400, {'ContentType': 'application/json'}
        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400

# delete product
@app.route("/product/<Id>", methods=["DELETE"])
def delete_product(Id):
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        product = Product.query.get(Id)
        db.session.delete(product)
        db.session.commit()
        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400
