from scripts.database.cards import CardsDatabase

class CardsController:

    def __init__(self, connection, cursor):
        self.db_cards = CardsDatabase(connection, cursor)


    # GET

    def get_used_cards(self, game_id:int) -> dict:
        used_cards = {
            tag : uses
            for tag, uses in self.db_cards.get_used_cards(game_id)
        }
        return used_cards