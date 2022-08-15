# Everything here returns a user or users

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import card
from flask_app import app # Maybe
from flask_bcrypt import Bcrypt
from flask import flash, redirect
import bcrypt
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:

    db = 'spiritcraft'

    def __init__(self, db_user):
        self.user_id = db_user['user_id']
        self.email = db_user['email']
        self.password = db_user['password']
        self.username = db_user['username']
        self.first_name = db_user['first_name']
        self.last_name = db_user['last_name']
        self.created_at = db_user['created_at']
        self.updated_at = db_user['updated_at']
        self.favorite_cards = []
        # Leaving out "details" for now


    @classmethod
    def add_new_user(cls, data_user):
        query = """
                INSERT INTO users (
                                username,
                                password,
                                first_name,
                                last_name,
                                email,
                                birthday,
                                get_birthday,
                                get_christmas,
                                get_newsletter,
                                created_at,
                                updated_at
                                )
                VALUES (
                    %(username)s,
                    %(password)s,
                    %(first_name)s,
                    %(last_name)s,
                    %(email)s,
                    %(birthday)s,
                    %(get_birthday)s,
                    %(get_christmas)s,
                    %(get_newsletter)s,
                    NOW(),
                    NOW()
                    );
                """
        return connectToMySQL(cls.db).query_db(query, data_user)


    @classmethod
    def get_a_user_by_username(cls, username_dict):
        query = """
                SELECT * FROM users
                WHERE username = %(username)s;
                """
        results = connectToMySQL(cls.db).query_db(query, username_dict)
        if results:
            logged_in_user = cls(results[0])
            return logged_in_user


    @classmethod
    def get_all_users(cls):
        query = """
                SELECT * FROM users;
                """
        rows_of_results = connectToMySQL(cls.db).query_db(query)
        list_of_all_users = []
        for user in rows_of_results:
            new_user = User(user)
            list_of_all_users.append(new_user)
        return list_of_all_users


    # Salvaged!
    @classmethod
    def get_a_cards_fans(cls, card_dict):
        query = """
                SELECT * FROM cards
                WHERE card_id = %(card_id)s;
                """
        row_containing_card = connectToMySQL(cls.db).query_db(query , card_dict)
        favorite_card = card.Card(row_containing_card[0])
        query = """
                SELECT * FROM users
                LEFT JOIN favorites ON favorites.user_id = users.user_id
                LEFT JOIN cards ON favorites.card_id = cards.card_id
                WHERE favorites.card_id = %(card_id)s;
                """
        rows_of_users = connectToMySQL(cls.db).query_db(query , card_dict)
        for single_user in rows_of_users:
            user = User(single_user)
            favorite_card.favorited_by.append(user)
        return favorite_card


    @staticmethod
    def validate_registration(registering_user):
        is_valid = True
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
                """
        results = connectToMySQL(User.db).query_db(query, registering_user)
        if results:
            flash("Email already taken. Choose another!", 'registration_error')
            is_valid = False
        if len(registering_user['first_name']) < 3:
            flash("First name must be at least 3 characters!", 'registration_error')
            is_valid = False
        if len(registering_user['last_name']) < 3:
            flash("Last name must be at least 3 characters!", 'registration_error')
            is_valid = False
        # Make sure to use 'novalidate' in forms
        # If time, detail all the registration error categories
        if not EMAIL_REGEX.match(registering_user['email']):
            flash("Invalid email format!", 'registration_error')
            is_valid = False
        if len(registering_user['password']) < 1:
            flash("Password must be at least 1 character!", 'registration_error')
            is_valid = False
        if registering_user['password'] != registering_user['confirm_password']:
            flash("Passwords don't match!", 'registration_error')
            is_valid = False
        if registering_user['invitation_code'] != 'CodingDojoBonus':
            flash("Sorry, you must be invited to join!", 'registration_error')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(username_dict):
        is_valid = True
        query = """
                SELECT * FROM users
                WHERE username = %(username)s;
                """
        results = connectToMySQL(User.db).query_db(query, username_dict)
        if not results:
            is_valid = False
            flash("Email not found!", 'login_error')
            # Yes?
            redirect('/')
        logged_in_user = User(results[0])
        if not bcrypt.check_password_hash(logged_in_user.password, username_dict['password']):
            is_valid = False
            flash("Invalid password!", 'login_error')
            # Yes?
            redirect('/')
        return is_valid