from scripts.database.games import GamesDatabase
from scripts.controller.pokemon import PokemonController
from scripts.controller.rolls import RollsController
from scripts.controller.cards import CardsController
from scripts.game import GameOptions, PokemonFilters, PokemonBox, GameSession

class GamesController:
    
    def __init__(self, connection, cursor):
        self.db_games = GamesDatabase(connection, cursor)
        self.pokemon = PokemonController(connection, cursor)
        self.rolls = RollsController(connection, cursor)
        self.cards = CardsController(connection, cursor)


    # GET

    def get_game(self, 
            game_id:int=None, user_id:int=None, gamename:str=None, 
            advanced_pokemon_box:bool=False
        ) -> GameSession:
        if game_id is None:
            if user_id is None or gamename is None:
                return None
            game_id = self.db_games.get_game_id(user_id, gamename)
            if game_id is None:
                return None

        # cargar datos de la sesión de juego
        game = self.db_games.get_game(game_id)

        user_id = game.get('user_id')
        gamename = game.get('gamename')

        options = GameOptions(
            max_rolls = game.get('max_rolls'), 
            rolls = game.get('rolls'), 
            tickets = game.get('tickets'), 
            money = game.get('money'), 
            item_points = game.get('item_points')
        )

        filters = PokemonFilters(
            generation = game.get('generation'),
            mythical = game.get('mythical'),
            legendary = game.get('legendary'),
            sublegendary = game.get('sublegendary'),
            powerhouse = game.get('powerhouse'),
            others = game.get('others'),
            fully_evolved = game.get('fully_evolved'),
            random_ability = game.get('random_ability')
        )

        box = { x:y for x,y in self.rolls.db_rolls.get_rolls(game_id) }
        # if advanced_pokemon_box:
        #     pokemon_box = [
        #         self.pokemon.get_pokemon_name_and_ability(pokemon_id, ability_id)
        #         for pokemon_id, ability_id in box
        #     ]
        # else:
        #    pokemon_box = [ x[0] for x in box ]
        pokemon_box = PokemonBox(box)

        used_cards = self.cards.get_used_cards(game_id)

        game = GameSession(
            game_id, 
            user_id,
            gamename, 
            options, 
            filters, 
            pokemon_box, 
            used_cards
        )
        return game

    def get_game_simplified_dict(self, game:GameSession):
        # convertir a diccionario
        game_dict = game.to_dict()

        # rellenar la caja con los nombres de los pokemon y nombres de habilidades 
        box = game_dict['pokemon_box']['box']
        new_box = { 
            pokemon_id : self.pokemon.get_pokemon_important_data(pokemon_id, ability_id)
            for pokemon_id,ability_id in box.items()
        }
        game_dict['pokemon_box']['box'] = new_box

        return game_dict

    # INSERT

    def create_game(self, user_id:int, gamename:str, dic_options:dict):
        options = None
        filters = None

        if dic_options.get('default_options'):
            options = GameOptions()
        else:
            try:
                max_rolls = int(dic_options['rolls'])
                if max_rolls<0:
                    max_rolls=0
                elif max_rolls > GameOptions.MAX_ROLLS:
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

        if dic_options.get('default_filters'):
            filters = PokemonFilters()
        else:
            try:
                generation = int(dic_options['generation'])
                if generation<0:
                    generation=0
                elif generation>PokemonFilters.DEFAULT_GENERATION:
                    generation = PokemonFilters.DEFAULT_GENERATION
            except:
                generation = PokemonFilters.DEFAULT_GENERATION
            
            filters = PokemonFilters(
                generation = generation,
                mythical = dic_options['mythical'],
                legendary = dic_options['legendary'],
                sublegendary = dic_options['sublegendary'],
                powerhouse = dic_options['powerhouse'],
                others = dic_options['others'],
                fully_evolved = dic_options['fully_evolved'],
                random_ability = dic_options['random_ability']
            )

        self.db_games.insert_game(
            user_id,
            gamename,
            options.max_rolls,
            options.rolls,
            options.tickets,
            options.money,
            options.item_points,
            filters.generation,
            filters.mythical,
            filters.legendary,
            filters.sublegendary,
            filters.powerhouse,
            filters.others,
            filters.fully_evolved,
            filters.random_ability
        )


    # DELETE

    def delete_game(self, game_id:int=None, user_id:int=None, gamename:str=None) -> bool:
        if game_id is None:
            if user_id is None or gamename is None:
                return False
            game_id = self.db_games.get_game_id(user_id, gamename)
            if game_id is None:
                return False

        self.db_games.delete_game(game_id)
        self.rolls.db_rolls.delete_rolls(game_id)
        self.cards.db_cards.delete_all_used_cards(game_id)
        return True 

    def delete_roll(self, game:GameSession, pokemon_id:int):
        game.pokemon_box.box.pop(pokemon_id)
        self.rolls.db_rolls.delete_roll(
            game.game_id, 
            pokemon_id
        )


    # UPDATE

    def add_rolls(self, game:GameSession, quantity:int):
        game.options.rolls+=quantity
        self.db_games.update_game(
            game.game_id,
            'rolls',
            game.options.rolls
        )
        game.options.max_rolls+=quantity
        self.db_games.update_game(
            game.game_id,
            'max_rolls',
            game.options.max_rolls
        )

    def add_tickets(self, game:GameSession, quantity:int):
        game.options.tickets+=quantity
        self.db_games.update_game(
            game.game_id,
            'tickets',
            game.options.tickets
        )

    def spend_roll(self, game:GameSession):
        game.options.rolls-=1
        self.db_games.update_game(
            game.game_id,
            'rolls',
            game.options.rolls
        )

    def spend_ticket(self, game:GameSession):
        game.options.tickets-=1
        self.db_games.update_game(
            game.game_id,
            'tickets',
            game.options.tickets
        )

    def spend_money(self, game:GameSession, price:int):
        game.options.money-=price
        self.db_games.update_game(
            game.game_id,
            'money',
            game.options.money
        )

    def spend_item_points(self, game:GameSession, points:int):
        game.options.item_points-=points
        self.db_games.update_game(
            game.game_id,
            'item_points',
            game.options.item_points
        )

    def insert_roll(self, game:GameSession, pokemon:dict):
        pokemon_id = pokemon.get('pokemon_id')
        ability_id = pokemon.get('random_ability_id')

        game.pokemon_box.box[pokemon_id] = ability_id
        self.rolls.db_rolls.insert_roll(
            game.game_id,
            pokemon_id,
            ability_id
        )

    def reset_rolls_and_box(self, game:GameSession):
        game.options.rolls = game.options.max_rolls
        self.db_games.update_game(
            game.game_id,
            'rolls',
            game.options.max_rolls
        )
        game.pokemon_box.reset()
        self.rolls.db_rolls.delete_rolls(
            game.game_id
        )


    # Rolls

    def do_roll(self, game:GameSession, pokemon_type:str=None) -> dict:
        additional_filters = None

        if game.options.rolls==0:
            return {}

        if pokemon_type:
            if game.options.tickets==0:
                return {}

            additional_filters = { 'pokemon_type':pokemon_type }

        # obtener pokemon
        pokemon = self.pokemon.get_random_pokemon(game, additional_filters)
        if not pokemon:
            return {}

        self.insert_roll(game, pokemon)

        # gastar tirada
        self.spend_roll(game)

        # gastar ticket
        if pokemon_type:
            self.spend_ticket(game)

        return pokemon
