import sqlite3

import scripts.constants as const


class DatabaseManager:
    
    def __init__(self):
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(const.DATABASE_PATH)
        self.cur = self.connection.cursor()

    def execute_and_commit(self, statement:str):
        self.cur.execute(statement)
        self.connection.commit()


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

    def get_users(self) -> list:
        self.cur.execute(f"SELECT user_id, username FROM users")
        rows = self.cur.fetchall()
        return rows

    def get_user(self, 
            user_id:int = None, 
            username:str = None
        ) -> list:

        if user_id is not None:
            query = (f"SELECT * FROM users WHERE user_id={user_id}")
        elif username is not None:
            query = (f"SELECT * FROM users WHERE username=\'{username}\'")
        else:
            return []

        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def get_user_id(self, username:str):
        self.cur.execute(f"SELECT user_id FROM users WHERE username=\'{username}\'")
        rows = self.cur.fetchall()
        if rows:
            return rows[0][0]
        else:
            return None

    def get_usernames(self) -> list:
        self.cur.execute(f"SELECT username FROM users")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]

    def get_game(self, game_id:int) -> list:
        self.cur.execute(f"SELECT * FROM games WHERE game_id={game_id}")
        rows = self.cur.fetchall()
        return rows[0]

    def get_games(self, user_id:int) -> list:
        self.cur.execute(f"SELECT game_id, gamename FROM games WHERE user_id={user_id}")
        rows = self.cur.fetchall()
        return rows

    def get_game_id(self, user_id:int, gamename:str) -> list:
        self.cur.execute(f"SELECT game_id FROM games WHERE user_id={user_id} AND gamename=\'{gamename}\'")
        rows = self.cur.fetchall()
        if rows:
            return rows[0][0]
        else:
            return None

    def get_game_ids(self, user_id:int) -> list:
        self.cur.execute(f"SELECT game_id FROM games WHERE user_id={user_id}")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]

    def get_gamenames(self, user_id:int) -> list:
        self.cur.execute(f"SELECT gamename FROM games WHERE user_id={user_id}")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]

    def get_pokemon_box(self, game_id:int) -> list:
        self.cur.execute(f"SELECT pokemon_id FROM pokemon_box WHERE game_id={game_id}")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]

    def get_used_cards(self, game_id:int) -> list:
        self.cur.execute(f"SELECT tag, uses FROM used_cards WHERE game_id={game_id}")
        rows = self.cur.fetchall()
        return rows


    # INSERT

    def insert_user(self, username:str):
        self.cur.execute(f"INSERT INTO users (username) VALUES (\'{username}\')")
        self.connection.commit()

    def insert_game(self, 
            user_id:int,
            gamename:str,
            max_rolls:int,
            rolls:int,
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
                gamename,
                max_rolls,
                rolls, 
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
                \'{gamename}\',
                {max_rolls},
                {rolls},
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

    def insert_pokemon(self, game_id:int, pokemon_id:int):
        self.cur.execute(
            f"""
            INSERT INTO pokemon_box 
            (game_id, pokemon_id)
            VALUES ({game_id}, {pokemon_id})
            """
        )
        self.connection.commit()

    def insert_used_card(self, game_id:int, tag:str, uses:int):
        self.cur.execute(
            f"""
            INSERT INTO used_cards 
            (game_id, tag, uses)
            VALUES ({game_id}, \'{tag}\', {uses})
            """
        )
        self.connection.commit()


    # DELETE

    def delete(self, table:str, column:str, value):
        self.cur.execute(f"DELETE FROM {table} WHERE {column}={value}")
        self.connection.commit()

    def delete_user(self, user_id:int):
        self.cur.execute(f"DELETE FROM users WHERE user_id={user_id}")
        self.connection.commit()

    def delete_game(self, game_id:int):
        self.cur.execute(f"DELETE FROM games WHERE game_id={game_id}")
        self.connection.commit()

    def delete_pokemon_box(self, game_id:int):
        self.cur.execute(f"DELETE FROM pokemon_box WHERE game_id={game_id}")
        self.connection.commit()

    def delete_pokemon(self, game_id:int, pokemon_id:int):
        self.cur.execute(f"DELETE FROM pokemon_box WHERE game_id={game_id} AND pokemon_id={pokemon_id}")
        self.connection.commit()

    def delete_all_used_cards(self, game_id:int):
        self.cur.execute(f"DELETE FROM used_cards WHERE game_id={game_id}")
        self.connection.commit()

    def delete_used_card(self, game_id:int, tag:str):
        self.cur.execute(f"DELETE FROM used_cards WHERE game_id={game_id} AND tag=\'{tag}\'")
        self.connection.commit()


    # UPDATE

    def update(self, table:str, column:str, new_value, check_column, check_column_value):
        self.cur.execute(f"UPDATE {table} SET {column}={new_value} WHERE {check_column}={check_column_value}")
        self.connection.commit()

    def update_user(self, user_id:int, column:str, value):
        self.cur.execute(f"UPDATE users SET {column}={value} WHERE user_id={user_id}")
        self.connection.commit()

    def update_game(self, game_id:int, column:str, value):
        self.cur.execute(f"UPDATE games SET {column}={value} WHERE game_id={game_id}")
        self.connection.commit()

    def update_used_card(self, game_id:int, tag:str, uses:int):
        self.cur.execute(f"UPDATE used_cards SET uses={uses} WHERE game_id={game_id} AND tag=\'{tag}\'")
        self.connection.commit()
