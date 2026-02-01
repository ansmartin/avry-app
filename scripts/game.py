import os
import pickle

import scripts.constants as const
from scripts.users import UserSystem
from scripts.database import PokemonDatabaseManager
from scripts.classlist import ClassList
from scripts.filters import PokemonFilters
from scripts.cards import Card


class GameOptions:
    
    MAX_ROLLS = 1028

    DEFAULT_ROLLS = 25
    DEFAULT_TICKETS = 3
    DEFAULT_MONEY = 10_000
    DEFAULT_ITEM_POINTS = 200

    def __init__(self, 
            rolls:int = DEFAULT_ROLLS, 
            tickets:int = DEFAULT_TICKETS, 
            money:int = DEFAULT_MONEY, 
            item_points:int = DEFAULT_ITEM_POINTS
        ):
        self.rolls = rolls
        self.tickets = tickets
        self.money = money
        self.item_points = item_points

    def set_to_default(self):
        self.rolls = GameOptions.DEFAULT_ROLLS
        self.tickets = GameOptions.DEFAULT_TICKETS
        self.money = GameOptions.DEFAULT_MONEY
        self.item_points = GameOptions.DEFAULT_ITEM_POINTS


class GameSession:
    
    def __init__(self, 
            name:str, 
            options:GameOptions = GameOptions(), 
            filters:PokemonFilters = PokemonFilters()
        ):
        self.name = name
        self.box = ClassList()

        self.options = options
        self.filters = filters

        self.rolls_backup = self.options.rolls
        self.used_rolls = 0
        self.used_cards = {}

    def reset_rolls_and_box(self):
        self.options.rolls = self.rolls_backup
        self.used_rolls = 0
        self.box.reset()


    def get_rolls(self) -> int:
        return self.options.rolls

    def get_tickets(self) -> int:
        return self.options.tickets


    def add_rolls(self, rolls:int):
        self.options.rolls+=rolls

    def add_ticket(self):
        self.options.tickets+=1


    def can_spend_roll(self) -> bool:
        return self.options.rolls > 0

    def can_spend_ticket(self) -> bool:
        return self.options.tickets > 0

    def can_spend_money(self, price:int) -> bool:
        return self.options.money >= price

    def can_spend_item_points(self, points:int) -> bool:
        return self.options.item_points >= points


    def spend_roll(self):
        self.options.rolls-=1
        self.used_rolls+=1

    def spend_ticket(self):
        self.options.tickets-=1

    def spend_money(self, price:int):
        self.options.money-=price

    def spend_item_points(self, points:int):
        self.options.item_points-=points


    def add_used_card(self, tag:str):
        uses = self.used_cards.get(tag, 0) + 1
        self.used_cards[tag] = uses


class GameSessionManager:
    
    def __init__(self, user_system:UserSystem, database:PokemonDatabaseManager):
        self.user_system = user_system
        self.database = database
        self.game = None

    def add_game_to_list(self, name):
        self.user_system.active_user.games.add(name)
        self.user_system.save_file_user()

    def create_game_session(self, name:str, dic_options:dict=None, dic_filters:dict=None):
        self.add_game_to_list(name)

        options = None
        filters = None

        if dic_options:
            
            try:
                rolls = int(dic_options['rolls'])
                if rolls<0:
                    rolls=0
                if rolls > GameOptions.MAX_ROLLS:
                    rolls = GameOptions.MAX_ROLLS
            except:
                rolls = None

            try:
                tickets = int(dic_options['tickets'])
                if tickets<0:
                    tickets=0
            except:
                tickets = None

            try:
                money = int(dic_options['money'])
                if money<0:
                    money=0
            except:
                money = None

            try:
                item_points = int(dic_options['item_points'])
                if item_points<0:
                    item_points=0
            except:
                item_points = None

            options = GameOptions(rolls, tickets, money, item_points)


        if dic_filters:
            
            try:
                generation = int(dic_filters['generation'])
                if generation<0:
                    generation=0
            except:
                generation = 9
            
            filters = PokemonFilters(
                generation = generation,
                mythical = dic_filters['mythical'],
                legendary = dic_filters['legendary'],
                sublegendary = dic_filters['sublegendary'],
                powerhouse = dic_filters['powerhouse'],
                others = dic_filters['others'],
                fully_evolved = dic_filters['fully_evolved']
            )


        self.game = GameSession(name, options, filters)
        self.save_file_game()


    def remove_game(self, position:int) -> bool:
        if self.user_system.active_user.games.position_is_in_range(position):
            # borrar archivo de juego
            name = self.user_system.active_user.games.get(position)
            self.delete_file_game(name)
            # y borrar juego de la lista del usuario
            self.user_system.active_user.games.remove(position)
            self.user_system.save_file_user()
            return True

        return False

    def get_path_game(self, name:str) -> str:
        return f'{const.SAVEDATA_PATH_GAMES}{self.user_system.active_user.username}_{name}.p'

    def change_game(self, position:int) -> bool:
        name = self.user_system.active_user.games.get(position)

        if name is None:
            return False

        self.load_game(name)
        return True

    def load_game(self, name:str):
        # carga los datos guardados
        try:
            game_path = self.get_path_game(name)
            self.game = pickle.load( open(game_path, "rb") )

            if not isinstance(self.game, GameSession):
                raise TypeError()

        # si hay algún error, crea nuevos datos
        except:
            self.game = GameSession(name)
            self.save_file_game()

        # pasa los filtros
        self.database.filter_dataset(self.game.filters)


    def save_file_game(self):
        game_path = self.get_path_game(self.game.name)
        pickle.dump( self.game, open(game_path, "wb") )

    def delete_file_game(self, name:str):
        game_path = self.get_path_game(name)
        if os.path.exists(game_path):
            os.remove(game_path)

    # def reset_and_save_game(self):
    #     self.game.reset()
    #     self.save_file_game()

    def get_namelist_of_obtained_pokemon(self) -> list:
        return [ 
            self.database.get_fullname(pokemon_id)
            for pokemon_id in self.game.box._list
        ]

    def can_use_card(self, card:Card) -> bool:
        if card is None:
            return False

        # sin limite
        if card.limit==0:
            return True

        uses = self.game.used_cards.get(card.tag, 0)
        return uses < card.limit

    def buy_card_and_save_game(self, card:Card):
        # usar carta
        self.game.spend_money(card.price)
        self.game.add_used_card(card.tag)
        # guardar
        self.save_file_game()
