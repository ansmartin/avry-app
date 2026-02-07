from scripts.db import DatabaseManager
from scripts.classlist import ClassList


class User:

    MAX_GAMES = 128

    def __init__(self, user_id:int, username:str, games:ClassList = None):
        self.user_id = user_id
        self.username = username
        self.games = games if games else ClassList(User.MAX_GAMES)


class UserSystem:

    MAX_USERS = 128

    def __init__(self, db:DatabaseManager):
        self.db = db
        self.usernames = ClassList(UserSystem.MAX_USERS, self.db.get_usernames())
        self.active_user = None


    def insert_user(self, username:str) -> bool:
        if self.usernames.contains(username):
            return False

        self.usernames.add(username)
        self.db.insert_user(username)
        return True

    def delete_user(self, position:int) -> bool:
        username = self.usernames.get(position)
        if username is None:
            return False

        user_id = self.db.get_user_id(username)
        if user_id is None:
            return False

        self.usernames.remove(position)
        self.db.delete_user(user_id)

        games_ids_list = self.db.get_game_ids(user_id)
        for game_id in games_ids_list:
            self.db.delete_game(game_id)
            self.db.delete_pokemon_box(game_id)
            self.db.delete_all_used_cards(game_id)

        return True

    def load_user(self, position:int) -> bool:
        username = self.usernames.get(position)
        if username is None:
            return False

        user_id = self.db.get_user_id(username)
        if user_id is None:
            return False

        gamenames_list = self.db.get_gamenames(user_id)
        games = ClassList(User.MAX_GAMES, gamenames_list)
        self.active_user = User(user_id, username, games)
        return True
