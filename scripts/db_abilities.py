from sqlite3 import Connection, Cursor

class AbilitiesDatabase:
    
    def __init__(self, connection:Connection, cursor:Cursor):
        self.connection = connection
        self.cur = cursor


    # GET

    def get_abilities(self, generation:int) -> list:
        self.cur.execute(f"SELECT ability_id FROM abilities WHERE generation<={generation}")
        rows = self.cur.fetchall()
        abilities_ids = [ x[0] for x in rows ]
        return abilities_ids

    def get_ability_name(self, ability_id:int) -> str|None:
        self.cur.execute(f"SELECT ability_name FROM abilities WHERE ability_id={ability_id}")
        rows = self.cur.fetchall()
        if rows:
            return rows[0][0]
        else:
            return None
