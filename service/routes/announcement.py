from flask import request, jsonify
from service import app
from service.models import Announcement, announcement_schema, announcements_schema
from datetime import datetime
from service import db

# Create announcement
@app.route('/announcement', methods=["POST"])
def add_announcement():
    html_string = request.json["html_string"]
    markdown_string = request.json["markdown_string"]
    placement = request.json["placement"]
    visibility = request.json["visibility"]
    updated_at = datetime.now()
    new_announcement = Announcement(html_string, markdown_string, placement, visibility, updated_at)

    db.session.add(new_announcement)
    db.session.commit()

    return announcement_schema.jsonify(new_announcement)

# Update announcement
@app.route("/announcement/<Id>", methods=["PUT"])
def update_announcement(Id):
    announcement = Announcement.query.get(Id)

    html_string = request.json["html_string"]
    placement = request.json["placement"]
    markdown_string = request.json["markdown_string"]
    visibility = request.json["visibility"]
    updatedat = datetime.now()

    announcement.html_string = html_string
    announcement.markdown_string = markdown_string
    announcement.placement = placement
    announcement.updated_at = updatedat
    announcement.visibility = visibility
    db.session.commit()

    return announcement_schema.jsonify(announcement)

# Get announcement
@app.route("/announcement", methods=["GET"])
def get_announcement():
    all_announcement = Announcement.query.all()
    result = announcements_schema.dump(all_announcement)
    return jsonify(result)

# Get announcement by Id
@app.route("/announcement/<Id>", methods=["GET"])
def get_venue(Id):
    announcement = Announcement.query.get(Id)
    return announcement_schema.jsonify(announcement)
