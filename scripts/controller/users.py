from scripts.database.users import UsersDatabase

class UsersController:

    MAX_USERS = 256

    def __init__(self, connection, cursor):
        self.db_users = UsersDatabase(connection, cursor)


    # SELECT

    def get_user(self, username:str) -> dict:
        user_id = self.get_user_id(username)
        if user_id is None:
            return {}

        user = {
            'user_id' : user_id,
            'username' : username
        }
        return user
    
    def get_usernames(self) -> list:
        return self.db_users.get_usernames()
    
    def get_user_id(self, username:str) -> int|None:
        return self.db_users.get_user_id(username)


    # INSERT

    def insert_user(self, username:str):
        self.db_users.insert_user(username)


    # DELETE

    def delete_user(self, user_id:int):
        self.db_users.delete_user(user_id)
