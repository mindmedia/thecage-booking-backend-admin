from flask import request, jsonify
from service import app
from service.models import promo_code_schema, promo_codes_schema, PromoCode, Product, products_schema, Venue, venues_schema, PromoCodeValidProduct, promo_code_valid_products_schema, PromoCodeValidLocation, promo_code_valid_locations_schema, PromoCodeValidTiming, promo_code_valid_timings_schema
from datetime import datetime
from sqlalchemy import exc
import json
from service import db
import jwt

# Create new PromotionCode
@app.route("/promotioncode", methods=['POST'])
def add_promo_code():
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        try:
            code = request.json["code"]
            valid_from = request.json["validFrom"]
            valid_to = request.json["validTo"]
            usage_limit = request.json["usageLimit"]
            times_used = 0
            usage_per_user = request.json["usageperUser"]
            discount_type = request.json["discountType"]
            discount = request.json["discount"]
            created_at = datetime.now()
            updated_at = datetime.now()

            new_promo_code = PromoCode(code, valid_from, valid_to, usage_limit, times_used, usage_per_user, discount_type, discount, created_at, updated_at)
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
                db.session.commit()
            timing_included = request.json["timingIncluded"]
            if timing_included is True:
                valid_timing = request.json["validTiming"]
                for i in valid_timing:
                    day_of_week = i["day"]
                    timing = i["timing"]
                    if len(timing) > 0:
                        for i in timing:
                            promo_code_id = new_promo_code.id
                            start_time = i["startTime"]
                            end_time = i["endTime"]
                            new_valid_timing = PromoCodeValidTiming(start_time, end_time, day_of_week, promo_code_id)
                            db.session.add(new_valid_timing)
                    else:
                        promo_code_id = new_promo_code.id
                        start_time = "00:00:00"
                        end_time = "23:59:59"
                        new_valid_timing = PromoCodeValidTiming(start_time, end_time, day_of_week, promo_code_id)
                        db.session.add(new_valid_timing)

                db.session.commit()

        except exc.IntegrityError:
            return json.dumps({'message': "Code '" + code + "' already exists"}), 400, {'ContentType': 'application/json'}
        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400

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
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        try:
            promocode = PromoCode.query.get(Id)
            code = request.json["code"]
            valid_from = request.json["validFrom"]
            valid_to = request.json["validTo"]
            usage_limit = request.json["usageLimit"]
            usage_per_user = request.json["usageperUser"]
            discount_type = request.json["discountType"]
            discount = request.json["discount"]
            updated_at = datetime.now()

            promocode.code = code
            promocode.valid_from = valid_from
            promocode.valid_to = valid_to
            promocode.usage_limit = usage_limit
            promocode.usage_per_user = usage_per_user
            promocode.discount_type = discount_type
            promocode.discount = discount
            promocode.updated_at = updated_at

            db.session.commit()

            validproduct = PromoCodeValidProduct.query.all()
            result = promo_code_valid_products_schema.dump(validproduct)
            for i in result:
                if i["promo_code_id"] == promocode.id:
                    valid_product_id = i["id"]
                    promocode_validproduct = PromoCodeValidProduct.query.get(valid_product_id)
                    db.session.delete(promocode_validproduct)
                    db.session.commit()

            valid_locations = PromoCodeValidLocation.query.all()
            result = promo_code_valid_locations_schema.dump(valid_locations)
            for i in result:
                if i["promo_code_id"] == promocode.id:
                    valid_location_id = i["id"]
                    promocode_validlocation = PromoCodeValidLocation.query.get(valid_location_id)
                    db.session.delete(promocode_validlocation)
                    db.session.commit()

            validtimings = PromoCodeValidTiming.query.all()
            result = promo_code_valid_timings_schema.dump(validtimings)
            for i in result:
                if i["promo_code_id"] == promocode.id:
                    valid_timing_id = i['id']
                    promocode_validtiming = PromoCodeValidTiming.query.get(valid_timing_id)
                    db.session.delete(promocode_validtiming)
                    db.session.commit()

            promo_code_id = promocode.id
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
                db.session.commit()

            timing_included = request.json["timingIncluded"]
            if timing_included is True:
                valid_timing = request.json["validTiming"]
                for i in valid_timing:
                    day_of_week = i["day_of_week"]
                    timing = i["timing"]
                    if len(timing) > 0:
                        for i in timing:
                            start_time = i["start_time"]
                            end_time = i["end_time"]
                            new_valid_timing = PromoCodeValidTiming(start_time, end_time, day_of_week, promo_code_id)
                            db.session.add(new_valid_timing)
                    else:

                        start_time = "00:00:00"
                        end_time = "23:59:59"
                        new_valid_timing = PromoCodeValidTiming(start_time, end_time, day_of_week, promo_code_id)
                        db.session.add(new_valid_timing)

                db.session.commit()

        except exc.IntegrityError:
            return json.dumps({'message': "Code '" + code + "' already exists"}), 400, {'ContentType': 'application/json'}
        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400

