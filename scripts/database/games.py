from sqlite3 import Connection, Cursor

class GamesDatabase:
    
    def __init__(self, connection:Connection, cursor:Cursor):
        self.connection = connection
        self.cur = cursor


    # SELECT

    def get_game(self, game_id:int) -> dict:
        self.cur.execute(
            f"""
            SELECT 
                game_id,
                user_id,
                gamemode_id,
                max_rolls,
                rolls,
                tickets,
                money,
                item_points
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
            'gamemode_id' : game[2],
            'max_rolls' : game[3], 
            'rolls' : game[4], 
            'tickets' : game[5], 
            'money' : game[6], 
            'item_points' : game[7]
        }
        return game_dic

    def get_gamemode(self, gamemode_id:int) -> dict:
        self.cur.execute(
            f"""
            SELECT 
                gamemode_id,
                gamename,
                max_rolls,
                max_tickets,
                max_money,
                max_item_points,
                generation,
                include_mythical,
                include_legendary,
                include_sublegendary,
                include_powerhouse,
                fully_evolved_only,
                random_ability
            FROM gamemodes 
            WHERE gamemode_id={gamemode_id}
            """
        )
        rows = self.cur.fetchall()
        if not rows:
            return {}

        game = rows[0]
        game_dic = {
            'gamemode_id' : game[0],
            'gamename' : game[1],
            'max_rolls' : game[2], 
            'max_tickets' : game[3], 
            'max_money' : game[4], 
            'max_item_points' : game[5],
            'generation' : game[6],
            'mythical' : game[7],
            'legendary' : game[8],
            'sublegendary' : game[9],
            'powerhouse' : game[10],
            'fully_evolved' : game[11],
            'random_ability' : game[12]
        }
        return game_dic

    # def get_games(self, user_id:int) -> list:
    #     self.cur.execute(f"SELECT game_id, gamename FROM games WHERE user_id={user_id}")
    #     rows = self.cur.fetchall()
    #     return rows

    def get_game_id(self, user_id:int, gamename:str=None, gamemode_id:int=None) -> int|None:
        if gamename is None:
            if gamemode_id is None:
                return None
    
        if gamemode_id is None:
            gamemode_id = self.get_gamemode_id(gamename)
            if gamemode_id is None:
                return None

        self.cur.execute(f"SELECT game_id FROM games WHERE user_id={user_id} AND gamemode_id={gamemode_id}")
        rows = self.cur.fetchall()
        if not rows:
            return None
        return rows[0][0]
    
    
    def get_gamemode_id(self, gamename:str) -> int|None:
        self.cur.execute(f"SELECT gamemode_id FROM gamemodes WHERE gamename=\'{gamename}\'")
        rows = self.cur.fetchall()
        if not rows:
            return None
        return rows[0][0]

    def get_game_ids(self, user_id:int) -> list[int]:
        self.cur.execute(f"SELECT game_id FROM games WHERE user_id={user_id}")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]

    def get_game_ids_of_gamemode(self, gamemode_id:int) -> list[int]:
        self.cur.execute(f"SELECT game_id FROM games WHERE gamemode_id={gamemode_id}")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]

    def get_gamenames(self) -> list[str]:
        self.cur.execute(f"SELECT gamename FROM gamemodes")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]

    def get_gamenames_user(self, user_id:int) -> list[str]:
        self.cur.execute(f"SELECT gamemode_id FROM games WHERE user_id={user_id}")
        rows = self.cur.fetchall()
        gamemodes_ids = ','.join([ str(x[0]) for x in rows ])
        
        self.cur.execute(f"SELECT gamename FROM gamemodes WHERE gamemode_id IN ({gamemodes_ids})")
        rows = self.cur.fetchall()
        gamenames = [ x[0] for x in rows ]
        return gamenames


    # INSERT

    def insert_game(self, 
            user_id:int,
            gamemode_id:int,
            max_rolls:int,
            rolls:int,
            tickets:int,
            money:int,
            item_points:int
        ):
        self.cur.execute(
            f"""
            INSERT INTO games 
            (
                user_id,
                gamemode_id,
                max_rolls,
                rolls,
                tickets,
                money,
                item_points
            )
            VALUES 
            (
                {user_id},
                {gamemode_id},
                {max_rolls},
                {rolls},
                {tickets},
                {money},
                {item_points}
            )
            """
        )
        self.connection.commit()

    def insert_gamemode(self, 
            gamename:str,
            rolls:int,
            tickets:int,
            money:int,
            item_points:int,
            generation:int,
            mythical:bool,
            legendary:bool,
            sublegendary:bool,
            powerhouse:bool,
            fully_evolved:bool,
	        random_ability:bool,
        ):
        self.cur.execute(
            f"""
            INSERT INTO gamemodes 
            (
                gamename,
                max_rolls,
                max_tickets,
                max_money,
                max_item_points,
                generation,
                include_mythical,
                include_legendary,
                include_sublegendary,
                include_powerhouse,
                fully_evolved_only,
                random_ability
            )
            VALUES 
            (
                \'{gamename}\',
                {rolls},
                {tickets},
                {money},
                {item_points},
                {generation},
                {int(mythical)},
                {int(legendary)},
                {int(sublegendary)},
                {int(powerhouse)},
                {int(fully_evolved)},
                {int(random_ability)}
            )
            """
        )
        self.connection.commit()


    # DELETE

    def delete_game(self, game_id:int):
        self.cur.execute(f"DELETE FROM games WHERE game_id={game_id}")
        self.connection.commit()

    def delete_gamemode(self, gamemode_id:int):
        self.cur.execute(f"DELETE FROM gamemodes WHERE gamemode_id={gamemode_id}")
        self.connection.commit()


    # UPDATE

    def update_game(self, game_id:int, column:str, value):
        self.cur.execute(f"UPDATE games SET {column}={value} WHERE game_id={game_id}")
        self.connection.commit()
