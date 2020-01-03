from flask import request, jsonify
from service import app
from service.models import Admin, admin_schema, admins_schema
from flask import request
from sqlalchemy import exc
import json
from service import db
import jwt
import bcrypt


@app.route("/signin", methods=["POST"])
def signin():
    req_data = request.get_json()

    login_id = req_data["userId"]
    login_password = req_data["password"]
    hashed_password = ""

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()

    admin = Admin.query.all()
    result = admins_schema.dump(admin)

    for p in result:
        if p["user_id"] == login_id:
            hashed_password = p["password"]
            id = p["id"]
            if bcrypt.checkpw(
                login_password.encode("utf-8"), hashed_password.encode("utf-8")
            ):
                token = jwt.encode({"customer_id": id}, key, algorithm="HS256")
                stringtoken = token.decode("utf-8")
                return {
                    "userId": id,
                    "user": login_id,
                    "token": stringtoken
                }
            else:
                return "Login Failed", 400
    return "Login Failed", 400
  