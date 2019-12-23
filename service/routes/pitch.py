from flask import request, jsonify
from service import app
from service.models import Field, Pitch, pitch_schema, pitches_schema
# from datetime import datetime
from service import db

# Create new pitch
@app.route("/pitch/<Id>", methods=['POST'])
def add_pitch(Id):
    field = Field.query.get(Id)
    field_id = field.id
    name = request.json["name"]
    odoo_id = request.json["odooId"]
    new_pitch = Pitch(name, field_id, odoo_id)
    field.num_pitches += 1
    db.session.add(new_pitch)
    db.session.commit()

    return pitch_schema.jsonify(new_pitch)


# Get lists of Pitch
@app.route("/pitch", methods=["GET"])
def get_pitches():
    all_pitches = Pitch.query.all()
    result = pitches_schema.dump(all_pitches)
    return jsonify(result)

# Get pitch based on Id
@app.route("/pitch/<Id>", methods=["GET"])
def get_pitch_based_on_id(Id):
    pitch = Pitch.query.get(Id)
    return pitch_schema.jsonify(pitch)

# Get Pitch based on field ID
@app.route("/pitches/<field_id>", methods=["GET"])
def get_pitch_based_on_field_id(field_id):
    all_pitches = Pitch.query.filter_by(field_id=field_id).all()
    result = pitches_schema.dump(all_pitches)
    return pitches_schema.jsonify(result)


# Update a Pitch
@app.route("/pitch/<Id>", methods=['PUT'])
def update_pitch(Id):
    pitch = Pitch.query.get(Id)

    name = request.json["name"]

    pitch.name = name

    db.session.commit()

    return pitch_schema.jsonify(pitch)

# Delete Pitch
@app.route("/pitch/<Id>", methods=["DELETE"])
def delete_pitch(Id):
    pitch = Pitch.query.get(Id)
    id = pitch.field_id
    field = Field.query.get(id)
    field.num_pitches -= 1
    db.session.delete(pitch)
    db.session.commit()

    return pitch_schema.jsonify(pitch)
