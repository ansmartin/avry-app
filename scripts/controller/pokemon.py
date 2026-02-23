import random

from scripts.database.pokemon import PokemonDatabase
from scripts.controller.abilities import AbilitiesController
from scripts.game import GameSession

class PokemonController:

    def __init__(self, connection, cursor):
        self.db_pokemon = PokemonDatabase(connection, cursor)
        self.abilities = AbilitiesController(connection, cursor)


    # GET

    def get_pokemon_fullname(self, pokemon_id:int) -> str:
        pokemon = self.db_pokemon.get_pokemon_name(pokemon_id)

        pokemon_name = pokemon[0]
        form_name = pokemon[1]

        if form_name is not None:
            pokemon_name += f' ({form_name})'

        return pokemon_name

    def get_sprite_link(self, sprite_number:int):
        return f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{sprite_number}.png'

    def get_pokemon_important_data(self, pokemon_id:int, ability_id:int=None) -> dict:
        pokemon = self.db_pokemon.get_pokemon(pokemon_id)

        data = {
            'pokemon_name' : self.get_pokemon_fullname(pokemon_id),
            'random_ability' : self.abilities.get_ability_name(ability_id),
            'sprite_link' : self.get_sprite_link(pokemon.get('sprite'))
        }
        return data


    def get_pokemon(self, pokemon_id:int, random_ability:bool=False, ability_generation:int=0) -> dict:
        pokemon = self.db_pokemon.get_pokemon(pokemon_id)
        if not pokemon:
            return {}

        # añadir habilidad random
        if random_ability:
            pokemon['random_ability_id'] = self.abilities.get_random_ability(ability_generation)

        return pokemon


    def get_list_of_elegible_pokemon_ids(self, game:GameSession, additional_filters:dict=None) -> list:
        # pasar filtros para obtener conjunto de pokemon posibles
        filtered_pokemon_ids = self.db_pokemon.get_pokemon_ids(game.filters, additional_filters)

        # quitar pokemon ya obtenidos previamente
        pokemon_ids = list(filtered_pokemon_ids - game.pokemon_box.box.keys())

        return pokemon_ids


    def get_random_pokemon(self, game:GameSession, additional_filters:dict=None) -> dict:
        pokemon_ids = self.get_list_of_elegible_pokemon_ids(game, additional_filters)
        if not pokemon_ids:
            return {}

        # obtener pokemon aleatorio
        n = random.randint(0, len(pokemon_ids)-1)
        pokemon_id = pokemon_ids[n]

        pokemon = self.get_pokemon(pokemon_id, game.filters.random_ability, game.filters.generation)

        return pokemon

    def get_multiple_random_pokemons(self, game:GameSession, quantity:int) -> list[dict]:
        pokemon_ids = self.get_list_of_elegible_pokemon_ids(game)
        if not pokemon_ids:
            return {}

        # desordenar
        random.shuffle(pokemon_ids)

        # devolver lista de pokemon aleatorios
        chosen_pokemon_ids = pokemon_ids[0:quantity]
        pokemon_list = [
            self.get_pokemon(pokemon_id, game.filters.random_ability, game.filters.generation)
            for pokemon_id in chosen_pokemon_ids
        ]

        return pokemon_list