# Delete Promo Code
@app.route("/promotioncode/<Id>", methods=["DELETE"])
def delete_promo_code(Id):
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    role = jwt.decode(token, key, algorithms=['HS256'])["role"]
    if role == "SuperAdmin":
        promocode = PromoCode.query.get(Id)
        db.session.delete(promocode)
        db.session.commit()

        return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
    else:
        return "You are not authorised to perform this action", 400

# Get ValidTimings based on PromoCodeId
@app.route("/validtimings/<promo_code_id>", methods=["GET"])
def get_validtimings_based_on_promocode_id(promo_code_id):
    return_list = []
    allvalidtimings = PromoCodeValidTiming.query.filter_by(promo_code_id=promo_code_id).all()
    for x in range(7):
        if day_of_week(x, promo_code_id) != "":
            return_list.append(day_of_week(x, promo_code_id))
    # print(return_list)
    return jsonify(return_list)


def zero(promo_code_id):
    return_dict = {'day_of_week':'Monday'}
    return_dict.setdefault('timing', [])
    mondayvalidtimings = PromoCodeValidTiming.query.filter_by(promo_code_id=promo_code_id, day_of_week="Monday").all()
    result_mondayvalidtimings = promo_code_valid_timings_schema.dump(mondayvalidtimings)
    if result_mondayvalidtimings == []:
        return ""
    for validtiming in result_mondayvalidtimings:
        if validtiming["start_time"] == "00:00:00" and validtiming["end_time"] == "23:59:59":
            del validtiming["start_time"]
            del validtiming["end_time"]
            del validtiming["day_of_week"]
            del validtiming["id"]
            del validtiming["promo_code_id"]
        else:
            return_dict['timing'].append(validtiming)
    return return_dict


def one(promo_code_id):
    return_dict = {'day_of_week':'Tuesday'}
    return_dict.setdefault('timing', [])
    tuesdayvalidtimings = PromoCodeValidTiming.query.filter_by(promo_code_id=promo_code_id, day_of_week="Tuesday").all()
    result_tuesdayvalidtimings = promo_code_valid_timings_schema.dump(tuesdayvalidtimings)
    if result_tuesdayvalidtimings == []:
        return ""
    for validtiming in result_tuesdayvalidtimings:
        if validtiming["start_time"] == "00:00:00" and validtiming["end_time"] == "23:59:59":
            del validtiming["start_time"]
            del validtiming["end_time"]
            del validtiming["day_of_week"]
            del validtiming["id"]
            del validtiming["promo_code_id"]
        else:
            return_dict['timing'].append(validtiming)
    return return_dict


def two(promo_code_id):
    return_dict = {'day_of_week':'Wednesday'}
    return_dict.setdefault('timing', [])
    wednesdayvalidtimings = PromoCodeValidTiming.query.filter_by(promo_code_id=promo_code_id, day_of_week="Wednesday").all()
    result_wednesdayvalidtimings = promo_code_valid_timings_schema.dump(wednesdayvalidtimings)
    if result_wednesdayvalidtimings == []:
        return ""
    for validtiming in result_wednesdayvalidtimings:
        if validtiming["start_time"] == "00:00:00" and validtiming["end_time"] == "23:59:59":
            del validtiming["start_time"]
            del validtiming["end_time"]
            del validtiming["day_of_week"]
            del validtiming["id"]
            del validtiming["promo_code_id"]
        else:
            return_dict['timing'].append(validtiming)
    return return_dict


