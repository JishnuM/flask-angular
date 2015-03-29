from flask import abort, Blueprint, jsonify, request
from database import Database
import json

api = Blueprint('api', __name__)

db = None

@api.record
def record_setup(setup_state):
    global db
    app = setup_state.app
    mongo_url = app.config.get('MONGODB_URL')
    mongo_db_name = app.config.get('MONGODB_DBNAME')
    db = Database(mongo_url, mongo_db_name)

@api.route('/user', methods=['GET'])
def get_current_user():
    return jsonify(user='current')
    ## TODO implement properly when adding login

@api.route('/user/<userid>', methods=['GET', 'POST', 'DELETE'])
def handle_user_request(userid):
    if request.method == 'GET':
        user = db.get_user(userid)
        if not user:
            abort(404)
        else:
            return jsonify(user)
    elif request.method == 'POST':
        update_data = request.get_json(force=True)
        update_success = db.update_user(userid, update_data)
        return jsonify(success=update_success)
    elif request.method == 'DELETE':
        delete_success = db.delete_user(userid)
        return jsonify(success=delete_success)
    else:
        abort()

@api.route('/unit/<unitid>', methods=['GET', 'POST', 'DELETE'])
def handle_unit_request(unitid):
    if request.method == 'GET':
        unit = db.get_unit(unitid)
        if not unit:
            abort(404)
        else:
            return jsonify(unit)
    elif request.method == 'POST':
        update_data = request.get_json(force=True)
        update_success = db.update_unit(unitid, update_data)
        return jsonify(success=update_success)
    elif request.method == 'DELETE':
        delete_success = db.delete_unit(unitid)
        return jsonify(success=delete_success)
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
    unit_id = db.create_unit(unit_data['block'], unit_data['street'], unit_data['pin'], unit_data['city'], unit_data['country'], unit_data['lat'], unit_data['lng'], unit_data['num_rooms'], unit_data['num_bathrooms'], unit_data['sqft'], unit_data['creator_id'])
    return jsonify(unit_id=unit_id)
