from scripts.db import DatabaseModel
from scripts.controller.pokemon import PokemonController

class RollsController:

    def __init__(self, db:DatabaseModel):
        self.db_rolls = db.rolls


    # INSERT

    def insert_roll(self, game_id:int, pokemon:dict):
        self.db_rolls.insert_roll(
            game_id,
            pokemon.get('id'),
            pokemon.get('random_ability_id')
        )