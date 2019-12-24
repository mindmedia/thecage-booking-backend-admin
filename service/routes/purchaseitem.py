from service.models import PurchaseLog, PurchaseItem, purchase_log_schema, purchase_logs_schema, purchase_log2_schema, purchase_log2s_schema, purchase_item_schema, purchase_items_schema
from flask import request, jsonify
from service import app
from datetime import datetime
from service import db


# Create a PurchaseItem
@app.route("/purchaseitem", methods=["POST"])
def add_purchaseitem():
    purchase_log_id = request.json["purchaseLogId"]
    product_id = request.json["productId"]
    field_id = request.json["fieldId"]
    pitch_id = request.json["pitchId"]
    price = request.json["price"]
    start_time = request.json["startTime"]
    end_time = request.json["endTime"]
    new_purchase_item = PurchaseItem(purchase_log_id, product_id, field_id, pitch_id, price, start_time, end_time)

    db.session.add(new_purchase_item)
    db.session.commit()

    return purchase_log_schema.jsonify(new_purchase_item)


# Update a PurchaseItem
@app.route("/purchaseitem/<Id>", methods=["PUT"])
def update_purchaseitem(Id):
    purchase_item = PurchaseItem.query.get(Id)

    purchase_item.purchase_log_id = request.json["purchaseLogId"]
    purchase_item.product_id = request.json["productId"]
    purchase_item.field_id = request.json["fieldId"]
    purchase_item.pitch_id = request.json["pitchId"]
    purchase_item.price = request.json["price"]
    purchase_item.start_time = request.json["startTime"]
    purchase_item.end_time = request.json["endTime"]

    db.session.commit()

    return purchase_log_schema.jsonify(purchase_item)
