from sqlite3 import Connection, Cursor

class RollsDatabase:
    
    def __init__(self, connection:Connection, cursor:Cursor):
        self.connection = connection
        self.cur = cursor


    # GET

    def get_rolls(self, game_id:int) -> list[(int,int)]:
        self.cur.execute(f"SELECT pokemon_id, ability_id FROM pokemon_box WHERE game_id={game_id}")
        rows = self.cur.fetchall()
        return rows


    # INSERT

    def insert_roll(self, game_id:int, pokemon_id:int, ability_id:int=None):
        if ability_id is None:
            ability_id = 'NULL'

        self.cur.execute(
            f"""
            INSERT INTO pokemon_box 
            (game_id, pokemon_id, ability_id)
            VALUES ({game_id}, {pokemon_id}, {ability_id})
            """
        )
        self.connection.commit()


    # DELETE

    def delete_rolls(self, game_id:int):
        self.cur.execute(f"DELETE FROM pokemon_box WHERE game_id={game_id}")
        self.connection.commit()

    def delete_roll(self, game_id:int, pokemon_id:int):
        self.cur.execute(f"DELETE FROM pokemon_box WHERE game_id={game_id} AND pokemon_id={pokemon_id}")
        self.connection.commit()


    # UPDATE
