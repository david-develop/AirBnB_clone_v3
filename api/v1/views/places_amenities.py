#!/usr/bin/python3
"""Flask app to handle Place API"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_place(place_id):
    """Retrieves the list of all Place objects of a City"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities_list = [amenity.to_dict() for amenity in place_obj.amenities]
        return jsonify(amenities_list)

    else:
        amenities_list = []
        for amenity_id in place_obj.amenity_ids:
            amenities_list.append(storage.get("Amenity", amenity_id).to_dict())
        return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity_place(place_id, amenity_id):
    """Deletes a Amenity object of a Place"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities_id_list = [amenity.id for amenity in place_obj.amenities]
        if amenity_obj not in place_obj.amenities:
            abort(404)
        place_obj.amenities.remove(amenity_obj)

    else:
        amenities_id_list = place_obj.amenity_ids
        if amenity_obj.id not in amenities_id_list:
            abort(404)
        place_obj.amenity_ids.remove(amenity_obj.id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def post_amenity_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404)

    amenity_dict = amenity_obj.to_dict()

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity_obj in  place_obj.amenities:
            return jsonify(amenity_dict), 200
        place_obj.amenities.append(amenity_obj)

    else:
        if amenity_obj.id in place.amenity_ids:
            return jsonify(amenity_dict), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity_dict), 201
