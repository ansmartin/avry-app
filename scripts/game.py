import os
import pickle

import scripts.constants as const
from scripts.users import UserSystem
from scripts.classlist import ClassList
from scripts.cards import Card


class GameSession:
    
    MAX_ROLLS = 1028

    DEFAULT_ROLLS = 25
    DEFAULT_TICKETS = 3
    DEFAULT_MONEY = 10_000
    DEFAULT_ITEM_POINTS = 200
    
    def __init__(self, name, rolls=None, tickets=None, money=None, item_points=None):
        self.name = name
        self.box = ClassList()

        self.rolls = rolls if rolls else GameSession.DEFAULT_ROLLS
        self.rolls_backup = self.rolls
        self.tickets = tickets if tickets else GameSession.DEFAULT_TICKETS
        self.money = money if money else GameSession.DEFAULT_MONEY
        self.item_points = item_points if item_points else GameSession.DEFAULT_ITEM_POINTS
        self.used_rolls = 0
        self.used_cards = {}

    def set_variables_to_default(self):
        self.rolls = self.rolls_backup = GameSession.DEFAULT_ROLLS
        self.tickets = GameSession.DEFAULT_TICKETS
        self.money = GameSession.DEFAULT_MONEY
        self.item_points = GameSession.DEFAULT_ITEM_POINTS
        self.used_rolls = 0
        self.used_cards = {}

    def reset(self):
        self.set_variables_to_default()
        self.box.reset()

    def reset_rolls_and_box(self):
        self.rolls = self.rolls_backup
        self.used_rolls = 0
        self.box.reset()

    def can_spend_money(self, price):
        return self.money >= price

    def spend_money(self, price):
        self.money -= price

    def spend_roll(self):
        self.rolls-=1
        self.used_rolls+=1

    def spend_ticket(self):
        self.tickets-=1

    def add_used_card(self, tag : str):
        uses = self.used_cards.get(tag, 0) + 1
        self.used_cards[tag] = uses


class GameSessionManager:
    
    def __init__(self, user_system : UserSystem, game : GameSession = None):
        self.user_system = user_system
        self.game = game

    def add_game_to_list(self, name):
        self.user_system.active_user.games.add(name)
        self.user_system.save_file_user()

    def add_game_default(self, name):
        self.add_game_to_list(name)
        self.create_and_save_game(name)

    def add_game_with_options(self, name, rolls, tickets, money, item_points):
        self.add_game_to_list(name)

        try:
            rolls = int(rolls)
            if rolls<0:
                rolls=0
            if rolls > GameSession.MAX_ROLLS:
                rolls = GameSession.MAX_ROLLS
        except:
            rolls = None

        try:
            tickets = int(tickets)
            if tickets<0:
                tickets=0
        except:
            tickets = None

        try:
            money = int(money)
            if money<0:
                money=0
        except:
            money = None

        try:
            item_points = int(item_points)
            if item_points<0:
                item_points=0
        except:
            item_points = None

        self.create_and_save_game(name, rolls, tickets, money, item_points)

    def remove_game(self, position):
        if self.user_system.active_user.games.position_is_in_range(position):
            # borrar archivo de juego
            name = self.user_system.active_user.games.get(position)
            self.delete_file_game(name)
            # y borrar de la lista del usuario
            self.user_system.active_user.games.remove(position)
            self.user_system.save_file_user()
            return True

        return False

    def get_path_game(self, name):
        return f'{const.SAVEDATA_PATH_GAMES}{self.user_system.active_user.username}_{name}.p'

    def change_game(self, position):
        name = self.user_system.active_user.games.get(position)

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
            self.create_and_save_game(name)

    def create_and_save_game(self, name, rolls=None, tickets=None, money=None, item_points=None):
        self.game = GameSession(name, rolls, tickets, money, item_points)
        self.save_file_game()

    def save_file_game(self):
        game_path = self.get_path_game(self.game.name)
        pickle.dump( self.game, open(game_path, "wb") )

    def delete_file_game(self, name):
        game_path = self.get_path_game(name)
        if os.path.exists(game_path):
            os.remove(game_path)

    # def reset_and_save_game(self):
    #     self.game.reset()
    #     self.save_file_game()


    def can_use_card(self, card : Card):
        if card is None:
            return False

        # sin limite
        if card.limit==0:
            return True

        uses = self.game.used_cards.get(card.tag, 0)
        return uses < card.limit

    def buy_card_and_save_game(self, card):
        # usar carta
        self.game.spend_money(card.price)
        self.game.add_used_card(card.tag)
        # guardar
        self.save_file_game()
