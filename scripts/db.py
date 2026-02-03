import sqlite3

import scripts.constants as const


class DatabaseManager:
    
    def __init__(self):
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(const.DATABASE_PATH)
        self.cur = self.connection.cursor()


    def get_table(self, table:str):
        self.cur.execute(f"SELECT * FROM {table}")
        rows = self.cur.fetchall()
        return rows

    def print_all_tables(self):
        tables = ['users', 'games', 'rolls']
        for table in tables:
            rows = self.get_table(table)
            print(rows)


    def insert_user(self, name:str):
        self.cur.execute(f"INSERT INTO users (name) VALUES (\'{name}\')")
        self.connection.commit()

    def insert_game(self, 
            user_id:int,
            name:str,
            rolls:int,
            used_rolls:int,
            tickets:int,
            money:int,
            item_points:int,
            generation:int,
            include_mythical:bool,
            include_legendary:bool,
            include_sublegendary:bool,
            include_powerhouse:bool,
            include_others:bool,
            fully_evolved_only:bool
        ):
        self.cur.execute(
            f"""
            INSERT INTO games 
            (
                user_id,
                name,
                rolls, 
                used_rolls,
                tickets,
                money,
                item_points,
                generation,
                include_mythical,
                include_legendary,
                include_sublegendary,
                include_powerhouse,
                include_others,
                fully_evolved_only
            )
            VALUES 
            (
                {user_id},
                \'{name}\',
                {rolls},
                {used_rolls},
                {tickets},
                {money},
                {item_points},
                {generation},
                {int(include_mythical)},
                {int(include_legendary)},
                {int(include_sublegendary)},
                {int(include_powerhouse)},
                {int(include_others)},
                {int(fully_evolved_only)}
            )
            """
        )
        self.connection.commit()

    def insert_roll(self, game_id:int, pokemon_id:int):
        self.cur.execute(
            f"""
            INSERT INTO rolls 
            (game_id, pokemon_id)
            VALUES ({game_id}, {pokemon_id})
            """
        )
        self.connection.commit()


    def delete(self, table:str, column:str, value):
        self.cur.execute(f"DELETE FROM {table} WHERE {column}={value}")
        self.connection.commit()

    def update(self, table:str, column:str, new_value, check_column, check_column_value):
        self.cur.execute(f"UPDATE {table} SET {column}={new_value} WHERE {check_column}={check_column_value}")
        self.connection.commit()
