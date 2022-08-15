# users.py

from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models.card import Card
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
import bcrypt


bcrypt = Bcrypt(app)


@app.route('/')
@app.route('/login_and_registration')
def get_login_and_registration_page():
    return render_template('login_and_registration.html')


@app.route('/process_registration', methods=['POST'])
def post_registration_info():
    if not User.validate_registration(registering_user=request.form):
        return redirect('/')
    data_user = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'username' : request.form['username'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']).decode('utf-8'),
        'birthday': request.form['birthday'],
        'get_birthday': request.form['get_birthday'],
        'get_christmas': request.form['get_christmas'],
        'get_newsletter': request.form['get_newsletter'],
        'invitation_code': request.form['invitation_code']
    }
    User.add_new_user(data_user=data_user)
    username_dict = {
        'username': data_user['username']
    }
    logged_in_user = User.get_a_user_by_username(username_dict=username_dict)
    session['user_id'] = logged_in_user.user_id
    session['username'] = logged_in_user.username
    session['first_name'] = logged_in_user.first_name
    return redirect('/cards')

@app.route('/process_login', methods=['POST'])
def post_login_info():
    if not User.validate_login(request.form):
        return redirect('/')
    logged_in_user = User.get_a_user_by_username(username_dict=request.form)
    session['user_id'] = logged_in_user.user_id
    session['username'] = logged_in_user.username
    session['first_name'] = logged_in_user.first_name
    return redirect('/cards')

@app.route('/users')
def get_all_users():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    list_of_all_users = User.get_all_users()
    return render_template('collectors.html', list_of_all_users=list_of_all_users)


@app.route('/your_cards')
def get_a_single_users_favorites():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    user_dict = {
        'username': session['username'],
        'user_id': session['user_id']
    }
    one_user = Card.get_a_users_favorite_cards_objects(user_dict=user_dict)
    return render_template('your_cards.html', one_user=one_user)


@app.route('/users/by_card/<int:card_id>')
def get_users_by_card(card_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    card_dict = {
        'card_id': card_id
    }
    favorite_card = User.get_a_cards_fans(card_dict)
    return render_template('card.html', favorite_card=favorite_card)

@app.route('/cards/others_cards/<username>')
def get_other_users_cards(username):
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    user_dict = {
        'username': username,
        'user_id': session['user_id']
    }
    one_user = Card.get_another_users_favorite_cards(user_dict=user_dict)
    return render_template('user.html', one_user=one_user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')