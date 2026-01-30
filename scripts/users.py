import os
import pickle

import scripts.constants as const
from scripts.classlist import ClassList


class User:

    MAX_GAMES = 128

    def __init__(self, username, games=None):
        self.username = username
        self.games = ClassList(games, User.MAX_GAMES)


class UserSystem:
    
    MAX_USERS = 128

    def __init__(self):
        self.load_usernames()
        self.active_user = None


    # usernames
    
    def load_usernames(self):
        # carga los datos guardados
        try:
            self.usernames = pickle.load( open(const.SAVEDATA_PATH_USERNAMES_FILE, "rb") )

            if not isinstance(self.usernames, ClassList):
                raise TypeError()

            # if len(self.usernames._list)>0:
            #     for element in self.usernames._list:
            #         if not isinstance(element, str):
            #             raise TypeError()

        # si hay algún error, crea nuevos datos
        except:
            self.usernames = ClassList(None, UserSystem.MAX_USERS)
            self.save_file_usernames()

    def save_file_usernames(self):
        pickle.dump( self.usernames, open(const.SAVEDATA_PATH_USERNAMES_FILE, "wb") )

    def add_user_and_save_file(self, username):
        self.usernames.add(username)
        self.save_file_usernames()

        self.create_and_save_user(username)

    def remove_user(self, position):
        if self.usernames.position_is_in_range(position):
            # borrar archivo de usuario
            username = self.usernames.get(position)
            self.delete_file_user(username)
            # y borrar de la lista de nombres de usuarios
            self.usernames.remove(position)
            self.save_file_usernames()
            return True

        return False


    # user

    def get_path_user(self, name):
        return f'{const.SAVEDATA_PATH_USERS}{name}.p'

    def change_user(self, position):
        username = self.usernames.get(position)

        if username is None:
            return False

        self.load_user(username)
        return True

    def load_user(self, username):
        # carga los datos guardados
        try:
            user_path = self.get_path_user(username)
            user = pickle.load( open(user_path, "rb") )

            if not isinstance(user, User):
                raise TypeError()

            # if len(user.games)>0:
            #     for element in user.games._list:
            #         if not isinstance(element, str):
            #             raise TypeError()

            self.active_user = user

        # si hay algún error, crea nuevos datos
        except:
            self.create_and_save_user(username)

    def create_and_save_user(self, username):
        self.active_user = User(username)
        self.save_file_user()

    def save_file_user(self):
        user_path = self.get_path_user(self.active_user.username)
        pickle.dump( self.active_user, open(user_path, "wb") )

    def delete_file_user(self, username):
        user_path = self.get_path_user(username)
        if os.path.exists(user_path):
            os.remove(user_path)
