from scripts.database.users import UsersDatabase
from scripts.controller.games import GamesController

class UsersController:

    MAX_USERS = 256

    def __init__(self, connection, cursor):
        self.db_users = UsersDatabase(connection, cursor)


    # SELECT

    def get_user(self, username:str) -> dict:
        user_id = self.db_users.get_user_id(username)
        if user_id is None:
            return {}

        user = {
            'user_id' : user_id,
            'username' : username
        }
        return user
    
    def get_usernames(self) -> list:
        return self.db_users.get_usernames()


    # INSERT

    def insert_user(self, username:str) -> bool:
        user_id = self.db_users.get_user_id(username)
        if user_id is not None:
            return False

        self.db_users.insert_user(username)
        return True


    # DELETE

    def delete_user(self, user_id:int=None, username:str=None) -> bool:
        if user_id is None:
            if username is None:
                return False
            user_id = self.db_users.get_user_id(username)
            if user_id is None:
                return False

        self.db_users.delete_user(user_id)
        return True
