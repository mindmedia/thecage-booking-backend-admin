from flask import request, jsonify
from service import app
from service.models import CustomTimeSlot, customtimeslot_schema, Field, customtimeslots_schema
from datetime import datetime
import json
from service import db
import jwt

# Create customtimeslot
@app.route('/customtimeslot/<Id>', methods=["POST"])
def add_customtimeslot(Id):
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        field = Field.query.get(Id)
        field_id = field.id
        start_time = request.json["startTime"]
        duration = request.json["duration"]
        end_time = request.json["endTime"]
        created_at = datetime.now()
        updated_at = datetime.now()
        new_customtimeslot = CustomTimeSlot(start_time, end_time, field_id, duration, created_at, updated_at)

        db.session.add(new_customtimeslot)
        db.session.commit()

        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400

# Get customtimeslot based on Id
@app.route("/customtimeslot/<Id>", methods=["GET"])
def get_customtimeslot_based_on_id(Id):
    customtimeslot = CustomTimeSlot.query.get(Id)

    return customtimeslot_schema.jsonify(customtimeslot)


# Get list of customtimeslots based on field id
@app.route("/customtimeslots/<field_id>", methods=["GET"])
def get_customtimeslot(field_id):
    all_customtimeslot = CustomTimeSlot.query.filter_by(field_id=field_id).all()
    result = customtimeslots_schema.dump(all_customtimeslot)
    return jsonify(result)

# Delete Custom Timeslot
@app.route("/customtimeslot/<Id>", methods=["DELETE"])
def delete_customtimeslot(Id):
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        customtimeslot = CustomTimeSlot.query.get(Id)

        db.session.delete(customtimeslot)
        db.session.commit()

        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400