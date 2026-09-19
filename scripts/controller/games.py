from scripts.database.games import GamesDatabase
from scripts.controller.pokemon import PokemonController
from scripts.controller.rolls import RollsController
from scripts.controller.cards import CardsController
from scripts.classes.game import GameProperties, PokemonFilters, PokemonBox, GameSession

class GamesController:
    
    def __init__(self, connection, cursor):
        self.db_games = GamesDatabase(connection, cursor)
        self.pokemon = PokemonController(connection, cursor)
        self.rolls = RollsController(connection, cursor)
        self.cards = CardsController(connection, cursor)


    # SELECT

    def get_gamemode(self, gamemode_id:int=None, gamename:str=None) -> dict:
        if gamemode_id is None:
            if gamename is None:
                return None
            gamemode_id = self.db_games.get_gamemode_id(gamename)
            if gamemode_id is None:
                return None

        # cargar datos
        gamemode = self.db_games.get_gamemode(gamemode_id)
        return gamemode

    def get_game(self, game_id:int=None, user_id:int=None, gamename:str=None) -> GameSession:
        if game_id is None:
            if user_id is None or gamename is None:
                return None
            gamemode_id = self.db_games.get_gamemode_id(gamename)
            if gamemode_id is None:
                return None
            game_id = self.db_games.get_game_id(user_id, gamemode_id=gamemode_id)
            if game_id is None:
                return None

        # cargar datos de la sesión de juego
        game = self.db_games.get_game(game_id)

        user_id = game.get('user_id')

        properties = GameProperties(
            max_rolls = game.get('max_rolls'), 
            rolls = game.get('rolls'), 
            tickets = game.get('tickets'), 
            money = game.get('money'), 
            item_points = game.get('item_points')
        )

        gamemode = self.db_games.get_gamemode(gamemode_id)

        filters = PokemonFilters(
            generation = gamemode.get('generation'),
            mythical = gamemode.get('mythical'),
            legendary = gamemode.get('legendary'),
            sublegendary = gamemode.get('sublegendary'),
            powerhouse = gamemode.get('powerhouse'),
            fully_evolved = gamemode.get('fully_evolved'),
            random_ability = gamemode.get('random_ability')
        )

        box = { x:y for x,y in self.rolls.db_rolls.get_rolls(game_id) }
        pokemon_box = PokemonBox(box)

        used_cards = self.cards.get_used_cards(game_id)

        game = GameSession(
            game_id, 
            user_id,
            gamename, 
            properties, 
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

    def create_game(self, user_id:int, gamemode_id:int):
        
        gamemode = self.db_games.get_gamemode(gamemode_id)
        if not gamemode:
            return None

        self.db_games.insert_game(
            user_id,
            gamemode_id,
            gamemode.get('max_rolls'),
            gamemode.get('max_rolls'),
            gamemode.get('max_tickets'), 
            gamemode.get('max_money'), 
            gamemode.get('max_item_points')
        )

    def create_gamemode(self, gamename:str, dic_options:dict):

        try:
            rolls = dic_options.get('rolls')
            rolls = int(rolls)
            if rolls<0:
                rolls=0
            elif rolls > GameProperties.MAX_ROLLS:
                rolls = GameProperties.MAX_ROLLS
        except:
            rolls = GameProperties.DEFAULT_ROLLS

        try:
            tickets = dic_options.get('tickets')
            tickets = int(tickets)
            if tickets<0:
                tickets=0
            elif tickets > GameProperties.MAX_TICKETS:
                tickets = GameProperties.MAX_TICKETS
        except:
            tickets = GameProperties.DEFAULT_TICKETS

        try:
            money = dic_options.get('money')
            money = int(money)
            if money<0:
                money=0
            elif money > GameProperties.MAX_MONEY:
                money = GameProperties.MAX_MONEY
        except:
            money = GameProperties.DEFAULT_MONEY

        try:
            item_points = dic_options.get('item_points')
            item_points = int(item_points)
            if item_points<0:
                item_points=0
            elif item_points > GameProperties.MAX_ITEM_POINTS:
                item_points = GameProperties.MAX_ITEM_POINTS
        except:
            item_points = GameProperties.DEFAULT_ITEM_POINTS

        properties = GameProperties(
            max_rolls = rolls,
            rolls = rolls, 
            tickets = tickets, 
            money = money, 
            item_points = item_points
        )

        try:
            generation = dic_options.get('generation')
            generation = int(generation)
            if generation<0:
                generation=0
            elif generation>PokemonFilters.DEFAULT_GENERATION:
                raise Exception()
        except:
            generation = PokemonFilters.DEFAULT_GENERATION
        
        filters = PokemonFilters(
            generation = generation,
            mythical = dic_options.get('mythical',PokemonFilters.DEFAULT_MYTHICAL),
            legendary = dic_options.get('legendary',PokemonFilters.DEFAULT_LEGENDARY),
            sublegendary = dic_options.get('sublegendary',PokemonFilters.DEFAULT_SUBLEGENDARY),
            powerhouse = dic_options.get('powerhouse',PokemonFilters.DEFAULT_POWERHOUSE),
            fully_evolved = dic_options.get('fully_evolved',PokemonFilters.DEFAULT_FULLY_EVOLVED),
            random_ability = dic_options.get('random_ability',PokemonFilters.DEFAULT_RANDOM_ABILITY)
        )

        self.db_games.insert_gamemode(
            gamename,
            properties.rolls,
            properties.tickets,
            properties.money,
            properties.item_points,
            filters.generation,
            filters.mythical,
            filters.legendary,
            filters.sublegendary,
            filters.powerhouse,
            filters.fully_evolved,
            filters.random_ability
        )


    # DELETE

    def delete_game(self, game_id:int=None, user_id:int=None, gamename:str=None) -> bool:
        if game_id is None:
            if user_id is None or gamename is None:
                return False
            game_id = self.db_games.get_game_id(user_id, gamename=gamename)
            if game_id is None:
                return False

        self.db_games.delete_game(game_id)
        self.rolls.db_rolls.delete_rolls(game_id)
        self.cards.db_cards.delete_all_used_cards(game_id)
        return True 

    def delete_gamemode(self, gamemode_id:int=None, gamename:str=None) -> bool:
        if gamemode_id is None:
            if gamename is None:
                return False
            gamemode_id = self.db_games.get_gamemode_id(gamename)
            if gamemode_id is None:
                return False

        self.db_games.delete_gamemode(gamemode_id)
        game_ids = self.db_games.get_game_ids_of_gamemode(gamemode_id)
        for game_id in game_ids:
            self.delete_game(game_id=game_id)
        return True 

    def delete_games_of_user(self, user_id):
        games_ids_list = self.db_games.get_game_ids(user_id)
        for game_id in games_ids_list:
            self.delete_game(game_id=game_id)
        return True

    def delete_roll(self, game:GameSession, pokemon_id:int):
        game.pokemon_box.box.pop(pokemon_id)
        self.rolls.db_rolls.delete_roll(
            game.game_id, 
            pokemon_id
        )


    # UPDATE

    def add_rolls(self, game:GameSession, quantity:int):
        game.properties.rolls+=quantity
        self.db_games.update_game(
            game.game_id,
            'rolls',
            game.properties.rolls
        )
        game.properties.max_rolls+=quantity
        self.db_games.update_game(
            game.game_id,
            'max_rolls',
            game.properties.max_rolls
        )

    def add_tickets(self, game:GameSession, quantity:int):
        game.properties.tickets+=quantity
        self.db_games.update_game(
            game.game_id,
            'tickets',
            game.properties.tickets
        )

    def spend_roll(self, game:GameSession):
        game.properties.rolls-=1
        self.db_games.update_game(
            game.game_id,
            'rolls',
            game.properties.rolls
        )

    def spend_ticket(self, game:GameSession):
        game.properties.tickets-=1
        self.db_games.update_game(
            game.game_id,
            'tickets',
            game.properties.tickets
        )

    def spend_money(self, game:GameSession, price:int):
        game.properties.money-=price
        self.db_games.update_game(
            game.game_id,
            'money',
            game.properties.money
        )

    def spend_item_points(self, game:GameSession, points:int):
        game.properties.item_points-=points
        self.db_games.update_game(
            game.game_id,
            'item_points',
            game.properties.item_points
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
        game.properties.rolls = game.properties.max_rolls
        self.db_games.update_game(
            game.game_id,
            'rolls',
            game.properties.max_rolls
        )
        game.pokemon_box.reset()
        self.rolls.db_rolls.delete_rolls(
            game.game_id
        )


    # Rolls

    def do_roll(self, game:GameSession, pokemon_type:str=None) -> dict:
        additional_filters = None

        if game.properties.rolls==0:
            return {}

        if pokemon_type:
            if game.properties.tickets==0:
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
