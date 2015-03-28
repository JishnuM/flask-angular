from flask import abort, Blueprint, jsonify, request
from database import Database, User, Unit, Address
import json

api = Blueprint('api', __name__)

db = Database()

@api.route('/user', methods=['GET'])
def get_current_user():
    return jsonify(user='current')
    ## TODO implement properly when adding login

@api.route('/user/<userid>', methods=['GET', 'POST', 'DELETE'])
def handle_user_request(userid):
    userid = int(userid)
    if request.method == 'GET':
        user = db.get_user(userid)
        if not user:
            abort(404)
        else:
            return jsonify(user.__dict__)
    elif request.method == 'POST':
        update_data = request.get_json(force=True)
        updated_user = User(userid, update_data['email'], update_data['first_name'], update_data['last_name'])
        db.update_user(updated_user)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    elif request.method == 'DELETE':
        db.delete_user(userid)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        abort()

@api.route('/unit/<unitid>', methods=['GET', 'POST', 'DELETE'])
def handle_unit_request(unitid):
    unitid = int(unitid)
    if request.method == 'GET':
        unit = db.get_unit_dict(unitid)
        if not unit:
            abort(404)
        else:
            return jsonify(unit)
    elif request.method == 'POST':
        ## TODO consider changing to allow update of only one field
        ## instead of replacing entire object on each update
        update_data = request.get_json(force=True)
        updated_address = Address(update_data['block'], update_data['street'], update_data['pin'], update_data['city'], update_data['country'], update_data['lat'], update_data['lng'])
        creator = db.get_user(update_data['creator_id'])
        if not creator:
            return json.dumps({'success':False}), 200, {'ContentType':'application/json'}
        updated_unit = Unit(unitid, updated_address, update_data['num_rooms'], update_data['num_bathrooms'], update_data['sqft'], creator)
        db.update_unit(updated_unit)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    elif request.method == 'DELETE':
        db.delete_unit(unitid)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        abort()

## Consider making this a PUT call to user / unit
@api.route('/createuser', methods=['POST'])
def create_user():
    user_data = request.get_json(force=True)
    user_id = db.create_user(user_data['email'], user_data['first_name'], user_data['last_name'])
    return jsonify(user_id=user_id)

@api.route('/createunit', methods=['POST'])
def create_unit():
    unit_data = request.get_json(force=True)
    unit_address = Address(unit_data['block'], unit_data['street'], unit_data['pin'], unit_data['city'], unit_data['country'], unit_data['lat'], unit_data['lng'])
    unit_id = db.create_unit(unit_address, unit_data['num_rooms'], unit_data['num_bathrooms'], unit_data['sqft'], unit_data['creator_id'])
    return jsonify(unit_id=unit_id)
