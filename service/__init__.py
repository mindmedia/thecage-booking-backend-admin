# app.py or app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True)
CORS(app, allow_headers='*')
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
import service.routes.bookinghistory
import service.routes.customer
import service.routes.venue
import service.routes.field
import service.routes.pitch
import service.routes.announcement
import service.routes.customtimeslot
import service.routes.discount
import service.routes.product
import service.routes.promotioncode
import service.routes.product
import service.routes.purchaseitem
import service.routes.purchaselog

# Now we can access the configuration variables via app.config["VAR_NAME"].
