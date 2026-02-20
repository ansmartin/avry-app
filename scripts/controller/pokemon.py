import random

from scripts.db import DatabaseModel
from scripts.controller.abilities import AbilitiesController
from scripts.game import GameSession, PokemonFilters

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

    def get_pokemon_name_and_ability(self, pokemon_id:int, ability_id:int):
        tuple = (
            pokemon_id,
            self.get_pokemon_fullname(pokemon_id),
            ability_id, 
            self.abilities.get_ability_name(ability_id)
        )
        return tuple


    def get_pokemon(self, pokemon_id:int, filters:PokemonFilters=None) -> dict:
        pokemon = self.db_pokemon.get_pokemon(pokemon_id)
        if not pokemon:
            return {}

        # añadir habilidad random
        if filters is not None:
            if filters.random_ability:
                ability_id = self.abilities.get_random_ability(filters.generation)
                pokemon['random_ability_id'] = ability_id
                pokemon['random_ability_name'] = self.abilities.get_ability_name(ability_id)

        return pokemon

    def get_random_pokemon(self, game:GameSession, additional_filters:dict=None) -> dict:
        # pasar filtros para obtener lista de ids
        pokemon_ids = self.db_pokemon.get_pokemon_ids(game.filters, additional_filters)

        # quitar pokemon ya obtenidos previamente
        obtained_pokemon_list = [ x[0] for x in game.pokemon_box._list ]
        pokemon_ids = list(set(pokemon_ids) - set(obtained_pokemon_list))
        if not pokemon_ids:
            return {}

        # obtener pokemon aleatorio
        n = random.randint(0, len(pokemon_ids)-1)
        pokemon_id = pokemon_ids[n]

        pokemon = self.get_pokemon(pokemon_id, game.filters)

        return pokemon
