from flask import request, jsonify
from service import app
from service.models import Discount, discount_schema, discounts_schema, TimingDiscount
from service import db

# Create new Discount
@app.route("/discount", methods=['POST'])
def add_discount():
    discount_type = request.json["discount_type"]
    amount = request.json["amount"]
    new_discount = Discount(discount_type, amount)

    db.session.add(new_discount)
    db.session.commit()

    discount_id = new_discount.id
    start_time = request.json["start_time"]
    end_time = request.json["end_time"]
    status = request.json["status"]
    new_timing_discount = TimingDiscount(discount_id, start_time, end_time, status)

    db.session.add(new_timing_discount)
    db.session.commit()
    return discount_schema.jsonify(new_discount)
