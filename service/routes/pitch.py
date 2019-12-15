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
    new_pitch = Pitch(name, field_id)
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


# Get Pitch based on Field ID
@app.route("/pitch/<field_id>", methods=["GET"])
def get_pitch_based_on_field_id(field_id):
    all_pitches = Pitch.query.filter_by(field_id=field_id).all()
    result = pitches_schema.dump(all_pitches)
    return pitches_schema.jsonify(result)

# Get pitch based on field id and pitch id
@app.route("/pitch/<field_id>/<id>", methods=["GET"])
def get_pitch_based_on_id(field_id, id):
    all_pitches = Pitch.query.filter_by(field_id=field_id, id=id).all()
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
@app.route("/pitch/<field_id>/<pitch_id>", methods=["DELETE"])
def delete_pitch(field_id, pitch_id):
    field = Field.query.get(field_id)
    pitch = Pitch.query.get(pitch_id)

    # field_with_pitch = Field.query(Field.id == pitch.field_id).all()\
    field.num_pitches -= 1
    db.session.delete(pitch)
    db.session.commit()

    return pitch_schema.jsonify(pitch)
