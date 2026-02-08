from scripts.users import UserSystem
from scripts.pokemon import PokemonDatabaseManager
from scripts.filters import PokemonFilters
from scripts.cards import Card


class GameOptions:
    
    MAX_ROLLS = 1028

    DEFAULT_ROLLS = 25
    DEFAULT_TICKETS = 3
    DEFAULT_MONEY = 10_000
    DEFAULT_ITEM_POINTS = 200

    def __init__(self, 
            max_rolls:int = DEFAULT_ROLLS, 
            rolls:int = DEFAULT_ROLLS, 
            tickets:int = DEFAULT_TICKETS, 
            money:int = DEFAULT_MONEY, 
            item_points:int = DEFAULT_ITEM_POINTS
        ):
        self.max_rolls = max_rolls
        self.rolls = rolls
        self.tickets = tickets
        self.money = money
        self.item_points = item_points

    def set_to_default(self):
        self.max_rolls = self.rolls = GameOptions.DEFAULT_ROLLS
        self.tickets = GameOptions.DEFAULT_TICKETS
        self.money = GameOptions.DEFAULT_MONEY
        self.item_points = GameOptions.DEFAULT_ITEM_POINTS


class GameSession:
    
    def __init__(self, 
            name:str, 
            options:GameOptions = None, 
            filters:PokemonFilters = None,
            box:dict = None,
            used_cards:dict = None,
            game_id:int = None,
            user_id:int = None
        ):
        self.name = name
        self.options = options if options else GameOptions()
        self.filters = filters if filters else PokemonFilters()
        self.box = box if box else {}
        self.used_cards = used_cards if used_cards else {}
        self.game_id = game_id
        self.user_id = user_id


    def get_rolls(self) -> int:
        return self.options.rolls

    def get_tickets(self) -> int:
        return self.options.tickets

    def get_money(self) -> int:
        return self.options.money

    def get_item_points(self) -> int:
        return self.options.item_points


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
                max_rolls = int(dic_options['rolls'])
                if max_rolls<0:
                    max_rolls=0
                if max_rolls > GameOptions.MAX_ROLLS:
                    max_rolls = GameOptions.MAX_ROLLS
            except:
                max_rolls = GameOptions.DEFAULT_ROLLS

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
                max_rolls = max_rolls, 
                rolls = max_rolls, 
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
                fully_evolved = dic_filters['fully_evolved'],
                random_ability = dic_filters['random_ability']
            )

        game = GameSession(gamename, options, filters)
        self.user_system.db.insert_game(
            self.user_system.active_user.user_id,
            game.name,
            game.options.max_rolls,
            game.options.rolls,
            game.options.tickets,
            game.options.money,
            game.options.item_points,
            game.filters.generation,
            game.filters.mythical,
            game.filters.legendary,
            game.filters.sublegendary,
            game.filters.powerhouse,
            game.filters.others,
            game.filters.fully_evolved,
            game.filters.random_ability
        )
        self.user_system.active_user.games.add(gamename)

    def insert_pokemon(self, pokemon_id:int, ability_id:int=None):
        self.game.box[pokemon_id] = ability_id
        self.user_system.db.insert_pokemon(
            self.game.game_id,
            pokemon_id,
            ability_id
        )

    def delete_game(self, position:int) -> bool:
        gamename = self.user_system.active_user.games.get(position)
        if gamename is None:
            return False

        self.user_system.active_user.games.remove(position)

        self.user_system.db.delete_game(self.game.game_id)
        self.user_system.db.delete_pokemon_box(self.game.game_id)
        self.user_system.db.delete_all_used_cards(self.game.game_id)
        return True

    def delete_pokemon(self, pokemon_id:int):
        pokemon = self.game.box.get(pokemon_id)
        if pokemon is None:
            return False

        self.game.box.pop(pokemon_id)
        self.user_system.db.delete_pokemon(
            self.game.game_id,
            pokemon_id
        )

    def load_game(self, position:int) -> bool:
        gamename = self.user_system.active_user.games.get(position)
        if gamename is None:
            return False

        user_id = self.user_system.active_user.user_id
        game_id = self.user_system.db.get_game_id(user_id, gamename)
        if game_id is None:
            return False

        # cargar datos de la sesión de juego
        game = self.user_system.db.get_game(game_id)

        options = GameOptions(
            max_rolls = game[3], 
            rolls = game[4], 
            tickets = game[5], 
            money = game[6], 
            item_points = game[7]
        )

        filters = PokemonFilters(
            generation = game[8],
            mythical = game[9],
            legendary = game[10],
            sublegendary = game[11],
            powerhouse = game[12],
            others = game[13],
            fully_evolved = game[14],
            random_ability = game[15]
        )

        pokemons_list = self.user_system.db.get_pokemon_box(game_id)
        box = { x[0]:x[1] for x in pokemons_list }

        used_cards_rows = self.user_system.db.get_used_cards(game_id)
        used_cards = {}
        for card in used_cards_rows:
            used_cards[card[0]] = card[1]

        self.game = GameSession(
            gamename, 
            options, 
            filters, 
            box, 
            used_cards, 
            game_id, 
            user_id
        )
        self.database.filter_dataset(self.game.filters)
        return True


    def get_obtained_pokemon(self) -> list:
        return list(self.game.box.items())

    def can_use_card(self, card:Card) -> bool:
        if card is None:
            return False

        # sin limite
        if card.limit==0:
            return True

        uses = self.game.used_cards.get(card.tag, 0)
        return uses < card.limit

    def buy_card_and_save(self, card:Card):
        self.spend_money(card.price)
        
        if card.limit>0:
            self.add_used_card(card.tag)

    def reset_rolls_and_box(self):
        self.game.options.rolls = self.game.options.max_rolls
        self.user_system.db.update_game(
            self.game.game_id,
            'rolls',
            self.game.options.max_rolls
        )
        self.game.box.reset()
        self.user_system.db.delete_pokemon_box(
            self.game.game_id
        )


    def add_rolls(self, rolls:int):
        self.game.options.rolls+=rolls
        self.user_system.db.update_game(
            self.game.game_id,
            'rolls',
            self.game.options.rolls
        )
        self.game.options.max_rolls+=rolls
        self.user_system.db.update_game(
            self.game.game_id,
            'max_rolls',
            self.game.options.max_rolls
        )

    def add_tickets(self, tickets:int):
        self.game.options.tickets+=tickets
        self.user_system.db.update_game(
            self.game.game_id,
            'tickets',
            self.game.options.tickets
        )


    def spend_roll(self):
        self.game.options.rolls-=1
        self.user_system.db.update_game(
            self.game.game_id,
            'rolls',
            self.game.options.rolls
        )

    def spend_ticket(self):
        self.game.options.tickets-=1
        self.user_system.db.update_game(
            self.game.game_id,
            'tickets',
            self.game.options.tickets
        )

    def spend_money(self, price:int):
        self.game.options.money-=price
        self.user_system.db.update_game(
            self.game.game_id,
            'money',
            self.game.options.money
        )

    def spend_item_points(self, points:int):
        self.game.options.item_points-=points
        self.user_system.db.update_game(
            self.game.game_id,
            'item_points',
            self.game.options.item_points
        )


    def add_used_card(self, tag:str):
        uses = self.game.used_cards.get(tag)
        if uses is None:
            uses = 1
            self.user_system.db.insert_used_card(
                self.game.game_id,
                tag,
                uses
            )
        else:
            uses += 1
            self.user_system.db.update_used_card(
                self.game.game_id,
                tag,
                uses
            )
        self.game.used_cards[tag] = uses
