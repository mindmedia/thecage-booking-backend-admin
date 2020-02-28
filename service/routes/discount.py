from flask import request, jsonify
from service import app
from service.models import TimingDiscount, timingdiscount_schema, timingdiscounts_schema
import json
from service import db
import jwt
import datetime

# Create new Timing Discount
@app.route("/discount", methods=['POST'])
def add_discount():
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        start_time = request.json["startTime"]
        end_time = request.json["endTime"]
        discount_type = request.json["discountType"]
        discount = request.json["discount"]
        status = request.json["status"]
        new_timing_discount = TimingDiscount(start_time, end_time, discount_type, discount, status)

        db.session.add(new_timing_discount)
        db.session.commit()
        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400

# Edit timing discount
@app.route("/discount/<Id>", methods=['PUT'])
def update_discount(Id):
    tokenstr = request.headers["Authorization"]
    print(datetime.date.today())
    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        timingdiscount = TimingDiscount.query.get(Id)
        start_time = request.json["startTime"]
        end_time = request.json["endTime"]
        discount_type = request.json["discountType"]
        discount = request.json["discount"]
        status = request.json["status"]
        date = datetime.date.today()

        timingdiscount.end_time = end_time
        timingdiscount.discount_type = discount_type
        timingdiscount.discount = discount
        timingdiscount.status = status
        timingdiscount.date = date
        db.session.commit()

        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400

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
