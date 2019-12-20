from flask import request, jsonify
from service import app
from service.models import Announcement, announcement_schema
from datetime import datetime
from service import db

# Create announcement
@app.route('/announcement', methods=["POST"])
def add_announcement():
    html_string = request.json["html_string"]
    placement = request.json["placement"]
    visibility = request.json["visibility"]
    updated_at = datetime.now()
    new_announcement = Announcement(html_string, placement, visibility, updated_at)

    db.session.add(new_announcement)
    db.session.commit()

    return announcement_schema.jsonify(new_announcement)

# Update announcement
@app.route("/announcement/<Id>", methods=["PUT"])
def update_announcement(Id):
    announcement = Announcement.query.get(Id)

    html_string = request.json["html_string"]
    placement = request.json["placement"]
    visibility = request.json["visibility"]
    updatedat = datetime.now()

    announcement.html_string = html_string
    announcement.placement = placement
    announcement.updated_at = updatedat
    announcement.visibility = visibility
    db.session.commit()

    return announcement_schema.jsonify(announcement)

# # Get announcement
# @app.route("/field  ", methods=["GET"])
# def get_fields():
#     all_fields = Field.query.all()
#     result = fields_schema.dump(all_fields)
#     return jsonify(result)
