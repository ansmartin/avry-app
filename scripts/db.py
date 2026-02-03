import sqlite3

import scripts.constants as const


class DatabaseManager:
    
    def __init__(self):
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(const.DATABASE_PATH)
        self.cur = self.connection.cursor()


    def get_table(self, table:str) -> list:
        self.cur.execute(f"SELECT * FROM {table}")
        rows = self.cur.fetchall()
        return rows

    def print_all_tables(self):
        tables = ['users', 'games', 'rolls']
        for table in tables:
            rows = self.get_table(table)
            print(rows)

    def execute_and_commit(self, statement:str):
        self.cur.execute(statement)
        self.connection.commit()


    def get_users(self) -> list:
        self.cur.execute(f"SELECT username FROM users")
        rows = self.cur.fetchall()
        return rows

    def get_game_names(self, username:str) -> list:
        self.cur.execute(f"SELECT gamename FROM games WHERE username=\'{username}\'")
        rows = self.cur.fetchall()
        return rows

    def get_game(self, username:str, gamename:str) -> list:
        self.cur.execute(f"SELECT * FROM games WHERE username=\'{username}\' AND gamename=\'{gamename}\'")
        rows = self.cur.fetchall()
        return rows[0]

    def get_rolls(self, game_id:int) -> list:
        self.cur.execute(f"SELECT pokemon_id FROM rolls WHERE game_id={game_id}")
        rows = self.cur.fetchall()
        return rows

    def get_used_cards(self, game_id:int) -> list:
        self.cur.execute(f"SELECT card_id FROM used_cards WHERE game_id={game_id}")
        rows = self.cur.fetchall()
        return rows


    def insert_user(self, username:str):
        self.cur.execute(f"INSERT INTO users (name) VALUES (\'{username}\')")
        self.connection.commit()

    def insert_game(self, 
            username:str,
            gamename:str,
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
                username,
                gamename,
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
                \'{username}\',
                \'{gamename}\',
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

    def insert_used_card(self, game_id:int, card_id:int):
        self.cur.execute(
            f"""
            INSERT INTO used_cards 
            (game_id, card_id)
            VALUES ({game_id}, {card_id})
            """
        )
        self.connection.commit()


    def delete(self, table:str, column:str, value):
        self.cur.execute(f"DELETE FROM {table} WHERE {column}={value}")
        self.connection.commit()

    def delete_user(self, username:str):
        self.cur.execute(f"DELETE FROM users WHERE name=\'{username}\'")
        self.connection.commit()

    def delete_game(self, username:str, gamename:str):
        self.cur.execute(f"DELETE FROM games WHERE username=\'{username}\' AND gamename=\'{gamename}\'")
        self.connection.commit()

    def delete_roll(self, game_id:int, pokemon_id:int):
        self.cur.execute(f"DELETE FROM rolls WHERE game_id={game_id} AND pokemon_id={pokemon_id}")
        self.connection.commit()

    def delete_used_card(self, game_id:int, card_id:int):
        self.cur.execute(f"DELETE FROM used_cards WHERE game_id={game_id} AND card_id={card_id}")
        self.connection.commit()


    def update(self, table:str, column:str, new_value, check_column, check_column_value):
        self.cur.execute(f"UPDATE {table} SET {column}={new_value} WHERE {check_column}={check_column_value}")
        self.connection.commit()
