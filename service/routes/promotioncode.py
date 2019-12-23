from flask import request, jsonify
from service import app
from service.models import promo_code_schema, PromoCode
from datetime import datetime
from service import db

# Create new PromotionCode
@app.route("/promotioncode", methods=['POST'])
def add_promo_code():
    code = request.json["code"]
    valid_from = request.json["validFrom"]
    valid_to = request.json["validTo"]
    usage_limit = request.json["usageLimit"]
    uses_left = request.json["usesLeft"] 
    discount_type = request.json["discountType"]
    discount = request.json["discount"]
    created_at = datetime.now()
    updated_at = datetime.now()

    new_promo_code = PromoCode(code, valid_from, valid_to, usage_limit, uses_left, discount_type, discount, created_at, updated_at)
    db.session.add(new_promo_code)
    db.session.commit()

    return promo_code_schema.jsonify(new_promo_code)
