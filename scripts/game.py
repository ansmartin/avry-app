from scripts.db import DatabaseManager
from scripts.users import UserSystem
from scripts.pokemon import PokemonDatabaseManager
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
            used_rolls:int = 0, 
            tickets:int = DEFAULT_TICKETS, 
            money:int = DEFAULT_MONEY, 
            item_points:int = DEFAULT_ITEM_POINTS
        ):
        self.rolls = rolls
        self.used_rolls = used_rolls
        self.tickets = tickets
        self.money = money
        self.item_points = item_points

    def set_to_default(self):
        self.rolls = GameOptions.DEFAULT_ROLLS
        self.used_rolls = 0
        self.tickets = GameOptions.DEFAULT_TICKETS
        self.money = GameOptions.DEFAULT_MONEY
        self.item_points = GameOptions.DEFAULT_ITEM_POINTS


class GameSession:
    
    def __init__(self, 
            name:str, 
            options:GameOptions = None, 
            filters:PokemonFilters = None,
            box:ClassList = None
        ):
        self.name = name
        self.options = options if options else GameOptions()
        self.filters = filters if filters else PokemonFilters()

        self.box = box if box else ClassList()
        self.rolls_backup = self.options.rolls
        self.used_cards = {}


    def get_rolls(self) -> int:
        return self.options.rolls

    def get_tickets(self) -> int:
        return self.options.tickets

    def get_money(self) -> int:
        return self.options.money

    def get_item_points(self) -> int:
        return self.options.item_points


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


class GameSessionManager:
    
    def __init__(self, user_system:UserSystem, database:PokemonDatabaseManager):
        self.user_system = user_system
        self.database = database
        self.game = None

    def create_game_session(self, gamename:str, dic_options:dict=None, dic_filters:dict=None):
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
                rolls = GameOptions.DEFAULT_ROLLS

            try:
                tickets = int(dic_options['tickets'])
                if tickets<0:
                    tickets=0
            except:
                tickets = GameOptions.DEFAULT_TICKETS

            try:
                money = int(dic_options['money'])
                if money<0:
                    money=0
            except:
                money = GameOptions.DEFAULT_MONEY

            try:
                item_points = int(dic_options['item_points'])
                if item_points<0:
                    item_points=0
            except:
                item_points = GameOptions.DEFAULT_ITEM_POINTS

            options = GameOptions(
                rolls = rolls, 
                used_rolls = 0, 
                tickets = tickets, 
                money = money, 
                item_points = item_points
            )


        if dic_filters:
            
            try:
                generation = int(dic_filters['generation'])
                if generation<0:
                    generation=0
            except:
                generation = PokemonFilters.DEFAULT_GENERATION
            
            filters = PokemonFilters(
                generation = generation,
                mythical = dic_filters['mythical'],
                legendary = dic_filters['legendary'],
                sublegendary = dic_filters['sublegendary'],
                powerhouse = dic_filters['powerhouse'],
                others = dic_filters['others'],
                fully_evolved = dic_filters['fully_evolved']
            )


        self.game = GameSession(gamename, options, filters)
        self.insert_game()

    def insert_game(self):
        self.user_system.active_user.games.add(self.game.name)
        self.user_system.db.insert_game(
            self.user_system.active_user.username,
            self.game.name,
            self.game.options.rolls,
            self.game.options.used_rolls,
            self.game.options.tickets,
            self.game.options.money,
            self.game.options.item_points,
            self.game.filters.generation,
            self.game.filters.mythical,
            self.game.filters.legendary,
            self.game.filters.sublegendary,
            self.game.filters.powerhouse,
            self.game.filters.others,
            self.game.filters.fully_evolved,
        )

    def insert_pokemon(self, pokemon_id:int):
        self.game.box.add(pokemon_id)
        self.user_system.db.insert_pokemon(
            self.user_system.active_user.username,
            self.game.name,
            pokemon_id
        )

    def delete_game(self, position:int) -> bool:
        gamename = self.user_system.active_user.games.get(position)
        if gamename is None:
            return False

        self.user_system.active_user.games.remove(position)
        username = self.user_system.active_user.username
        self.user_system.db.delete_game(username, gamename)
        self.user_system.db.delete_pokemon_box(username, gamename)
        self.user_system.db.delete_all_used_cards(username, gamename)
        return True

    def delete_pokemon(self, position:int) -> bool:
        pokemon_id = self.game.box.get(position)
        if pokemon_id is None:
            return False

        self.game.box.remove(pokemon_id)
        self.user_system.db.delete_pokemon(
            self.user_system.active_user.username,
            self.game.name,
            pokemon_id
        )

    def load_game(self, position:int) -> bool:
        gamename = self.user_system.active_user.games.get(position)
        if gamename is None:
            return False

        # cargar datos de la sesión de juego
        game = self.user_system.db.get_game(self.user_system.active_user.username, gamename)

        options = GameOptions(
            rolls = game[2], 
            used_rolls = game[3], 
            tickets = game[4], 
            money = game[5], 
            item_points = game[6]
        )

        filters = PokemonFilters(
            generation = game[7],
            mythical = game[8],
            legendary = game[9],
            sublegendary = game[10],
            powerhouse = game[11],
            others = game[12],
            fully_evolved = game[13]
        )

        pokemon_ids = self.user_system.db.get_pokemon_box(
            self.user_system.active_user.username,
            gamename
        )
        box = ClassList(new_list = pokemon_ids)

        self.game = GameSession(gamename, options, filters, box)
        self.database.filter_dataset(self.game.filters)
        return True


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

    def buy_card_and_save(self, card:Card):
        # usar carta
        self.spend_money(card.price)
        self.add_used_card(card.tag)

    def reset_rolls_and_box(self):
        self.game.options.rolls = self.game.rolls_backup
        self.user_system.db.update_game(
            self.user_system.active_user.username,
            self.game.name,
            'rolls',
            self.game.rolls_backup
        )
        self.game.options.used_rolls = 0
        self.user_system.db.update_game(
            self.user_system.active_user.username,
            self.game.name,
            'used_rolls',
            0
        )
        self.game.box.reset()
        self.user_system.db.delete_pokemon_box(
            self.user_system.active_user.username,
            self.game.name
        )


    def spend_roll(self):
        self.game.options.rolls-=1
        self.user_system.db.update_game(
            self.user_system.active_user.username,
            self.game.name,
            'rolls',
            self.game.options.rolls
        )
        self.game.options.used_rolls+=1
        self.user_system.db.update_game(
            self.user_system.active_user.username,
            self.game.name,
            'used_rolls',
            self.game.options.used_rolls
        )

    def spend_ticket(self):
        self.game.options.tickets-=1
        self.user_system.db.update_game(
            self.user_system.active_user.username,
            self.game.name,
            'tickets',
            self.game.options.tickets
        )

    def spend_money(self, price:int):
        self.game.options.money-=price
        self.user_system.db.update_game(
            self.user_system.active_user.username,
            self.game.name,
            'money',
            self.game.options.money
        )

    def spend_item_points(self, points:int):
        self.game.options.item_points-=points
        self.user_system.db.update_game(
            self.user_system.active_user.username,
            self.game.name,
            'item_points',
            self.game.options.item_points
        )


    def add_used_card(self, tag:str):
        uses = self.game.used_cards.get(tag, 0) + 1
        self.game.used_cards[tag] = uses
