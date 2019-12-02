# app.py or app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
def index():
    return "Hello World!"

import service.routes.admin
import service.routes.customer

# Now we can access the configuration variables via app.config["VAR_NAME"].