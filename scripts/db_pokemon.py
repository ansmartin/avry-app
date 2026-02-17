from sqlite3 import Connection, Cursor
import random

class PokemonDatabase:
    
    def __init__(self, connection:Connection, cursor:Cursor):
        self.connection = connection
        self.cur = cursor


    # pokemon

    def get_pokemon_fullname(self, pokemon_id:int) -> str:
        self.cur.execute(f"SELECT pokemon_name, form_name FROM pokemon WHERE pokemon_id={pokemon_id}")
        rows = self.cur.fetchall()
        pokemon = rows[0]

        species_name = pokemon[0]
        form_name = pokemon[1]

        name = species_name
        if form_name is not None:
            name += f' ({form_name})'

        return name


    # abilities

    def get_ability_name(self, ability_id:int) -> str|None:
        if ability_id is None:
            return None

        self.cur.execute(f"SELECT ability_name FROM abilities WHERE ability_id={ability_id}")
        rows = self.cur.fetchall()
        if rows:
            return rows[0][0]
        else:
            return None

    def get_random_ability(self, generation:int) -> int|None:
        self.cur.execute(f"SELECT ability_id FROM abilities WHERE generation<={generation}")
        rows = self.cur.fetchall()
        if not rows:
            return None

        abilities_ids = [ x[0] for x in rows ]
        n = random.randint(0, len(abilities_ids)-1)
        ability = abilities_ids[n]
        return ability
