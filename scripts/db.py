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
        tables = ['users', 'games', 'pokemon_box', 'used_cards']
        for table in tables:
            rows = self.get_table(table)
            print(rows)

    def execute_and_commit(self, statement:str):
        self.cur.execute(statement)
        self.connection.commit()


    def get_usernames(self) -> list:
        self.cur.execute(f"SELECT username FROM users")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]

    def get_gamenames(self, username:str) -> list:
        self.cur.execute(f"SELECT gamename FROM games WHERE username=\'{username}\'")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]

    def get_game(self, username:str, gamename:str) -> list:
        self.cur.execute(f"SELECT * FROM games WHERE username=\'{username}\' AND gamename=\'{gamename}\'")
        rows = self.cur.fetchall()
        return rows[0]

    def get_pokemon_box(self, username:str, gamename:str) -> list:
        self.cur.execute(f"SELECT pokemon_id FROM pokemon_box WHERE username=\'{username}\' AND gamename=\'{gamename}\'")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]

    def get_used_cards(self, username:str, gamename:str) -> list:
        self.cur.execute(f"SELECT card_id FROM used_cards WHERE username=\'{username}\' AND gamename=\'{gamename}\'")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]


    def insert_user(self, username:str):
        self.cur.execute(f"INSERT INTO users (username) VALUES (\'{username}\')")
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

    def insert_pokemon(self, username:str, gamename:str, pokemon_id:int):
        self.cur.execute(
            f"""
            INSERT INTO pokemon_box 
            (username, gamename, pokemon_id)
            VALUES (\'{username}\', \'{gamename}\', {pokemon_id})
            """
        )
        self.connection.commit()

    def insert_used_card(self, username:str, gamename:str, card_id:int):
        self.cur.execute(
            f"""
            INSERT INTO used_cards 
            (username, gamename, card_id)
            VALUES (\'{username}\', \'{gamename}\', {card_id})
            """
        )
        self.connection.commit()


    def delete(self, table:str, column:str, value):
        self.cur.execute(f"DELETE FROM {table} WHERE {column}={value}")
        self.connection.commit()

    def delete_user(self, username:str):
        self.cur.execute(f"DELETE FROM users WHERE username=\'{username}\'")
        self.connection.commit()

    def delete_game(self, username:str, gamename:str):
        self.cur.execute(f"DELETE FROM games WHERE username=\'{username}\' AND gamename=\'{gamename}\'")
        self.connection.commit()

    def delete_pokemon_box(self, username:str, gamename:str):
        self.cur.execute(f"DELETE FROM pokemon_box WHERE username=\'{username}\' AND gamename=\'{gamename}\'")
        self.connection.commit()

    def delete_pokemon(self, username:str, gamename:str, pokemon_id:int):
        self.cur.execute(f"DELETE FROM pokemon_box WHERE username=\'{username}\' AND gamename=\'{gamename}\' AND pokemon_id={pokemon_id}")
        self.connection.commit()

    def delete_all_used_cards(self, username:str, gamename:str):
        self.cur.execute(f"DELETE FROM used_cards WHERE username=\'{username}\' AND gamename=\'{gamename}\'")
        self.connection.commit()

    def delete_used_card(self, username:str, gamename:str, card_id:int):
        self.cur.execute(f"DELETE FROM used_cards WHERE username=\'{username}\' AND gamename=\'{gamename}\' AND card_id={card_id}")
        self.connection.commit()


    def update(self, table:str, column:str, new_value, check_column, check_column_value):
        self.cur.execute(f"UPDATE {table} SET {column}={new_value} WHERE {check_column}={check_column_value}")
        self.connection.commit()

    def update_game(self, username:str, gamename:str, column:str, value):
        self.cur.execute(f"UPDATE games SET {column}={value} WHERE username=\'{username}\' AND gamename=\'{gamename}\'")
        self.connection.commit()
