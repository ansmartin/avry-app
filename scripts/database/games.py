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

    # def get_games(self, user_id:int) -> list:
    #     self.cur.execute(f"SELECT game_id, gamename FROM games WHERE user_id={user_id}")
    #     rows = self.cur.fetchall()
    #     return rows

    def get_game_id(self, user_id:int, gamemode_id:int) -> int|None:
        self.cur.execute(f"SELECT game_id FROM games WHERE user_id={user_id} AND gamemode_id={gamemode_id}")
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


    # DELETE

    def delete_game(self, game_id:int):
        self.cur.execute(f"DELETE FROM games WHERE game_id={game_id}")
        self.connection.commit()


    # UPDATE

    def update_game(self, game_id:int, column:str, value):
        self.cur.execute(f"UPDATE games SET {column}={value} WHERE game_id={game_id}")
        self.connection.commit()
