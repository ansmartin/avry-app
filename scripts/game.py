import pickle

import scripts.constants as const
from scripts.users import UserSystem
from scripts.box import PokemonBox


class GameSession:
    
    MAX_ROLLS = 128
    
    def __init__(self, name, rolls=None, tickets=None, money=None, item_points=None):
        self.name = name

        if rolls>GameSession.MAX_ROLLS:
            rolls = GameSession.MAX_ROLLS
        self.rolls = rolls

        self.tickets = tickets
        self.money = money
        self.item_points = item_points
        self.used_cards = {}
        self.box = PokemonBox()

    def set_variables_to_default(self):
        self.rolls = 20
        self.tickets = 3
        self.money = 10_000
        self.item_points = 200
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
        return len(self.user_system.active_user.games) < self.user_system.max_games_in_user

    def add_game(self, name):
        if self.name_is_available(name):
            self.user_system.active_user.games.append(name)
            self.user_system.save_user()
            return True

        return False

    def delete_game(self, position):
        if self.position_is_in_range(position):
            self.user_system.active_user.games.pop(position)
            self.user_system.save_user()
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

    def create_game(self, name, rolls=None, tickets=None, money=None, item_points=None):
        self.game = GameSession(name, rolls, tickets, money, item_points)
        self.save_game()

    def load_game(self, name):
        # carga los datos guardados
        try:
            game_path = self.get_path_game(name)
            self.game = pickle.load( open(game_path, "rb") )

            if not isinstance(self.game, GameSession):
                raise TypeError()

        # si hay algún error, crea nuevos datos
        except:
            self.game = GameSession(name)
            self.game.set_variables_to_default()
            self.save_game()

    def save_game(self):
        game_path = self.get_path_game(self.game.name)
        pickle.dump( self.game, open(game_path, "wb") )


    def can_pay(self, price):
        return self.game.money >= price

    def pay(self, price):
        self.game.money -= price

    def add_pokemon_in_box(self, pokemon_id):
        success = self.game.box.save_pokemon(pokemon_id)
        if success:
            self.save_game()
