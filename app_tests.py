import app
import json
import unittest

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        ## Assumes create_user works to spec
        self.user_one = {
            'email': 'jane_doe@example.com',
            'first_name': 'Jane',
            'last_name': 'Doe'
        }
        self.user_two = {
            'email': 'test.user@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user_three = {
            'email': 'thirduser@example.com',
            'first_name': 'Ender',
            'last_name': 'Third'
        } 
        res_one = self.app.post('/api/createuser', data=json.dumps(self.user_one))
        res_two = self.app.post('/api/createuser', data=json.dumps(self.user_two))
        res_three = self.app.post('/api/createuser', data=json.dumps(self.user_three))
        self.user_one_id = json.loads(res_one.data)['user_id']
        self.user_two_id = json.loads(res_two.data)['user_id']
        self.user_three_id = json.loads(res_three.data)['user_id']
        ## Assumes create unit works to spec
        self.unit_one = {
            'creator_id': self.user_two_id,
            'address': {
                'block_number': '95',
                'street_name': 'Orchard Road',
                'postal_code': '149211',
                'city': 'Singapore',
                'country': 'Singapore',
                'coordinates': ['1.3', '103.8']
            },
            'num_rooms': 4,
            'num_bathrooms': 3,
            'sqft': 1500
        }
        self.unit_two = {
            'creator_id': self.user_two_id,
            'address': {
                'block_number': '89A',
                'street_name': 'Somerset Road',
                'postal_code': '142311',
                'city': 'Kuala Lumpur',
                'country': 'Malaysia',
                'coordinates': ['10', '103.8']
            },
            'num_rooms': 2,
            'num_bathrooms': 1,
            'sqft': 600
        }
        self.unit_three = {
            'creator_id': self.user_two_id,
            'address': {
                'block_number': '34',
                'street_name': 'Clementi Road',
                'postal_code': '121212',
                'city': 'Singapore',
                'country': 'Singapore',
                'coordinates': ['1.3','103.8']
            },
            'num_rooms': 3,
            'num_bathrooms': 3,
            'sqft': 1200
        }
        res_unit_one = self.app.post('/api/createunit', data=json.dumps(self.unit_one))
        res_unit_two = self.app.post('/api/createunit', data=json.dumps(self.unit_two))
        res_unit_three = self.app.post('/api/createunit', data=json.dumps(self.unit_three))
        self.unit_one_id = json.loads(res_unit_one.data)['unit_id']
        self.unit_two_id = json.loads(res_unit_two.data)['unit_id']
        self.unit_three_id = json.loads(res_unit_three.data)['unit_id']
    
    #def tearDown(self):   

    def test_create_user(self):
        new_user = {
            'email': 'john.doe@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        res = self.app.post('/api/createuser', data=json.dumps(new_user))
        user_id = json.loads(res.data)['user_id']
        assert user_id is not None

    def test_get_user(self):
        res = self.app.get('/api/user/' + str(self.user_one_id))
        db_user = json.loads(res.data)
        assert db_user['email'] == self.user_one['email']
        assert db_user['first_name'] == self.user_one['first_name']
        assert db_user['last_name'] == self.user_one['last_name']

    def test_update_user(self):
        updated_user_two = {
            'email': 'new_test_user@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        res_updated = self.app.post('/api/user/' + str(self.user_two_id), data=json.dumps(updated_user_two))
        ## Depends on get
        assert json.loads(res_updated.data)['success'] is True
        res_new = self.app.get('/api/user/' + str(self.user_two_id))
        db_user = json.loads(res_new.data)
        assert db_user['email'] == updated_user_two['email']
        self.user_two = updated_user_two

    def test_delete_user(self):
        res_delete = self.app.delete('/api/user/' + str(self.user_three_id))
        assert json.loads(res_delete.data)['success'] is True    
        res = self.app.get('/api/user/' + str(self.user_three_id))
        assert res.status_code == 404   
 
    def test_create_unit(self):
        new_unit = {
            'creator_id': self.user_one_id,
            'address': {
                'block_number': '71',
                'street_name': 'Diagon Alley',
                'postal_code': '100101',
                'city': 'Singapore',
                'country': 'Singapore',
                'coordinates': ['1.3','103.8']
            },
            'num_rooms': 3,
            'num_bathrooms': 1,
            'sqft': 700
        }
        res = self.app.post('/api/createunit', data=json.dumps(new_unit))
        unit_id = json.loads(res.data)['unit_id']
        assert unit_id is not None
    
    def test_get_unit(self):
        res = self.app.get('/api/unit/' + str(self.unit_one_id))
        db_unit = json.loads(res.data)
        assert db_unit is not None
        for key in self.unit_one:
            assert db_unit[key] == self.unit_one[key]
    
    def test_update_unit(self):
        updated_unit_two = {
            'creator_id': self.user_two_id,
            'address': {
                'block_number': '89A',
                'street_name': 'Somerset Road',
                'postal_code': '142311',
                'city': 'Kuala Lumpur',
                'country': 'China',
                'coordinates': ['10','103.8']
            },
            'num_rooms': 2,
            'num_bathrooms': 1,
            'sqft': 650
        } 
        res_updated = self.app.post('/api/unit/' + str(self.unit_two_id), data=json.dumps(updated_unit_two))
        ## Depends on get
        assert json.loads(res_updated.data)['success'] is True
        res_new = self.app.get('/api/unit/' + str(self.unit_two_id))
        db_unit = json.loads(res_new.data)
        for key in updated_unit_two:
            assert db_unit[key] == updated_unit_two[key]
        self.unit_two = updated_unit_two

    def test_delete_unit(self):
        res_delete = self.app.delete('/api/unit/' + str(self.unit_three_id))
        assert json.loads(res_delete.data)['success'] is True    
        res = self.app.get('/api/unit/' + str(self.unit_three_id))
        assert res.status_code == 404

    def test_get_user_by_email(self):
        res = self.app.get('/api/user-email/' + self.user_one['email'])
        db_user = json.loads(res.data)
        assert db_user['email'] == self.user_one['email']
        assert db_user['first_name'] == self.user_one['first_name']
        assert db_user['last_name'] == self.user_one['last_name']

    def test_get_all_users(self):
        res = self.app.get('/api/users')
        db_user_list = json.loads(res.data)['data']
        #print db_user_list[:3]
        assert len(db_user_list) >= 1

    def test_get_user_units(self):
        res = self.app.get('/api/user-units/' + self.user_two_id)
        db_unit_list = json.loads(res.data)['data']
        #print db_unit_list[:3]
        assert len(db_unit_list)

if __name__ == '__main__':
    unittest.main()
