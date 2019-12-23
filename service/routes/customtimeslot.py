from flask import request, jsonify
from service import app
from service.models import CustomTimeSlot, customtimeslot_schema, Field, customtimeslots_schema
from datetime import datetime
from service import db

# Create customtimeslot
@app.route('/customtimeslot/<Id>', methods=["POST"])
def add_customtimeslot(Id):
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

    return customtimeslot_schema.jsonify(new_customtimeslot)


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
    customtimeslot = CustomTimeSlot.query.get(Id)

    db.session.delete(customtimeslot)
    db.session.commit()

    return customtimeslot_schema.jsonify(customtimeslot)
