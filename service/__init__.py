# app.py or app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.config.from_pyfile("config.py")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)


@app.route("/")
def index():
    return "Hello World!"


import service.routes.admin
import service.routes.customer
import service.routes.venue
import service.routes.field
import service.routes.pitch

# Now we can access the configuration variables via app.config["VAR_NAME"].
