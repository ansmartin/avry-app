from sqlite3 import Connection, Cursor

class GamemodesDatabase:
    
    def __init__(self, connection:Connection, cursor:Cursor):
        self.connection = connection
        self.cur = cursor


    # SELECT

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

    def get_gamemode_id(self, gamename:str) -> int|None:
        self.cur.execute(f"SELECT gamemode_id FROM gamemodes WHERE gamename=\'{gamename}\'")
        rows = self.cur.fetchall()
        if not rows:
            return None
        return rows[0][0]

    def get_all_gamemode_names(self) -> list[str]:
        self.cur.execute(f"SELECT gamename FROM gamemodes")
        rows = self.cur.fetchall()
        return [ x[0] for x in rows ]

    def get_gamenames_of_user(self, user_id:int) -> list[str]:
        self.cur.execute(f"SELECT gamemode_id FROM games WHERE user_id={user_id}")
        rows = self.cur.fetchall()
        gamemodes_ids = ','.join([ str(x[0]) for x in rows ])
        
        self.cur.execute(f"SELECT gamename FROM gamemodes WHERE gamemode_id IN ({gamemodes_ids})")
        rows = self.cur.fetchall()
        gamenames = [ x[0] for x in rows ]
        return gamenames


    # INSERT

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

    def delete_gamemode(self, gamemode_id:int):
        self.cur.execute(f"DELETE FROM gamemodes WHERE gamemode_id={gamemode_id}")
        self.connection.commit()


    # UPDATE

