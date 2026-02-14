from numpy import isnan

from scripts.db import DatabaseManager
from scripts.users import User, UserSystem
from scripts.pokemon import PokemonDatabaseManager
from scripts.filters import PokemonFilters
from scripts.cards import Card, CardManager

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

    def can_spend_roll(self) -> bool:
        return self.options.rolls > 0

    def can_spend_ticket(self) -> bool:
        return self.options.tickets > 0

    def can_spend_money(self, price:int) -> bool:
        return self.options.money >= price

    def can_spend_item_points(self, points:int) -> bool:
        return self.options.item_points >= points

    def can_use_card(self, card:Card) -> bool:
        if card.limit==0: 
            # sin limite
            return True

        uses = self.used_cards.get(card.tag, 0)
        return uses < card.limit


class GameSessionManager:
    
    def __init__(self, db:DatabaseManager):
        self.db = db
        self.pokemon_db = PokemonDatabaseManager()
        self.user_system = UserSystem(db)
        self.cards = CardManager.get_all_cards()

    def create_game_session(self, user_id:int, gamename:str, dic_options:dict=None, dic_filters:dict=None):
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
        self.db.insert_game(
            user_id,
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

    def delete_game_session(self, user_id:int, gamename:str) -> bool:
        game_id = self.db.get_game_id(user_id, gamename)
        if game_id is None:
            return False

        self.db.delete_game(game_id)
        self.db.delete_pokemon_box(game_id)
        self.db.delete_all_used_cards(game_id)
        return True

    def get_game_session(self, user_id:int, gamename:str) -> GameSession:
        game_id = self.db.get_game_id(user_id, gamename)
        if game_id is None:
            return None

        # cargar datos de la sesión de juego
        game = self.db.get_game(game_id)

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

        pokemons_list = self.db.get_pokemon_box(game_id)
        box = { x[0]:x[1] for x in pokemons_list }

        used_cards_rows = self.db.get_used_cards(game_id)
        used_cards = {}
        for card in used_cards_rows:
            used_cards[card[0]] = card[1]

        game = GameSession(
            gamename, 
            options, 
            filters, 
            box, 
            used_cards, 
            game_id, 
            user_id
        )
        self.pokemon_db.filter_dataset(game.filters)
        return game


    def get_random_pokemon(self, obtained_pokemon_list:list, random_ability:bool=False, mask=None) -> dict:
        pokemon = self.pokemon_db.get_random_pokemon(obtained_pokemon_list, mask)

        if not pokemon:
            return {}

        if random_ability:
            ability = self.pokemon_db.get_random_ability()
            pokemon['random_ability_id'] = ability.get('ability_id')
            pokemon['random_ability_name'] = ability.get('ability_name')

        return pokemon

    def get_random_pokemon_and_save(self, game_id:int, obtained_pokemon_list:list, random_ability:bool=False, mask=None) -> dict:
        pokemon = self.pokemon_db.get_random_pokemon(obtained_pokemon_list, mask)

        if not pokemon:
            return {}

        if random_ability:
            ability = self.pokemon_db.get_random_ability()
            pokemon['random_ability_id'] = ability.get('ability_id')
            pokemon['random_ability_name'] = ability.get('ability_name')

        # guardar pokemon
        self.db.insert_pokemon(
            game_id,
            pokemon.get('id'), 
            pokemon.get('random_ability_id')
        )

        return pokemon


    def reset_rolls_and_box(self, game:GameSession):
        game.options.rolls = game.options.max_rolls
        self.db.update_game(
            game.game_id,
            'rolls',
            game.options.max_rolls
        )
        game.box = {}
        self.db.delete_pokemon_box(
            game.game_id
        )


    def add_rolls(self, game:GameSession, rolls:int):
        game.options.rolls+=rolls
        self.db.update_game(
            game.game_id,
            'rolls',
            game.options.rolls
        )
        game.options.max_rolls+=rolls
        self.db.update_game(
            game.game_id,
            'max_rolls',
            game.options.max_rolls
        )

    def add_tickets(self, game:GameSession, tickets:int):
        game.options.tickets+=tickets
        self.db.update_game(
            game.game_id,
            'tickets',
            game.options.tickets
        )


    def spend_roll(self, game:GameSession):
        game.options.rolls-=1
        self.db.update_game(
            game.game_id,
            'rolls',
            game.options.rolls
        )

    def spend_ticket(self, game:GameSession):
        game.options.tickets-=1
        self.db.update_game(
            game.game_id,
            'tickets',
            game.options.tickets
        )

    def spend_money(self, game:GameSession, price:int):
        game.options.money-=price
        self.db.update_game(
            game.game_id,
            'money',
            game.options.money
        )

    def spend_item_points(self, game:GameSession, points:int):
        game.options.item_points-=points
        self.db.update_game(
            game.game_id,
            'item_points',
            game.options.item_points
        )


    def add_used_card(self, game:GameSession, tag:str):
        uses = game.used_cards.get(tag)
        if uses is None:
            uses = 1
            self.db.insert_used_card(
                game.game_id,
                tag,
                uses
            )
        else:
            uses += 1
            self.db.update_used_card(
                game.game_id,
                tag,
                uses
            )
        game.used_cards[tag] = uses


    # Rolls

    def do_roll(self, game:GameSession, obtained_pokemon_list:list) -> dict:
        if game.options.rolls==0:
            return {}

        # obtener pokemon
        pokemon = self.get_random_pokemon_and_save(
            game.game_id,
            obtained_pokemon_list,
            game.filters.random_ability
        )
        if not pokemon:
            return {}

        # gastar tirada
        self.spend_roll(game)

        return pokemon

    def do_roll_with_type(self, game:GameSession, obtained_pokemon_list:list, pokemon_type:str) -> dict:
        if game.options.rolls==0:
            return {}

        if game.options.tickets==0:
            return

        mask = (
            (self.pokemon_db.df_filtered.first_type==pokemon_type) 
            | 
            (self.pokemon_db.df_filtered.second_type==pokemon_type)
        )

        # obtener pokemon
        pokemon = self.get_random_pokemon_and_save(
            game.game_id,
            obtained_pokemon_list,
            game.filters.random_ability,
            mask
        )
        if not pokemon:
            return {}

        # gastar tirada
        self.spend_ticket(game)
        self.spend_roll(game)

        return pokemon


    # Cards

    def buy_card(self, card:Card):
        self.spend_money(card.price)
        
        if card.limit>0:
            self.add_used_card(card.tag)

    def check_card_conditions(self, card:Card) -> bool:
        if card is None:
            return False

        if not self.game.can_use_card(card):
            return False

        if not self.game.can_spend_money(card.price):
            return False

        return True

    def use_card_mega(self):
        tag = 'mega'
        card = self.cards.get(tag)

        if not self.check_card_conditions(card):
            return {}

        # obtener pokemon
        mask = self.pokemon_db.df_filtered.has_mega
        pokemon = self.get_random_pokemon_and_save(mask)
        if not pokemon:
            return {}

        self.buy_card(card)

        return pokemon

    def use_card_fusion(self, pokemon_id1:int, pokemon_id2:int):
        tag = 'fusion'
        card = self.cards.get(tag)

        if not self.check_card_conditions(card):
            return {}

        if len(self.game.box)<2:
            return {}

        # obtener pokemon
        pokemon = self.get_random_pokemon_and_save()
        if not pokemon:
            return {}

        # borrar pokemons
        self.db.delete_pokemon(game_id, pokemon_id1)
        self.db.delete_pokemon(game_id, pokemon_id2)

        self.buy_card(card)

        return pokemon

    def use_card_intercambio(self, pokemon_id:int):
        tag = 'intercambio'
        card = self.cards.get(tag)

        if not self.check_card_conditions(card):
            return {}

        if len(self.game.box)==0:
            return {}

        # obtener pokemon
        pokemon = self.get_random_pokemon_and_save()
        if not pokemon:
            return {}

        # borrar pokemon
        self.db.delete_pokemon(game_id, pokemon_id)

        self.buy_card(card)

        return pokemon

    def use_card_preevo(self, pokemon_id:int):
        tag = 'preevo'
        card = self.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        if len(self.game.box)==0:
            return

        preevo_id = self.pokemon_db.df.loc[pokemon_id].evolves_from_pokemon_id

        if isnan(preevo_id):
            return

        pokemon = self.pokemon_db.df.loc[preevo_id].to_dict()

        ability_id = None
        if self.game.filters.random_ability:
            ability = self.pokemon_db.get_random_ability()
            pokemon['random_ability_id'] = ability.get('ability_id')
            pokemon['random_ability_name'] = ability.get('ability_name')
            ability_id = ability.get('ability_id')

        # borrar pokemon e insertar preevo
        self.db.delete_pokemon(game_id, pokemon_id)
        self.db.insert_pokemon(game_id, preevo_id, ability_id)

        self.buy_card(card)

        return pokemon

    def use_card_comienzo(self):
        tag = 'comienzo'
        card = self.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        if abs(self.game.options.rolls - self.game.options.max_rolls) >= 18:
            return

        self.reset_rolls_and_box()
        self.buy_card(card)

    def use_card_powerhouse(self):
        tag = 'powerhouse'
        card = self.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        self.buy_card(card)

    def use_card_type(self):
        tag = 'tipo'
        card = self.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        self.add_tickets(1)
        self.buy_card(card)

    def use_card_aditional(self, rolls:int):
        tag = 'adicional_' + str(rolls)
        card = self.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        self.add_rolls(rolls)
        self.buy_card(card)
