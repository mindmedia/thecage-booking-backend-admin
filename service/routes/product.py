from flask import request, jsonify
from service.models import Product, products_schema, product_schema
from service import app
from service import db

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

    new_product = Product(name, price, odoo_id, start_time, end_time)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)
