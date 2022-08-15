# [ ] Favorite a card
# [ ] Unfavorite a card

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.card import Card
from flask_app.models.user import User


class Favorite:
    def __init__(self, db_favorite):
        self.user_id = db_favorite['user_id']
        self.card_id = db_favorite['card_id']


    @classmethod
    # 'data_dict' is too generic a name!
    def favorite_a_card(cls, data_dict):
        query = """
                INSERT INTO favorites (user_id, card_id)
                VALUES (%(user_id)s, %(card_id)s);
                """
        return connectToMySQL('spiritcraft').query_db(query, data_dict)


    @classmethod
    # 'data_dict' is too generic a name!
    def unfavorite_a_card(cls, data_dict):
        query = """"""
        return connectToMySQL('spiritcraft').query_db(query, data_dict)