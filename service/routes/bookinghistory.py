from service.models import (
    PurchaseLog,
    PurchaseItem,
    purchase_log_schema,
    purchase_logs_schema,
    purchase_log2_schema,
    purchase_log2s_schema,
    purchase_item_schema,
    purchase_items_schema,
)
from flask import request, jsonify
from service import app
from datetime import datetime
from service import db


@app.route("/bookinghistory/<Id>", methods=["GET"])
def get_bookinghistory(Id):
    purchase_log_ids = []
    return_dict = {"logs": [], "items": []}

    purchase_log = (
        PurchaseLog.query.order_by(PurchaseLog.timestamp.desc())
        .filter_by(customer_id=Id)
        .all()
    )
    results_purchase_log = purchase_log2s_schema.dump(purchase_log)
    for result in purchase_log:
        purchase_log_ids.append(result.id)

    for log in results_purchase_log:
        return_dict["logs"].append(log)

    for log_id in purchase_log_ids:
        purchase_item = (
            PurchaseItem.query.order_by(PurchaseItem.id.desc())
            .filter_by(purchase_log_id=log_id)
            .all()
        )
        results_purchase_item = purchase_items_schema.dump(purchase_item)
        for i in results_purchase_item:
            return_dict["items"].append(i)

    return jsonify(return_dict)
