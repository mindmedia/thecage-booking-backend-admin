from flask import request, jsonify
from service import app
from service.models import Admin, admin_schema, admins_schema
from sqlalchemy import exc
import json
from service import db

# Create an Admin
@app.route("/admin", methods=["POST"])
def add_admin():
    try:
        user_id = request.json["user_id"]
        password = request.json["password"]
        role = request.json["role"]

        new_admin = Admin(user_id, password, role)

        db.session.add(new_admin)
        db.session.commit()

    except exc.IntegrityError:
        return json.dumps({'message': "User Id '" + user_id + "' already exists"}), 400, {'ContentType': 'application/json'}
    return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})


# Get lists of Admin
@app.route("/admin", methods=["GET"])
def get_admins():
    all_admins = Admin.query.all()
    result = admins_schema.dump(all_admins)
    return jsonify(result)


# Get Admin based on ID
@app.route("/admin/<Id>", methods=["GET"])
def get_admin(Id):
    admin = Admin.query.get(Id)
    return admin_schema.jsonify(admin)


# Update an Admin
@app.route("/admin/<Id>", methods=["PUT"])
def update_admin(Id):
    try:
        admin = Admin.query.get(Id)

        user_id = request.json["user_id"]
        password = request.json["password"]

        admin.user_id = user_id
        admin.password = password

        db.session.commit()

    except exc.IntegrityError:
        return json.dumps({'message': "User Id '" + user_id + "' already exists"}), 400, {'ContentType': 'application/json'}
    return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})


# Delete Admin
@app.route("/admin/<Id>", methods=["DELETE"])
def delete_admin(Id):
    admin = Admin.query.get(Id)
    db.session.delete(admin)
    db.session.commit()

    return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
