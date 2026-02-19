from sqlite3 import Connection, Cursor

class CardsDatabase:
    
    def __init__(self, connection:Connection, cursor:Cursor):
        self.connection = connection
        self.cur = cursor


    # GET

    def get_used_cards(self, game_id:int) -> list:
        self.cur.execute(f"SELECT tag, uses FROM used_cards WHERE game_id={game_id}")
        rows = self.cur.fetchall()
        return rows


    # INSERT

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

    def delete_all_used_cards(self, game_id:int):
        self.cur.execute(f"DELETE FROM used_cards WHERE game_id={game_id}")
        self.connection.commit()

    def delete_used_card(self, game_id:int, tag:str):
        self.cur.execute(f"DELETE FROM used_cards WHERE game_id={game_id} AND tag=\'{tag}\'")
        self.connection.commit()


    # UPDATE

    def update_used_card(self, game_id:int, tag:str, uses:int):
        self.cur.execute(f"UPDATE used_cards SET uses={uses} WHERE game_id={game_id} AND tag=\'{tag}\'")
        self.connection.commit()
