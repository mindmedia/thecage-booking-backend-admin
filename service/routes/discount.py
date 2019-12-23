from flask import request, jsonify
from service import app
from service.models import TimingDiscount, timingdiscount_schema, timingdiscounts_schema
from service import db

# Create new Timing Discount
@app.route("/discount", methods=['POST'])
def add_discount():
    start_time = request.json["startTime"]
    end_time = request.json["endTime"]
    discount_type = request.json["discountType"]
    discount = request.json["discount"]
    status = request.json["status"]
    new_timing_discount = TimingDiscount(start_time, end_time, discount_type, discount, status)

    db.session.add(new_timing_discount)
    db.session.commit()
    return timingdiscount_schema.jsonify(new_timing_discount)

# Edit timing discount
@app.route("/discount/<Id>", methods=['PUT'])
def update_discount(Id):
    timingdiscount = TimingDiscount.query.get(Id)
    start_time = request.json["startTime"]
    end_time = request.json["endTime"]
    discount_type = request.json["discountType"]
    discount = request.json["discount"]
    status = request.json["status"]

    timingdiscount.start_time = start_time
    timingdiscount.end_time = end_time
    timingdiscount.discount_type = discount_type
    timingdiscount.discount = discount
    timingdiscount.status = status
    db.session.commit()

    return timingdiscount_schema.jsonify(timingdiscount)


# Get timing discount
@app.route("/discount", methods=["GET"])
def get_discounts():
    all_timingdiscounts = TimingDiscount.query.all()
    result = timingdiscounts_schema.dump(all_timingdiscounts)
    return jsonify(result)

# Get timing discoutn based on id
@app.route("/discount/<Id>", methods=["GET"])
def get_discount_based_on_id(Id):
    timingdiscount = TimingDiscount.query.get(Id)
    return timingdiscount_schema.jsonify(timingdiscount)
