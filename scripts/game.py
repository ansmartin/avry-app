import os
import pickle

import scripts.constants as const
from scripts.users import UserSystem
from scripts.box import PokemonBox


class GameSession:
    
    MAX_ROLLS = 128

    DEFAULT_ROLLS = 20
    DEFAULT_TICKETS = 3
    DEFAULT_MONEY = 10_000
    DEFAULT_ITEM_POINTS = 200
    
    def __init__(self, name, rolls=None, tickets=None, money=None, item_points=None):
        self.name = name

        self.rolls = rolls if rolls else GameSession.DEFAULT_ROLLS
        self.tickets = tickets if tickets else GameSession.DEFAULT_TICKETS
        self.money = money if money else GameSession.DEFAULT_MONEY
        self.item_points = item_points if item_points else GameSession.DEFAULT_ITEM_POINTS
        self.used_cards = {}
        self.box = PokemonBox()

    def set_variables_to_default(self):
        self.rolls = GameSession.DEFAULT_ROLLS
        self.tickets = GameSession.DEFAULT_TICKETS
        self.money = GameSession.DEFAULT_MONEY
        self.item_points = GameSession.DEFAULT_ITEM_POINTS
        self.used_cards = {}

    def reset(self):
        self.set_variables_to_default()
        self.box.init_box()


class GameSessionManager:
    
    def __init__(self, user_system : UserSystem):
        self.user_system = user_system
        self.game = None

    def name_is_available(self, name):
        return name not in self.user_system.active_user.games

    def position_is_in_range(self, position):
        return position>=0 and position<len(self.user_system.active_user.games)

    def get_gamename(self, position):
        if self.position_is_in_range(position):
            return self.user_system.active_user.games[position]

        return None

    def can_add_game(self):
        return len(self.user_system.active_user.games) < self.user_system.MAX_GAMES_IN_USER

    def add_game(self, name):
        self.user_system.active_user.games.append(name)
        self.user_system.save_file_user()

    def add_game_default(self, name):
        self.add_game(name)
        self.create_game(name)

    def add_game_with_options(self, name, rolls, tickets, money, item_points):
        self.add_game(name)

        try:
            rolls = int(rolls)
        except:
            rolls = None

        try:
            tiquets = int(tiquets)
        except:
            tiquets = None

        try:
            money = int(money)
        except:
            money = None

        try:
            item_points = int(item_points)
        except:
            item_points = None

        self.create_game(name, rolls, tickets, money, item_points)

    def remove_game(self, position):
        if self.position_is_in_range(position):
            # borrar archivo de juego
            name = self.get_gamename(position)
            self.delete_file_game(name)
            # y borrar de la lista del usuario
            self.user_system.active_user.games.pop(position)
            self.user_system.save_file_user()
            return True

        return False

    def get_path_game(self, name):
        return f'{const.SAVEDATA_PATH_GAMES}{self.user_system.active_user.username}_{name}.p'

    def change_game(self, position):
        name = self.get_gamename(position)

        if name is None:
            return False

        self.load_game(name)
        return True

    def load_game(self, name):
        # carga los datos guardados
        try:
            game_path = self.get_path_game(name)
            self.game = pickle.load( open(game_path, "rb") )

            if not isinstance(self.game, GameSession):
                raise TypeError()

        # si hay algún error, crea nuevos datos
        except:
            self.create_game(name)

    def create_game(self, name, rolls=None, tickets=None, money=None, item_points=None):
        self.game = GameSession(name, rolls, tickets, money, item_points)
        self.save_file_game()

    def save_file_game(self):
        game_path = self.get_path_game(self.game.name)
        pickle.dump( self.game, open(game_path, "wb") )

    def delete_file_game(self, name):
        game_path = self.get_path_game(name)
        if os.path.exists(game_path):
            os.remove(game_path)


    def can_pay(self, price):
        return self.game.money >= price

    def pay(self, price):
        self.game.money -= price

    def add_pokemon_in_box(self, pokemon_id):
        success = self.game.box.save_pokemon(pokemon_id)
        if success:
            self.save_file_game()

    def reset_game(self):
        self.game.reset()
        self.save_file_game()
