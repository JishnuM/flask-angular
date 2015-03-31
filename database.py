from pymongo import MongoClient
from bson.objectid import ObjectId

class Database:

    def __init__(self, db_url, db_name):
        client = MongoClient(db_url)
        db = client[db_name]
        self.users = db.users
        self.units = db.units
        self.addresses = db.addresses

    def create_user(self, email, first_name, last_name):
        user = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        }
        user_id = self.users.insert_one(user).inserted_id
        return str(user_id)

    def update_user(self, uid, input_dict):
        user_id = ObjectId(uid)
        update_dict = {}
        user_keys = ['email', 'first_name', 'last_name']
        for key in input_dict:
            if key in user_keys:
                update_dict[key] = input_dict[key]
        if not update_dict:
            return False
        res = self.users.update_one({'_id': user_id}, {'$set': update_dict}, False)
        if (res.modified_count == 0):
            return False
        else:
            return True

    def delete_user(self, uid):
        user_id = ObjectId(uid)
        res_user = self.users.delete_one({'_id': user_id})
        for unit in self.units.find({'creator_id': user_id}):
            address_id = unit['address_id']
            db.addresses.delete_one({'_id': address_id})
        self.units.delete_many({'creator_id': user_id})
        if (res_user.deleted_count == 0):
            return False
        else:
            return True

    def get_user(self, uid):
        user_id = ObjectId(uid)
        user_doc = self.users.find_one({'_id': user_id})
        if user_doc:
            return {
                'uid': str(user_doc['_id']),
                'email': user_doc['email'],
                'first_name': user_doc['first_name'],
                'last_name': user_doc['last_name']
            }
        else:
            return None

    def get_all_users(self):
        to_return = []
        for user_doc in self.users.find():
            user_dict = {
                'uid': str(user_doc['_id']),
                'email': user_doc['email'],
                'first_name': user_doc['first_name'],
                'last_name': user_doc['last_name']
            
            }
            to_return.append(user_dict)
        return to_return

    def get_user_by_email(self, email):
        user_doc = self.users.find_one({'email': email})
        if user_doc:
            return {
                'uid': str(user_doc['_id']),
                'email': user_doc['email'],
                'first_name': user_doc['first_name'],
                'last_name': user_doc['last_name']
            }
        else:
            return None

    def create_unit(self, block, street, pin, city, country, lat, lng, num_rooms, num_bathrooms, sqft, creator_id_str):
        address = {
            'block_number': block,
            'street_name': street,
            'postal_code': pin,
            'city': city,
            'country': country,
            'coordinates': [lat, lng]
        }
        address_id = self.addresses.insert_one(address).inserted_id
        creator_id = ObjectId(creator_id_str)
        unit = {
            'address_id': address_id,
            'num_rooms': num_rooms,
            'num_bathrooms': num_bathrooms,
            'sqft': sqft,
            'creator_id': creator_id
        }
        unit_id = self.units.insert_one(unit).inserted_id
        return str(unit_id)

    def update_unit(self, uid, unit_dict):
        address_updates = {}
        unit_updates = {}
        unit_keys = ['num_rooms', 'num_bathrooms', 'sqft']
        address_keys = ['block_number', 'street_name', 'postal_code', 'city', 'country', 'coordinates'] 
        for key in unit_dict:
            if key in unit_keys:
                unit_updates[key] = unit_dict[key]
            elif key in address_keys:
                address_updates[key] = unit_dict[key]
        unit_id = ObjectId(uid)
        to_update = self.units.find_one({'_id': unit_id})
        address_id = to_update['address_id']
        creator_id = to_update['creator_id']
        creator = self.users.find_one({'_id': creator_id})
        if not creator:
            return False
        updated_count = 0
        if unit_updates:
            res_unit = self.units.update_one({'_id': unit_id}, {'$set': unit_updates}, False)
            updated_count += res_unit.modified_count
        if address_updates:
            res_addr = self.addresses.update_one({'_id': address_id}, {'$set': address_updates}, False)
            updated_count += res_addr.modified_count
        if updated_count == 0:
            return False
        else:
            return True
    
    def delete_unit(self, uid):
        unit_id = ObjectId(uid)
        to_delete = self.units.find_one({'_id': unit_id})
        address_id = to_delete['address_id']
        res_unit = self.units.delete_one({'_id': unit_id})
        res_addr = self.addresses.delete_one({'_id': address_id})        
        if (res_unit.deleted_count > 0 or res_addr.deleted_count > 0):
            return True
        else:
            return False

    def get_unit(self, uid):
        unit_id = ObjectId(uid)
        unit_doc = self.units.find_one({'_id': unit_id})
        if unit_doc:
            unit = {
                'uid': uid,
                'num_rooms': unit_doc['num_rooms'],
                'num_bathrooms': unit_doc['num_bathrooms'],
                'sqft': unit_doc['sqft'],
                'creator_id': str(unit_doc['creator_id'])
            }
            address_doc = self.addresses.find_one({'_id': unit_doc['address_id']})
            if not address_doc: 
                return None
            address = {
                'block_number': address_doc['block_number'],
                'street_name': address_doc['street_name'],
                'postal_code': address_doc['postal_code'],
                'city': address_doc['city'],
                'country': address_doc['country'],
                'coordinates': address_doc['coordinates']
            }
            unit['address'] = address
            return unit
        else:
            return None

    def get_all_units(self, uid):
        user_id = ObjectId(uid)
        to_return = []
        for unit_doc in self.units.find({'creator_id': user_id}):
            unit = {
                'uid': str(unit_doc['_id']),
                'num_rooms': unit_doc['num_rooms'],
                'num_bathrooms': unit_doc['num_bathrooms'],
                'sqft': unit_doc['sqft'],
                'creator_id': str(unit_doc['creator_id'])
            }
            address_doc = self.addresses.find_one({'_id': unit_doc['address_id']})
            if not address_doc: 
                continue;
            address = {
                'block_number': address_doc['block_number'],
                'street_name': address_doc['street_name'],
                'postal_code': address_doc['postal_code'],
                'city': address_doc['city'],
                'country': address_doc['country'],
                'coordinates': address_doc['coordinates']
            }
            unit['address'] = address
            to_return.append(unit)
        return to_return
