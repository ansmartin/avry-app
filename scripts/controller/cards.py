from scripts.db import DatabaseModel

class CardsController:

    def __init__(self, db:DatabaseModel):
        self.db_cards = db.cards


    # GET

    def get_used_cards(self, game_id:int) -> dict:
        used_cards = {
            tag : uses
            for tag, uses in self.db_cards.get_used_cards(game_id)
        }
        return used_cards