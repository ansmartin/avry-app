from scripts.db import DatabaseManager
from scripts.classlist import ClassList


class User:

    MAX_GAMES = 128

    def __init__(self, username:str, games:ClassList = None):
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

        self.usernames.remove(position)
        self.db.delete_user(username)

        gamenames_list = self.db.get_gamenames(username)
        for gamename in gamenames_list:
            self.db.delete_game(username, gamename)
            self.db.delete_pokemon_box(username, gamename)
            self.db.delete_all_used_cards(username, gamename)

        return True

    # def delete_user(self, name:str):
    #     position = self.usernames._list.index(name)
    #     self.usernames.remove(position)

    #     self.db.delete_user(name)

    def load_user(self, position:int) -> bool:
        name = self.usernames.get(position)
        if name is None:
            return False

        gamenames_list = self.db.get_gamenames(name)
        games = ClassList(User.MAX_GAMES, gamenames_list)
        self.active_user = User(name, games)
        return True
