from sqlite3 import Connection, Cursor

from scripts.game import PokemonFilters

class PokemonDatabase:
    
    def __init__(self, connection:Connection, cursor:Cursor):
        self.connection = connection
        self.cur = cursor


    # GET

    def get_pokemon(self, pokemon_id:int) -> dict:
        self.cur.execute(
            f"""
            SELECT 
                pokemon_id,
                pokemon_name,
                form_name,
                generation,
                evolves_from_pokemon_id,
                first_type,
                second_type,
                first_ability,
                second_ability,
                hidden_ability,
                is_mythical,
                is_legendary,
                is_sublegendary,
                is_powerhouse,
                is_fully_evolved,
                has_mega,
                has_gmax,
                sprite
            FROM pokemon 
            WHERE pokemon_id={pokemon_id}
            """
        )
        rows = self.cur.fetchall()
        if not rows:
            return {}

        pokemon = rows[0]
        pokemon_dic = {
            'pokemon_id' : pokemon[0],
            'pokemon_name' : pokemon[1],
            'form_name' : pokemon[2],
            'generation' : pokemon[3],
            'evolves_from_pokemon_id' : pokemon[4],
            'first_type' : pokemon[5],
            'second_type' : pokemon[6],
            'first_ability' : pokemon[7],
            'second_ability' : pokemon[8],
            'hidden_ability' : pokemon[9],
            'is_mythical' : pokemon[10],
            'is_legendary' : pokemon[11],
            'is_sublegendary' : pokemon[12],
            'is_powerhouse' : pokemon[13],
            'is_fully_evolved' : pokemon[14],
            'has_mega' : pokemon[15],
            'has_gmax' : pokemon[16],
            'sprite' : pokemon[17]
        }
        return pokemon_dic

    def get_pokemon_name(self, pokemon_id:int):
        self.cur.execute(f"SELECT pokemon_name, form_name FROM pokemon WHERE pokemon_id={pokemon_id}")
        rows = self.cur.fetchall()
        if rows:
            pokemon_name, form_name = rows[0]
            return (pokemon_name, form_name)
        else:
            return None

    def get_pokemon_ids(self, filters:PokemonFilters, additional_filters:dict=None) -> list:
        query = f"""
        SELECT pokemon_id 
        FROM pokemon
        WHERE 
        generation<={filters.generation}"""

        if filters.fully_evolved:
            query += ' AND is_fully_evolved'

        conditions = [
            ('is_mythical', filters.mythical),
            ('is_legendary', filters.legendary),
            ('is_sublegendary', filters.sublegendary),
            ('is_powerhouse', filters.powerhouse)
        ]
        cond_list = [ x[0] for x in conditions if x[1] ]

        if filters.others:
            cond_list.append("(NOT is_mythical AND NOT is_legendary AND NOT is_sublegendary AND NOT is_powerhouse)")

        if len(cond_list)>0:
            cond = ' OR '.join(cond_list)
            query += f' AND ({cond})'

        # filtros adicionales
        if additional_filters:
            if additional_filters.get('has_mega'):
                query += ' AND has_mega'
            pokemon_type = additional_filters.get('pokemon_type')
            if pokemon_type:
                query += f' AND (first_type=\'{pokemon_type}\' OR second_type=\'{pokemon_type}\')'

        self.cur.execute(query)
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]
