from flask import request, jsonify
from service import app
from service.models import promo_code_schema, Discount, PromoCode
from datetime import datetime
from service import db

# Create new PromotionCode
@app.route("/promotioncode", methods=['POST'])
def add_promo_code():
    code = request.json["code"]
    valid_from = request.json["valid_from"]
    valid_to = request.json["valid_to"]
    usage_limit = request.json["usage_limit"]
    uses_left = request.json["uses_left"]
    discount_type = request.json["discount_type"]
    discount = request.json["discount"]
    created_at = datetime.now()
    updated_at = datetime.now()

    new_discount = Discount(discount_type, discount)
    db.session.add(new_discount)
    db.session.commit()

    discount_id = new_discount.id
    new_promo_code = PromoCode(discount_id, code, valid_from, valid_to, usage_limit, uses_left, created_at, updated_at)

    db.session.add(new_promo_code)
    db.session.commit()

    return promo_code_schema.jsonify(new_promo_code)
