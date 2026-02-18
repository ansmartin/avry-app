from scripts.db import DatabaseManager
from scripts.game import GameSessionManager

class User:

    MAX_GAMES = 128

    def __init__(self, user_id:int, username:str, games:list = None):
        self.user_id = user_id
        self.username = username
        self.games = games if games else []


class UserManager:

    MAX_USERS = 128

    def __init__(self, db:DatabaseManager):
        self.db = db

    def set_game_manager(self, game_manager:GameSessionManager):
        self.game_manager = game_manager


    # GET

    def get_user(self, user_id:int=None, username:str=None) -> dict:
        if user_id is None:
            user_id = self.db.users.get_user_id(username)
            if user_id is None:
                return {}

        user = {
            'user_id' : user_id,
            'username' : username,
            'games' : self.db.games.get_gamenames(user_id)
        }
        return user


    # INSERT

    def insert_user(self, username:str) -> bool:
        user_id = self.db.users.get_user_id(username)
        if user_id is not None:
            return False

        self.db.users.insert_user(username)
        return True


    # DELETE

    def delete_user(self, username:str) -> bool:
        user_id = self.db.users.get_user_id(username)
        if user_id is None:
            return False

        self.db.users.delete_user(user_id)

        games_ids_list = self.db.games.get_game_ids(user_id)
        for game_id in games_ids_list:
            self.game_manager.delete_game_session(game_id=game_id)

        return True
