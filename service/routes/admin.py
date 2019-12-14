from flask import request, jsonify
from service import app
from service.models import Admin, admin_schema, admins_schema

from service import db

# Create an Admin
@app.route("/admin", methods=["POST"])
def add_admin():
    user_id = request.json["user_id"]
    password = request.json["password"]
    name = request.json["name"]
    role = request.json["role"]

    new_admin = Admin(user_id, password, role)

    db.session.add(new_admin)
    db.session.commit()

    return admin_schema.jsonify(new_admin)


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
    admin = Admin.query.get(Id)

    user_id = request.json["user_id"]
    password = request.json["password"]
    name = request.json["name"]
    role = request.json["role"]

    admin.name = name
    admin.user_id = user_id
    admin.password = password
    admin.role = role

    db.session.commit()

    return admin_schema.jsonify(admin)


# Delete Admin
@app.route("/admin/<Id>", methods=["DELETE"])
def delete_admin(Id):
    admin = Admin.query.get(Id)
    db.session.delete(admin)
    db.session.commit()

    return admin_schema.jsonify(admin)
