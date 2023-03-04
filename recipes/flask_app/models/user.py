
from flask_app.config.mysqlconnection import connectToMySQL

import re

from flask import flash

import flask_app.models.recipe

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = 'user_and_recipes'

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def show_all(cls):
        query = 'SELECT * FROM users'
        results = connectToMySQL('user_and_recipes').query_db(query)
        all_users = []
        for row in results:
            all_users.append(cls(row))
        return all_users

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)'
        result = connectToMySQL('user_and_recipes').query_db(query, data)
        return result

    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM users WHERE id = %(id)s'
        result  = connectToMySQL('user_and_recipes').query_db(query,data)
        print(result)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_onewith_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result  = connectToMySQL(cls.db).query_db(query,data)
        if result:
            return cls(result[0])
        return False


    @staticmethod
    def validate(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result  = connectToMySQL(User.db).query_db(query,user)
        if len(user['first_name']) < 2 :
            flash('First name too short')
            is_valid = False
        if len(user['last_name']) < 2 :
            flash('Last name too short')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be atleast 8 characters')
            is_valid = False
        if user['password'] != user['confirm']:
            flash('Passwords do not match')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("User already taken")
            is_valid = False
        return is_valid
