from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


class User():

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.band = None


    @classmethod
    def create_user(clas, data):

        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        connection = connectToMySQL('band_together_exam')

        user_id = connection.query_db(query, data)
        print("*"*80, user_id)
        return user_id

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('band_together_exam').query_db(query,data)

        if len(result) != 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all_users(cls, data):
        query = "SELECT * FROM users"

        connection = connectToMySQL('band_together_exam')
        results = connection.query_db(query, data)
        
        if len(results) == 0:
            print('No user with that ID')
            return False

        else:
            result = results[0]
            user = cls(result)
            band_data = {
                'id': result['bands.id'],
                'band_name': result['band_name'],
                'music_genre': result['music_genre'],
                'home_city': result['home_city'],
                'created_at': result['bands.created_at'],
                'updated_at': result['bands.updated_at']
            }
        user = User(band_data)
        return user

    @classmethod
    def get_user_id(cls, data):
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
            band.founder_id = user.User(user_data)
            return band

    @staticmethod
    def validate_user(data):
        is_valid = True

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(data['first_name']) == 0 or len(data['first_name']) > 255:
            is_valid = False
            flash("First name must be at least 2 characters long.")

        if len(data['last_name']) == 0 or len(data['last_name']) > 255:
            is_valid = False
            flash("Last name must be at least 2 characters long.")

        if not email_regex.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        
        if  User.get_user_by_email(data):
            is_valid = False
            flash('Email address is already in use!')

        if len(data['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters long")
        
        if data['password'] != data['confirm_password']:
            is_valid = False
            flash("Password and confirm password must match")

        return is_valid