from sqlite3 import Connection, Cursor

from scripts.db_users import UsersDatabase
from scripts.db_games import GamesDatabase
from scripts.db_rolls import RollsDatabase
from scripts.db_cards import CardsDatabase
from scripts.db_pokemon import PokemonDatabase


class DatabaseManager:
    
    def __init__(self, connection:Connection):
        self.connection = connection
        self.cur = self.connection.cursor()

        self.users = UsersDatabase(self.connection, self.cur)
        self.games = GamesDatabase(self.connection, self.cur)
        self.rolls = RollsDatabase(self.connection, self.cur)
        self.cards = CardsDatabase(self.connection, self.cur)
        self.pokemon = PokemonDatabase(self.connection, self.cur)


    # GET

    def get_table(self, table:str) -> list:
        self.cur.execute(f"SELECT * FROM {table}")
        rows = self.cur.fetchall()
        return rows

    def get_all_tables(self) -> dict:
        tables = ['users', 'games', 'pokemon_box', 'used_cards']
        dic_tables = {}
        for table in tables:
            rows = self.get_table(table)
            dic_tables[table] = rows
        return dic_tables

    def get_table_length(self, table:str) -> list:
        self.cur.execute(f"SELECT COUNT(*) FROM {table}")
        rows = self.cur.fetchall()
        size = rows[0][0]
        return size


    # INSERT


    # DELETE

    def delete(self, table:str, column:str, value):
        self.cur.execute(f"DELETE FROM {table} WHERE {column}={value}")
        self.connection.commit()


    # UPDATE

    def update(self, table:str, column:str, new_value, check_column, check_column_value):
        self.cur.execute(f"UPDATE {table} SET {column}={new_value} WHERE {check_column}={check_column_value}")
        self.connection.commit()
