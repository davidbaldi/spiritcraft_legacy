from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Card:
    def __init__(self, db_card):
        self.card_id = db_card['card_id']
        self.name = db_card['name']
        self.type = db_card['type']
        self.card_set = db_card['card_set']
        self.expansion = db_card['expansion']
        self.release_date = db_card['release_date']
        self.description = db_card['description']
        self.is_editors_choice = db_card['is_editors_choice']
        self.is_players_pick = db_card['is_players_pick']
        self.is_collectable_only = db_card['is_collectable_only']
        self.status = db_card['status']
        self.quantity = db_card['quantity']
        self.is_horiztonal = db_card['is_horizontal']
        self.image_url = db_card['image_url']
        self.created_at = db_card['created_at']
        self.updated_at = db_card['updated_at']
        self.favorited_by = []
        # Leaving out "details" for now


    @classmethod
    def add_new_card(cls, data_dict):
        query = """
                INSERT INTO cards (name, type, card_set, expansion, release_date, description, is_editors_choice, is_players_pick, is_collectable_only, status, quantity, is_horizontal, image_url, created_at, updated_at)
                VALUES (
                    %(name)s,
                    %(type)s,
                    %(card_set)s,
                    %(expansion)s,
                    %(release_date)s,
                    %(description)s,
                    %(is_editors_choice)s,
                    %(is_players_pick)s,
                    %(is_collectable_only)s,
                    %(status)s,
                    %(quantity)s,
                    %(is_horizontal)s,
                    %(image_url)s,
                    NOW(),
                    NOW()
                    );
                """
        return connectToMySQL('spiritcraft').query_db(query, data_dict)

    @classmethod
    def get_a_single_card(cls, card_name_dict):
        query = """
                SELECT * FROM cards
                WHERE name = %(card_name)s;
                """
        one_card = connectToMySQL('spiritcraft').query_db(query, card_name_dict)
        instantiated_card = Card(one_card[0])
        return instantiated_card

    @classmethod
    def get_all_cards(cls):
        query = """
                SELECT * FROM cards;
                """
        all_cards = connectToMySQL('spiritcraft').query_db(query)
        instantiated_cards = []
        for one_card in all_cards:
            instantiated_cards.append(cls(one_card))
        return instantiated_cards

    @classmethod
    def get_all_cards_by_type_test(cls, card_dict):
        query = """
                SELECT * FROM cards
                WHERE type = %(type)s;
                """
        all_cards = connectToMySQL('spiritcraft').query_db(query, card_dict)
        instantiated_cards = []
        for one_card in all_cards:
            instantiated_cards.append(cls(one_card))
        return instantiated_cards

    @classmethod
    def is_card_favorited(cls, user_dict):
        query = """
                SELECT EXISTS (
                    SELECT * FROM cards
                    LEFT JOIN favorites ON favorites.card_id = cards.card_id
                    WHERE user_id = %(user_id)s
                    );
                """
        is_favorited = connectToMySQL('spiritcraft').query_db(query, user_dict)

    @classmethod
    def get_a_users_favorite_cards_ids(cls, user_dict):
        query = """
                SELECT * FROM users
                WHERE user_id = %(user_id)s;
                """
        row_containing_user = connectToMySQL('spiritcraft').query_db(query, user_dict)
        one_user = user.User(row_containing_user[0])
        query = """
                SELECT * FROM cards
                LEFT JOIN favorites ON favorites.card_id = cards.card_id
                LEFT JOIN users ON favorites.user_id = users.user_id
                WHERE favorites.user_id = %(user_id)s;
                """
        rows_of_cards = connectToMySQL('spiritcraft').query_db(query, user_dict)
        for favorite_card in rows_of_cards:
            card = Card(favorite_card)
            # one_user.favorite_cards.append(card)
            one_user.favorite_cards.append(card.card_id)
        return one_user

    @classmethod
    def get_a_users_favorite_cards_objects(cls, user_dict):
        query = """
                SELECT * FROM users
                WHERE user_id = %(user_id)s;
                """
        row_containing_user = connectToMySQL('spiritcraft').query_db(query, user_dict)
        one_user = user.User(row_containing_user[0])
        query = """
                SELECT * FROM cards
                LEFT JOIN favorites ON favorites.card_id = cards.card_id
                LEFT JOIN users ON favorites.user_id = users.user_id
                WHERE favorites.user_id = %(user_id)s;
                """
        rows_of_cards = connectToMySQL('spiritcraft').query_db(query, user_dict)
        for favorite_card in rows_of_cards:
            card = Card(favorite_card)
            # one_user.favorite_cards.append(card)
            one_user.favorite_cards.append(card)
        return one_user
    
    @classmethod
    def create_favorite(cls, favorite_dict):
        query = """
                INSERT INTO favorites (user_id, card_id)
                VALUES (%(user_id)s, %(card_id)s);
                """
        return connectToMySQL('spiritcraft').query_db(query, favorite_dict)
    
    @classmethod
    def delete_favorite(cls, favorite_dict):
        query = """
                DELETE FROM favorites
                WHERE user_id = %(user_id)s AND card_id = %(card_id)s
                """
        return connectToMySQL('spiritcraft').query_db(query, favorite_dict)


    # @classmethod
    # def get_all_cards_by_type(cls, card_type_dict):
    #     query = """
    #             SELECT * FROM cards
    #             WHERE type = %(type)s;
    #             """
    #     all_cards = connectToMySQL('spiritcraft').query_db(query, card_type_dict)
    #     instantiated_cards = []
    #     for one_card in all_cards:
    #         instantiated_cards.append(cls(one_card))
    #     return instantiated_cards

    @classmethod
    def get_all_cards_by_type(cls, card_type_dict):
        query = """
                SELECT * FROM cards
                WHERE type = %(type)s;
                """
        all_cards = connectToMySQL('spiritcraft').query_db(query, card_type_dict)
        instantiated_cards = []
        for one_card in all_cards:
            instantiated_cards.append(cls(one_card))
        return instantiated_cards
    
    # @classmethod
    # def get_other_users_cards(cls, user_dict):
    #     query = """
    #             SELECT * FROM cards
    #             LEFT JOIN favorites ON favorites.card_id = cards.card_id
    #             LEFT JOIN users ON favorites.user_id = users.user_id
    #             WHERE favorites.user_id = %(user_id)s;
    #             """
    #     rows_of_results = connectToMySQL('spiritcraft').query_db(query, user_dict)

    @classmethod
    def get_another_users_favorite_cards(cls, user_dict):
        query = """
                SELECT * FROM users
                WHERE username = %(username)s;
                """
        row_containing_user = connectToMySQL('spiritcraft').query_db(query, user_dict)
        # print(row_containing_user)
        one_user = user.User(row_containing_user[0])
        # print(one_user)
        query = """
                SELECT * FROM cards
                LEFT JOIN favorites ON favorites.card_id = cards.card_id
                LEFT JOIN users ON favorites.user_id = users.user_id
                WHERE favorites.user_id = %(user_id)s;
                """
        rows_of_cards = connectToMySQL('spiritcraft').query_db(query, user_dict)
        print(rows_of_cards)
        for favorite_card in rows_of_cards:
            card = Card(favorite_card)
            one_user.favorite_cards.append(card)
            print(one_user.favorite_cards)
        return one_user

    @classmethod
    def get_list_of_cards_for_update(cls):
        query = """
                SELECT * FROM cards;
                """
        rows_of_cards = connectToMySQL('spiritcraft').query_db(query)
        list_of_cards_for_update = []
        for card_as_row in rows_of_cards:
            list_of_cards_for_update.append(cls(card_as_row))
        return list_of_cards_for_update

    @classmethod
    def get_a_card_for_update(cls, card_id_dict):
        query = """
                SELECT * FROM cards
                WHERE card_id = %(card_id)s;
                """
        row_of_one_card = connectToMySQL('spiritcraft').query_db(query, card_id_dict)
        one_card = cls(row_of_one_card[0])
        return one_card

    @classmethod
    def update_a_card(cls, card_dict):
        query = """
                INSERT INTO cards (name, type, card_set, expansion, release_date, description, is_editors_choice, is_players_pick, is_collectable_only, status, quantity, is_horizontal, image_url, created_at, updated_at)
                VALUES (
                    %(name)s,
                    %(type)s,
                    %(card_set)s,
                    %(expansion)s,
                    %(release_date)s,
                    %(description)s,
                    %(is_editors_choice)s,
                    %(is_players_pick)s,
                    %(is_collectable_only)s,
                    %(status)s,
                    %(quantity)s,
                    %(is_horizontal)s,
                    %(image_url)s,
                    NOW(),
                    NOW()
                    );
                WHERE card_id = ;
                """
        return connectToMySQL('spiritcraft').query_db(query, card_dict)