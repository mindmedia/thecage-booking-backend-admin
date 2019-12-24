from flask import request, jsonify
from service import app
from service.models import promo_code_schema, promo_codes_schema, PromoCode, Product, products_schema, Venue, venues_schema, PromoCodeValidProduct, PromoCodeValidLocation
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
    usage_per_user = request.json["usageperUser"]
    discount_type = request.json["discountType"]
    discount = request.json["discount"]
    created_at = datetime.now()
    updated_at = datetime.now()

    new_promo_code = PromoCode(code, valid_from, valid_to, usage_limit, uses_left, usage_per_user, discount_type, discount, created_at, updated_at)
    db.session.add(new_promo_code)
    db.session.commit()

    promo_code_id = new_promo_code.id
    valid_product = request.json["validProduct"]
    product = Product.query.all()
    result = products_schema.dump(product)
    for p in result:
        if p["name"] == valid_product:
            product_id = p["id"]

    new_valid_product = PromoCodeValidProduct(valid_product, promo_code_id, product_id)
    db.session.add(new_valid_product)
    db.session.commit()

    valid_location = request.json["validLocation"]
    venue = Venue.query.all()
    result = venues_schema.dump(venue)
    for p in result:
        if p["name"] == valid_location:
            venue_id = p["id"]

    new_valid_location = PromoCodeValidLocation(valid_location, promo_code_id, venue_id)
    db.session.add(new_valid_location)
    db.session.commit()
    return promo_code_schema.jsonify(new_promo_code)

# Get PromotionCodes
@app.route("/promotioncodes", methods=['GET'])
def get_promo_code():
    promocode = PromoCode.query.all()
    result = promo_codes_schema.dump(promocode)
    return jsonify(result)

# Get PromotionCode based on Id
@app.route("/promotioncode/<Id>", methods=['GET'])
def get_promo_code_based_on_id(Id):
    promocode = PromoCode.query.get(Id)
    return promo_code_schema.jsonify(promocode)

# # Update PromotionCode
# @app.route("/promotioncode/<Id>", methods=['PUT'])
# def update_promo_code(Id):
#     promocode = PromoCode.query.get(Id)
#     code = request.json["code"]
#     valid_from = request.json["validFrom"]
#     valid_to = request.json["validTo"]
#     usage_limit = request.json["usageLimit"]
#     uses_left = request.json["usesLeft"]
#     usage_per_user = request.json["usageperUser"]
#     discount_type = request.json["discountType"]
#     discount = request.json["discount"]
#     updated_at = datetime.now()

#     promocode.code = code
#     promocode.valid_from = valid_from
#     promocode.valid_to = valid_to
#     promocode.usage_limit = usage_limit
#     promocode.uses_left = uses_left
#     promocode.usage_per_user = usage_per_user
#     promocode.discount_type = discount_type
#     promocode.discount = discount
#     promocode.updated_at = updated_at

#     db.session.commit()
    
#     promocode_id = promocode.id

#     promocodevalidlocation = PromoCodeValidLocation.query.filter_by(promo)
#     return promo_code_schema.jsonify(promocode)
