from flask import request, jsonify
from service import app
from service.models import Admin, admin_schema, admins_schema
from sqlalchemy import exc
import json
from service import db
from parse import parse
import bcrypt

# Create an Admin
@app.route("/admin", methods=["POST"])
def add_admin():
    req_data = request.get_json()

    user_id = req_data["user_id"]
    password = req_data["password"]
    role = "Admin"
    try:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf8"), salt)
        password = hashed_password.decode("utf8")

        new_admin = Admin(user_id, password, role)

        db.session.add(new_admin)
        db.session.commit()

    except exc.IntegrityError as e:
        dupe_field = parse('duplicate key value violates unique constraint "{constraint}"\nDETAIL:  Key ({field})=({input}) already exists.\n', str(e.orig))["field"]
        print(dupe_field)
        return json.dumps({'message': f'{dupe_field} already exists'}), 400, {'ContentType': 'application/json'}
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
    old_password = request.json.get("oldPassword")

    if admin.password == old_password:
        try:
            admin.user_id = user_id
            admin.password = password

            db.session.commit()
        except exc.IntegrityError:
            return json.dumps({'message': "User Id '" + user_id + "' already exists"}), 400, {'ContentType': 'application/json'}
    else:
        return json.dumps({'message': 'Passwords do not match'}), 400, {'ContentType': 'application/json'}
    return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})


# Delete Admin
@app.route("/admin/<Id>", methods=["DELETE"])
def delete_admin(Id):
    admin = Admin.query.get(Id)
    db.session.delete(admin)
    db.session.commit()

    return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
