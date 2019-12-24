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

# create product
@app.route("/product", methods=['POST'])
def add_product():
    name = request.json["name"]
    price = request.json["price"]
    odoo_id = request.json["odooId"]

    new_product = Product(name, price, odoo_id)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)
