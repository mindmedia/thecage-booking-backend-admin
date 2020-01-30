from flask import request, jsonify
from service.models import Product, products_schema, product_schema, ProductValidDay
from service import app
from service import db
from sqlalchemy import exc
import json
import jwt

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

        new_product = Product(name, price, odoo_id, start_time, end_time)

        db.session.add(new_product)
        db.session.commit()

        for i in valid_days:
            day_of_week = i
            product_id = new_product.id

            new_valid_day = ProductValidDay(product_id, day_of_week)
            db.session.add(new_valid_day)
            db.session.commit()
            


    else:
        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})

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

            product.name = name
            product.price = price
            product.odoo_id = odoo_id
            product.start_time = start_time
            product.end_time = end_time

            db.session.commit()
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
