import random, copy

class Database:

    def __init__(self):
        self.users = {}
        self.units = {}
    
    def create_user(self, email, first_name, last_name):
        uid = random.randint(1, 10000)
        while uid in self.users:
            uid = random.randint(1, 10000)
        user = User(uid, email, first_name, last_name)
        self.users[uid] = user
        return uid

    def update_user(self, user):
        self.users[user.uid] = user

    def delete_user(self, uid):
        del self.users[uid]

    def get_user(self, uid):
        if uid in self.users:
            return self.users[uid]
        else:
            return None  

    def create_unit(self, address, num_rooms, num_bathrooms, sqft, creator_id):
        uid = random.randint(1, 10000)
        while uid in self.units:
            uid = random.randint(1, 10000)
        creator = self.users[creator_id]
        unit = Unit(uid, address, num_rooms, num_bathrooms, sqft, creator)
        self.units[uid] = unit
        return uid     

    def update_unit(self, unit):
        self.units[unit.uid] = unit
    
    def delete_unit(self, uid):
        if uid in self.units:
            del self.units[uid]

    def get_unit_dict(self, uid):
        if uid in self.units:
            unit = copy.deepcopy(self.units[uid].__dict__)
            unit['creator_id'] = unit['creator'].uid
            del unit['creator']
            unit['address'] = unit['address'].__dict__
            return unit
        else:
            return None

class User:

    def __init__(self, uid, email, first_name, last_name):
        self.uid = uid
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

class Unit:

    def __init__(self, uid, address, num_rooms, num_bathrooms, sqft, creator):
        self.uid = uid
        self.address = address
        self.num_rooms = num_rooms
        self.num_bathrooms = num_bathrooms
        self.sqft = sqft
        self.creator = creator

class Address:

    def __init__(self, block, street, pin, city, country, lat, lng):
        self.block_number = block
        self.street_name = street
        self.postal_code = pin
        self.city = city
        self.country = country
        self.coordinates = (lat, lng)