def three(promo_code_id):
    return_dict = {'day_of_week':'Thursday'}
    return_dict.setdefault('timing', [])
    thursdayvalidtimings = PromoCodeValidTiming.query.filter_by(promo_code_id=promo_code_id, day_of_week="Thursday").all()
    result_thursdayvalidtimings = promo_code_valid_timings_schema.dump(thursdayvalidtimings)
    print(result_thursdayvalidtimings)
    if result_thursdayvalidtimings == []:
        return ""
    for validtiming in result_thursdayvalidtimings:
        if validtiming["start_time"] == "00:00:00" and validtiming["end_time"] == "23:59:59":
            del validtiming["start_time"]
            del validtiming["end_time"]
            del validtiming["day_of_week"]
            del validtiming["id"]
            del validtiming["promo_code_id"]
        else:
            return_dict['timing'].append(validtiming)
    return return_dict


def four(promo_code_id):
    return_dict = {'day_of_week':'Friday'}
    return_dict.setdefault('timing', [])
    fridayvalidtimings = PromoCodeValidTiming.query.filter_by(promo_code_id=promo_code_id, day_of_week="Friday").all()
    result_fridayvalidtimings = promo_code_valid_timings_schema.dump(fridayvalidtimings)
    if result_fridayvalidtimings == []:
        return ""
    for validtiming in result_fridayvalidtimings:
        if validtiming["start_time"] == "00:00:00" and validtiming["end_time"] == "23:59:59":
            del validtiming["start_time"]
            del validtiming["end_time"]
            del validtiming["day_of_week"]
            del validtiming["id"]
            del validtiming["promo_code_id"]
        else:
            return_dict['timing'].append(validtiming)
    return return_dict


def five(promo_code_id):
    return_dict = {'day_of_week':'Saturday'}
    return_dict.setdefault('timing', [])
    saturdayvalidtimings = PromoCodeValidTiming.query.filter_by(promo_code_id=promo_code_id, day_of_week="Saturday").all()
    result_saturdayvalidtimings = promo_code_valid_timings_schema.dump(saturdayvalidtimings)
    if result_saturdayvalidtimings == []:
        return ""
    for validtiming in result_saturdayvalidtimings:
        if validtiming["start_time"] == "00:00:00" and validtiming["end_time"] == "23:59:59":
            del validtiming["start_time"]
            del validtiming["end_time"]
            del validtiming["day_of_week"]
            del validtiming["id"]
            del validtiming["promo_code_id"]
        else:
            return_dict['timing'].append(validtiming)
    return return_dict


def six(promo_code_id):
    return_dict = {'day_of_week':'Sunday'}
    return_dict.setdefault('timing', [])
    sundayvalidtimings = PromoCodeValidTiming.query.filter_by(promo_code_id=promo_code_id, day_of_week="Sunday").all()
    result_sundayvalidtimings = promo_code_valid_timings_schema.dump(sundayvalidtimings)
    if result_sundayvalidtimings == []:
        return ""
    for validtiming in result_sundayvalidtimings:
        if validtiming["start_time"] == "00:00:00" and validtiming["end_time"] == "23:59:59":
            del validtiming["start_time"]
            del validtiming["end_time"]
            del validtiming["day_of_week"]
            del validtiming["id"]
            del validtiming["promo_code_id"]
        else:
            return_dict['timing'].append(validtiming)
    return return_dict


def day_of_week(i, promo_code_id):
    switcher = {
        0: zero,
        1: one,
        2: two,
        3: three,
        4: four,
        5: five,
        6: six
    }
    func = switcher.get(i, lambda: "Invalid day of week")
    return func(promo_code_id)
