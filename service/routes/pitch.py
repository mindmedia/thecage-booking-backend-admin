from flask import request, jsonify
from service import app
from service.models import Field, Pitch, pitch_schema, pitches_schema
import json
from service import db
import jwt

# Create new pitch
@app.route("/pitch/<Id>", methods=['POST'])
def add_pitch(Id):

    field = Field.query.get(Id)
    field_id = field.id
    name = request.json["name"]
    odoo_id = request.json["odooId"]
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        new_pitch = Pitch(name, field_id, odoo_id)
        field.num_pitches += 1
        db.session.add(new_pitch)
        db.session.commit()

        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400
# Get lists of Pitch
@app.route("/pitches", methods=["GET"])
def get_pitches():
    all_pitches = Pitch.query.all()
    result = pitches_schema.dump(all_pitches)
    return jsonify(result)

# Get pitch based on Id
@app.route("/pitch/<Id>", methods=["GET"])
def get_pitch_based_on_id(Id):
    pitch = Pitch.query.get(Id)
    return pitch_schema.jsonify(pitch)


# Update a Pitch
@app.route("/pitch/<Id>", methods=['PUT'])
def update_pitch(Id):
    pitch = Pitch.query.get(Id)

    name = request.json["name"]
    odoo_id = request.json["odooId"]
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        pitch.name = name
        pitch.odoo_id = odoo_id

        db.session.commit()

        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400

# Delete Pitch
@app.route("/pitch/<Id>", methods=["DELETE"])
def delete_pitch(Id):
    pitch = Pitch.query.get(Id)
    id = pitch.field_id

    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        field = Field.query.get(id)
        field.num_pitches -= 1
        db.session.delete(pitch)
        db.session.commit()

        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400