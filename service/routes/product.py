from flask import request, jsonify
from service.models import Product, products_schema, product_schema
from service import app
from service import db
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

    else:
        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})

    return product_schema.jsonify(new_product)
