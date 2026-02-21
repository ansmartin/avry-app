from scripts.db import DatabaseModel
from scripts.controller.games import GamesController

class UsersController:

    MAX_USERS = 128

    def __init__(self, db:DatabaseModel, games:GamesController):
        self.db_users = db.users
        self.games = games


    # GET

    def get_user(self, username:str) -> dict:
        user_id = self.db_users.get_user_id(username)
        if user_id is None:
            return {}

        user = {
            'user_id' : user_id,
            'username' : username,
            'games' : self.games.db_games.get_gamenames(user_id)
        }
        return user


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

        games_ids_list = self.games.db_games.get_game_ids(user_id)
        for game_id in games_ids_list:
            self.games.delete_game_session(game_id=game_id)

        return True
