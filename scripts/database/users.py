from sqlite3 import Connection, Cursor

class UsersDatabase:
    
    def __init__(self, connection:Connection, cursor:Cursor):
        self.connection = connection
        self.cur = cursor


    # GET

    def get_users(self) -> list:
        self.cur.execute(f"SELECT user_id, username FROM users")
        rows = self.cur.fetchall()
        return rows

    def get_user(self, user_id:int=None, username:str=None) -> list:
        # buscar por id o por nombre de usuario
        if user_id is not None:
            condition = f"user_id={user_id}"
        elif username is not None:
            condition = f"username=\'{username}\'"
        else:
            return []

        self.cur.execute(f"SELECT * FROM users WHERE {condition}")
        rows = self.cur.fetchall()
        return rows

    def get_user_id(self, username:str) -> int|None:
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


    # INSERT

    def insert_user(self, username:str):
        self.cur.execute(f"INSERT INTO users (username) VALUES (\'{username}\')")
        self.connection.commit()


    # DELETE

    def delete_user(self, user_id:int):
        self.cur.execute(f"DELETE FROM users WHERE user_id={user_id}")
        self.connection.commit()


    # UPDATE

    def update_user(self, user_id:int, column:str, value):
        self.cur.execute(f"UPDATE users SET {column}={value} WHERE user_id={user_id}")
        self.connection.commit()
