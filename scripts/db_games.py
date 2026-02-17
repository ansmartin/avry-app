from sqlite3 import Connection, Cursor

class GamesDatabase:
    
    def __init__(self, connection:Connection, cursor:Cursor):
        self.connection = connection
        self.cur = cursor


    # GET

    def get_game(self, game_id:int) -> dict:
        self.cur.execute(
            f"""
            SELECT 
                game_id,
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
                fully_evolved_only,
                random_ability
            FROM games 
            WHERE game_id={game_id}
            """
        )
        rows = self.cur.fetchall()
        if not rows:
            return {}

        game = rows[0]
        game_dic = {
            'game_id' : game[0],
            'user_id' : game[1],
            'gamename' : game[2],
            'max_rolls' : game[3], 
            'rolls' : game[4], 
            'tickets' : game[5], 
            'money' : game[6], 
            'item_points' : game[7],
            'generation' : game[8],
            'mythical' : game[9],
            'legendary' : game[10],
            'sublegendary' : game[11],
            'powerhouse' : game[12],
            'others' : game[13],
            'fully_evolved' : game[14],
            'random_ability' : game[15]
        }
        return game_dic

    def get_games(self, user_id:int) -> list:
        self.cur.execute(f"SELECT game_id, gamename FROM games WHERE user_id={user_id}")
        rows = self.cur.fetchall()
        return rows

    def get_game_id(self, user_id:int, gamename:str) -> int|None:
        self.cur.execute(f"SELECT game_id FROM games WHERE user_id={user_id} AND gamename=\'{gamename}\'")
        rows = self.cur.fetchall()
        if rows:
            return rows[0][0]
        else:
            return None

    def get_game_ids(self, user_id:int) -> list[int]:
        self.cur.execute(f"SELECT game_id FROM games WHERE user_id={user_id}")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]

    def get_gamenames(self, user_id:int) -> list[str]:
        self.cur.execute(f"SELECT gamename FROM games WHERE user_id={user_id}")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]


    # INSERT

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
            fully_evolved_only:bool,
	        random_ability:bool,
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
                fully_evolved_only,
                random_ability
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
                {int(fully_evolved_only)},
                {int(random_ability)}
            )
            """
        )
        self.connection.commit()


    # DELETE

    def delete_game(self, game_id:int):
        self.cur.execute(f"DELETE FROM games WHERE game_id={game_id}")
        self.connection.commit()


    # UPDATE

    def update_game(self, game_id:int, column:str, value):
        self.cur.execute(f"UPDATE games SET {column}={value} WHERE game_id={game_id}")
        self.connection.commit()
