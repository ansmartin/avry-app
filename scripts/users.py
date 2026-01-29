import os
import pickle

import scripts.constants as const


class User:

    def __init__(self, username, games=None):
        self.username = username
        self.games = games if games else []

    def get_user_games_list(self):
        return [ x for x in self.games ]

    def position_is_in_range(self, position):
        return position>=0 and position<len(self.games)

    def get_gamename(self, position):
        if self.position_is_in_range(position):
            return self.games[position]

        return None

    def name_is_available(self, name):
        return name not in self.games

class UserSystem:
    
    MAX_USERS = 128
    MAX_GAMES_IN_USER = 128

    def __init__(self):
        self.usernames_list = []
        self.load_usernames()

        self.active_user = None


    # usernames_list
    
    def load_usernames(self):
        # carga los datos guardados
        try:
            self.usernames_list = pickle.load( open(const.SAVEDATA_PATH_USERNAMES_FILE, "rb") )

            if not isinstance(self.usernames_list, list):
                raise TypeError()

            if len(self.usernames_list)>0:
                for s in self.usernames_list:
                    if not isinstance(s, str):
                        raise TypeError()

        # si hay algún error, crea nuevos datos
        except:
            self.usernames_list = []
            self.save_file_usernames()

    def save_file_usernames(self):
        pickle.dump( self.usernames_list, open(const.SAVEDATA_PATH_USERNAMES_FILE, "wb") )

    def name_is_available(self, username):
        return username not in self.usernames_list

    def position_is_in_range(self, position):
        return position>=0 and position<len(self.usernames_list)

    def get_username(self, position):
        if self.position_is_in_range(position):
            return self.usernames_list[position]

        return None

    def can_add_user(self):
        return len(self.usernames_list) < UserSystem.MAX_USERS

    def add_user(self, username):
        self.usernames_list.append(username)
        self.save_file_usernames()

        self.create_user(username)

    def remove_user(self, position):
        if self.position_is_in_range(position):
            # borrar archivo de usuario
            username = self.get_username(position)
            self.delete_file_user(username)
            # y borrar de la lista de nombres de usuarios
            self.usernames_list.pop(position)
            self.save_file_usernames()
            return True

        return False


    # user

    def get_path_user(self, name):
        return f'{const.SAVEDATA_PATH_USERS}{name}.p'

    def change_user(self, position):
        username = self.get_username(position)

        if username is None:
            return False

        self.load_user(username)
        return True

    def load_user(self, username):
        # carga los datos guardados
        try:
            user_path = self.get_path_user(username)
            game_list = pickle.load( open(user_path, "rb") )

            if not isinstance(game_list, list):
                raise TypeError()

            if len(game_list)>0:
                for s in game_list:
                    if not isinstance(s, str):
                        raise TypeError()

            self.active_user = User(username, game_list)

        # si hay algún error, crea nuevos datos
        except:
            self.create_user(username)

    def create_user(self, username):
        self.active_user = User(username)
        self.save_file_user()

    def save_file_user(self):
        user_path = self.get_path_user(self.active_user.username)
        pickle.dump( self.active_user.get_user_games_list(), open(user_path, "wb") )

    def delete_file_user(self, username):
        user_path = self.get_path_user(username)
        if os.path.exists(user_path):
            os.remove(user_path)
