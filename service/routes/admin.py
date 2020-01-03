from flask import request, jsonify
from service import app
from service.models import Admin, admin_schema, admins_schema
from sqlalchemy import exc
import json
from service import db
from parse import parse
import bcrypt
import jwt

# Create an Admin
@app.route("/admin", methods=["POST"])
def add_admin():
    req_data = request.get_json()

    user_id = req_data["userId"]
    password = req_data["password"]
    role_name = "Admin"
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode("utf8"), salt)
            password = hashed_password.decode("utf8")

            new_admin = Admin(user_id, password, role_name)

            db.session.add(new_admin)
            db.session.commit()

        except exc.IntegrityError as e:
            dupe_field = parse('duplicate key value violates unique constraint "{constraint}"\nDETAIL:  Key ({field})=({input}) already exists.\n', str(e.orig))["field"]
            print(dupe_field)
            return json.dumps({'message': f'{dupe_field} already exists'}), 400, {'ContentType': 'application/json'}
        return admin_schema.jsonify(new_admin)
    else:
        return "You are not authorised to perform this action", 400

# Get lists of Admin
@app.route("/admin", methods=["GET"])
def get_admins():
    all_admins = Admin.query.filter(Admin.role == "Admin").all()
    result = admins_schema.dump(all_admins)
    return jsonify(result)


# Get Admin based on ID
@app.route("/admin/<Id>", methods=["GET"])
def get_admin(Id):
    admin = Admin.query.get(Id)
    return admin_schema.jsonify(admin)


# Update own account
@app.route("/accountsettings", methods=["PUT"])
def account_settings():
    admin = Admin.query.get()

    user_id = request.json["userId"]
    password = request.json["password"]
    old_password = request.json.get("oldPassword")
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    user_id = jwt.decode(token, key, algorithms=['HS256'])["id"]
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

# Update an Admin
@app.route("/admin/<Id>", methods=["PUT"])
def update_admin(Id):
    admin = Admin.query.get(Id)

    user_id = request.json["userId"]
    password = request.json["password"]
    old_password = request.json.get("oldPassword")
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        try:
            admin.user_id = user_id
            admin.password = password

            db.session.commit()
        except exc.IntegrityError:
            return json.dumps({'message': "User Id '" + user_id + "' already exists"}), 400, {'ContentType': 'application/json'}
        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400

# Delete Admin
@app.route("/admin/<Id>", methods=["DELETE"])
def delete_admin(Id):
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        admin = Admin.query.get(Id)
        db.session.delete(admin)
        db.session.commit()

        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400
