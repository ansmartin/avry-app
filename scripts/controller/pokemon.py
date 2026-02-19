import random

from scripts.db import DatabaseModel
from scripts.controller.abilities import AbilitiesController
from scripts.game import GameSession

class PokemonController:

    def __init__(self, db:DatabaseModel):
        self.db_pokemon = db.pokemon
        self.abilities = AbilitiesController(db)


    # GET

    def get_pokemon_fullname(self, pokemon_id:int) -> str:
        pokemon = self.db_pokemon.get_pokemon_name(pokemon_id)

        pokemon_name = pokemon[0]
        form_name = pokemon[1]

        if form_name is not None:
            pokemon_name += f' ({form_name})'

        return pokemon_name

    def get_random_pokemon(self, game:GameSession, save:bool=False) -> dict:
        # pasar filtros para obtener lista de ids
        pokemon_ids = self.db_pokemon.get_pokemon_ids(game.filters)

        # quitar pokemon ya obtenidos previamente
        obtained_pokemon_list = [ x[0] for x in game.pokemon_box._list ]
        pokemon_ids = list(set(pokemon_ids) - set(obtained_pokemon_list))
        if not pokemon_ids:
            return {}

        # obtener pokemon aleatorio
        n = random.randint(0, len(pokemon_ids)-1)
        pokemon_id = pokemon_ids[n]

        pokemon = self.db_pokemon.get_pokemon(pokemon_id)
        if not pokemon:
            return {}

        # añadir habilidad random
        if game.filters.random_ability:
            ability_id = self.abilities.get_random_ability(game.filters.generation)
            pokemon['random_ability_id'] = ability_id
            pokemon['random_ability_name'] = self.abilities.get_ability_name(ability_id)
        
        """ 
        # guardar pokemon
        if save:
            self.db.rolls.insert_pokemon(
                game.game_id,
                pokemon_id,
                pokemon.get('random_ability_id')
            )
        """
        return pokemon
