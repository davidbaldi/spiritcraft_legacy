# cards.py

from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models.card import Card
from flask_app.models.user import User


@app.route('/cards')
def get_all_cards_for_display():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    user_dict = {
        'user_id': session['user_id']
    }
    instantiated_cards = Card.get_all_cards()
    users_favorites = Card.get_a_users_favorite_cards_ids(user_dict)
    return render_template('cards.html', instantiated_cards=instantiated_cards, users_favorites=users_favorites)

# This is to test out the by-type, favorited-or-not display
@app.route('/cards/types/<card_type>')
def get_all_cards_for_display_by_type(card_type):
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    user_dict = {
        'user_id': session['user_id']
    }
    card_dict = {
        'type': card_type
    }
    instantiated_cards = Card.get_all_cards_by_type_test(card_dict)
    users_favorites = Card.get_a_users_favorite_cards_ids(user_dict)
    return render_template('cards.html', instantiated_cards=instantiated_cards, users_favorites=users_favorites)


@app.route('/cards/single_card/<card_name>')
def get_a_single_card(card_name):
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    card_name_dict = {
        'card_name': card_name
    }
    instantiated_card = Card.get_a_single_card(card_name_dict=card_name_dict)
    return render_template('card.html', card=instantiated_card)


@app.route('/cards/<username>')
def get_cards_by_user(username):
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    user_dict = {
        'user_id': session['user_id']
    }
    one_user = Card.get_a_users_favorites(user_dict)
    return render_template('user.html', one_user=one_user)


@app.route('/cards/add_card')
def get_new_card_form():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    if session['user_id'] != 14:
        flash("You must be an admin to view that page!", 'not_an_admin_error')
        return redirect('/')
    return render_template('add_new_card_form.html')


@app.route('/cards/process_new_card', methods=['POST'])
def post_new_card_info():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    Card.add_new_card(data_dict=request.form)
    return redirect('/cards/add_card')


@app.route('/cards/process_card_like/<int:card_id>')
def process_card_like(card_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    user_dict = {
        'user_id': session['user_id']
    }
    one_user = Card.get_a_users_favorite_cards_ids(user_dict)
    print(one_user.favorite_cards)
    # if card_id in one_user.favorite_cards:
    #     flash("You already faved that card!", 'already_faved_error')
    #     return redirect('/your_cards')
    favorite_dict = {
        'user_id': session['user_id'],
        'card_id': card_id
    }
    Card.create_favorite(favorite_dict)
    return redirect('/cards')


@app.route('/cards/process_card_unlike/<int:card_id>')
def process_card_unlike(card_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    favorite_dict = {
        'user_id': session['user_id'],
        'card_id': card_id
    }
    Card.delete_favorite(favorite_dict=favorite_dict)
    user_dict = {
        'user_id': session['user_id']
    }
    instantiated_cards = Card.get_all_cards()
    users_favorites = Card.get_a_users_favorite_cards_ids(user_dict)
    # return render_template('cards.html', instantiated_cards=instantiated_cards, users_favorites=users_favorites)
    return render_template('cards.html', instantiated_cards=instantiated_cards, users_favorites=users_favorites)


@app.route('/your_cards')
def display_all_your_cards():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    user_dict = {
        'user_id': session['user_id']
    }
    one_user = Card.get_a_users_favorite_cards_objects(user_dict)
    return render_template('your_cards.html', one_user)


# @app.route('/cards/types/<type>')
# def display_cards_by_type(type):
#     if 'user_id' not in session:
#         flash("You must be logged in to view this page!", 'must_be_logged_in_error')
#         return redirect('/')
#     card_type_dict = {
#         'type': type,
#         'user_id': session['user_id']
#     }
#     instantiated_cards = Card.get_all_cards_by_type(card_type_dict)
#     return render_template('cards_by_type.html', instantiated_cards=instantiated_cards)

@app.route('/updates')
def display_cards_for_update():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    if session['user_id'] != 14:
        flash("You must be an admin to view that page!", 'not_an_admin_error')
        return redirect('/')
    list_of_cards_for_update = Card.get_list_of_cards_for_update()
    return render_template('list_of_cards_for_update.html', list_of_cards_for_update=list_of_cards_for_update)

@app.route('/updates/<int:card_id>')
def get_card_update_form(card_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    if session['user_id'] != 14:
        flash("You must be an admin to view that page!", 'not_an_admin_error')
        return redirect('/')
    card_id_dict = {
        'card_id': card_id
    }
    one_card = Card.get_a_card_for_update(card_id_dict)
    return render_template('update_card_form.html', one_card=one_card)

@app.route('/updates/process_update', methods=['POST'])
def process_card_update():
    if 'user_id' not in session:
        flash("You must be logged in to view this page!", 'must_be_logged_in_error')
        return redirect('/')
    if session['user_id'] != 14:
        flash("You must be an admin to view that page!", 'not_an_admin_error')
        return redirect('/')
    Card.update_a_card(card_dict=request.form)
    return redirect('/updates')