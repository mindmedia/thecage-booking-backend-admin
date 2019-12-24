from service.models import PurchaseLog, PurchaseItem, purchase_log_schema, purchase_logs_schema, purchase_log2_schema, purchase_log2s_schema, purchase_item_schema, purchase_items_schema
from flask import request, jsonify
from service import app
from datetime import datetime
from service import db


# Create a PurchaseLog
@app.route("/purchaselog", methods=["POST"])
def add_purchaselog():
    customer_id = request.json["customerId"]
    timestamp = datetime.now()
    new_purchase_log = PurchaseLog(customer_id, timestamp)

    db.session.add(new_purchase_log)
    db.session.commit()

    return purchase_log_schema.jsonify(new_purchase_log)


# Get all PurchaseLog, ordered by create date
@app.route("/purchaselogs", methods=["GET"])
def get_purchaselog_by_id():
    purchase_log = PurchaseLog.query.order_by(PurchaseLog.timestamp.desc()).all()
    results = purchase_log2s_schema.dump(purchase_log)
    return jsonify(results)
