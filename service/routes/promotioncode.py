from flask import request, jsonify
from service import app
from service.models import promo_code_schema, promo_codes_schema, PromoCode, Product, products_schema, Venue, venues_schema, PromoCodeValidProduct, promo_code_valid_products_schema, PromoCodeValidLocation, PromoCodeValidTiming
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
    valid_products = request.json["validProducts"]
    for i in valid_products:
        valid_product = i
        product = Product.query.all()
        result = products_schema.dump(product)
        for p in result:
            if p["name"] == valid_product:
                product_id = p["id"]

        new_valid_product = PromoCodeValidProduct(valid_product, promo_code_id, product_id)
        db.session.add(new_valid_product)
        db.session.commit()

    valid_locations = request.json["validLocations"]
    for i in valid_locations:
        valid_location = i
        venue = Venue.query.all()
        result = venues_schema.dump(venue)
        for p in result:
            if p["name"] == valid_location:
                venue_id = p["id"]

        new_valid_location = PromoCodeValidLocation(valid_location, promo_code_id, venue_id)
        db.session.add(new_valid_location)
    timing_included = request.json["timingIncluded"]
    if timing_included is True:
        valid_timing = request.json["validTiming"]
        for i in valid_timing:
            day_of_week = i["dayOfWeek"]
            timing = i["timing"]
            for i in timing:
                promo_code_id = new_promo_code.id
                start_time = i["startTime"]
                end_time = i["endTime"]
                new_valid_timing = PromoCodeValidTiming(start_time, end_time, day_of_week, promo_code_id)
                db.session.add(new_valid_timing)

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

# Update PromotionCode
@app.route("/promotioncode/<Id>", methods=['PUT'])
def update_promo_code(Id):
    promocode = PromoCode.query.get(Id)
    code = request.json["code"]
    valid_from = request.json["validFrom"]
    valid_to = request.json["validTo"]
    usage_limit = request.json["usageLimit"]
    uses_left = request.json["usesLeft"]
    usage_per_user = request.json["usageperUser"]
    discount_type = request.json["discountType"]
    discount = request.json["discount"]
    updated_at = datetime.now()

    promocode.code = code
    promocode.valid_from = valid_from
    promocode.valid_to = valid_to
    promocode.usage_limit = usage_limit
    promocode.uses_left = uses_left
    promocode.usage_per_user = usage_per_user
    promocode.discount_type = discount_type
    promocode.discount = discount
    promocode.updated_at = updated_at

    db.session.commit()

    valid_product = request.json["validProduct"]
    validproduct = PromoCodeValidProduct.query.all()
    result = promo_code_valid_products_schema.dump(validproduct)
    for p in result:
        if p["name"] == valid_product:
            valid_product_id = p["id"]
    
    promocode_validproduct = PromoCodeValidProduct.query.get(valid_product_id)
    promocode_validproduct.name = valid_product



    return promo_code_schema.jsonify(promocode)


# Delete Promo Code
@app.route("/promotioncode/<Id>", methods=["DELETE"])
def delete_promo_code(Id):
    promocode = PromoCode.query.get(Id)
    db.session.delete(promocode)
    db.session.commit()

    return promo_code_schema.jsonify(promocode)