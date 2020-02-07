from flask import request, jsonify
from service import app
from service.models import Venue, Field, field_schema, fields_schema, fields2_schema, field2_schema, fields3_schema, Pitch, pitches_schema
from datetime import datetime
from sqlalchemy import exc
import json
from service import db
import jwt
import xmlrpc.client
from instance.config import url, db_odoo as database, username, password


# Create new Field
@app.route("/field/<Id>", methods=['POST'])
def add_field(Id):
    tokenstr = request.headers["Authorization"]
    odoo_id = request.json["odooId"]
    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        try:
            if odoo_id=="":
                return (json.dumps({'message': 'Mandatory field \'Odoo ID\' is empty.'}), 400, {'ContentType': 'application/json'})
            common = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/common")
            uid = common.authenticate(database, username, password, {})
            models = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/object")
            odoo_counterpart = models.execute_kw(
            database,
                uid,
                password,
                "pitch_booking.venue",
                "search",
                [
                    [['id', '=', odoo_id]]
                ],
            )
            if (odoo_counterpart == []):
                return (json.dumps({'message': "ID '" + str(odoo_id) + "' does not exist in Odoo"}), 400, {'ContentType': 'application/json'})
            else:
                venue = Venue.query.get(Id)
                venue_id = venue.id
                odoo_id = request.json["odooId"]
                name = request.json["name"]
                field_type = request.json["fieldType"]
                colour = request.json["colour"]
                num_pitches = request.json["numPitches"]
                created_at = datetime.now()
                updated_at = datetime.now()

                new_field = Field(name, venue_id, field_type, num_pitches, colour, created_at, updated_at, odoo_id)
                db.session.add(new_field)
                db.session.commit()
                if int(num_pitches) >= 1:
                    for i in range(int(num_pitches)):
                        field_id = new_field.id
                        pitchname = "P" + str(i+1)
                        odoo_id = None
                        new_pitch = Pitch(pitchname, field_id, odoo_id)
                        db.session.add(new_pitch)
                db.session.commit()
        except exc.IntegrityError:
            return json.dumps({'message': "Name '" + name + "' already exists"}), 400, {'ContentType': 'application/json'}
        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400

# # Get lists of Field

# @app.route("/field", methods=["GET"])
# def get_fields():
#     all_fields = Field.query.all()
#     result = fields_schema.dump(all_fields)
#     return jsonify(result)


# # Get field and Pitch based on field ID
# @app.route("/fields/<field_id>", methods=["GET"])
# def get_pitch_based_on_field_id(field_id):
#     all_pitches = Pitch.query.filter_by(field_id=field_id).all()
#     result = pitches_schema.dump(all_pitches)
#     return pitches_schema.jsonify(result)


# Get list of fields
@app.route("/fields", methods=["GET"])
def get_fieldss():
    field = Field.query.order_by(Field.id).all()
    results = fields2_schema.dump(field)
    return jsonify(results)


# Get field based on Id
@app.route("/field/<Id>", methods=["GET"])
def get_fields_based_on_id(Id):
    field = Field.query.get(Id)

    return field2_schema.jsonify(field)

# Update a Field
@app.route("/field/<Id>", methods=["PUT"])
def update_field(Id):
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        try:
            field = Field.query.get(Id)

            name = request.json["name"]
            field_type = request.json["fieldType"]
            colour = request.json["colour"]
            updatedat = datetime.now()

            field.name = name
            field.field_type = field_type
            field.colour = colour
            field.updatedat = updatedat

            db.session.commit()
        except exc.IntegrityError:
            return json.dumps({'message': "Name '" + name + "' already exists"}), 400, {'ContentType': 'application/json'}
        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400


# Delete Field
@app.route("/field/<Id>", methods=["DELETE"])
def delete_field(Id):
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        field = Field.query.get(Id)

        db.session.delete(field)
        db.session.commit()

        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400