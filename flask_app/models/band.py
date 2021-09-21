from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models.user import User

class Band():

    def __init__(self, data):
        self.id = data['id']
        self.band_name = data['band_name']
        self.music_genre = data['music_genre']
        self.home_city = data['home_city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.founder = None

    @classmethod
    def create_band(cls, data):
        query = 'INSERT INTO bands (band_name, music_genre, home_city, founder_id) VALUES (%(band_name)s, %(music_genre)s, %(home_city)s, %(founder_id)s);'

        connection = connectToMySQL('band_together_exam')
        return connection.query_db(query, data)

    @classmethod
    def get_all_bands(cls):
        query = "SELECT * FROM bands JOIN users ON users.id = bands.founder_id;"

        connection = connectToMySQL('band_together_exam')
        results = connection.query_db(query)

        bands = []

        for result in results:
            band = cls(result)
            user_data = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at']
            }
            band.founder = User(user_data)
            bands.append(band)

        return bands

    @classmethod
    def get_band_by_id(cls, data):
        query = 'SELECT * FROM bands JOIN users ON users.id = bands.founder_id WHERE bands.id = %(id)s;'

        connection = connectToMySQL('band_together_exam')
        results = connection.query_db(query, data)

        if len(results) == 0:
            print('No band with that ID')
            return False

        else:
            result = results[0]
            band = cls(result)
            user_data = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at']
            }
            band.founder = User(user_data)
            return band

    @classmethod
    def update_band(cls, data):
        query = 'UPDATE bands SET band_name=%(band_name)s, music_genre=%(music_genre)s, home_city=%(home_city)s WHERE id = %(band_id)s;'

        connection = connectToMySQL('band_together_exam')
        connection.query_db(query, data)

    @classmethod
    def delete_band(cls, data):
        query = 'DELETE FROM bands WHERE id = %(id)s;'

        connection = connectToMySQL('band_together_exam')
        connection.query_db(query, data)

    @staticmethod
    def validate_band(data):
        is_valid = True

        if len(data['band_name']) < 2 or len(data['band_name']) > 255:
            is_valid = False
            flash('Band name must be between 2 and 255 characters long.')

        if len(data['music_genre']) < 2 or len(data['music_genre']) > 255:
            is_valid = False
            flash('Music genre must be between 2 and 255 characters long.')

        if data['home_city'] == '' or len(data['home_city']) > 255:
            is_valid = False
            flash('Please enter a home city! up to 255 character long.')

        return is_valid
