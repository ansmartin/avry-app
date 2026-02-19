from scripts.db import DatabaseModel
from scripts.controller.pokemon import PokemonController
from scripts.game import GameOptions, PokemonFilters, GameSession
from scripts.cards import Card, CardManager

class GamesController:
    
    def __init__(self, db:DatabaseModel):
        self.db_games = db.games
        self.db_rolls = db.rolls
        self.db_cards = db.cards
        self.pokemon = PokemonController(db)
        self.cards = CardManager.get_all_cards()


    # GET

    def get_game_session(self, 
            game_id:int=None, user_id:int=None, gamename:str=None, 
            advanced_pokemon_box:bool=False
        ) -> GameSession:
        if game_id is None:
            game_id = self.db_games.get_game_id(user_id, gamename)
            if game_id is None:
                return None

        # cargar datos de la sesión de juego
        game = self.db_games.get_game(game_id)

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

        box = self.db_rolls.get_rolls(game_id)
        if advanced_pokemon_box:
            pokemon_box = [
                self.get_pokemon_tuple(pokemon_id, ability_id)
                for pokemon_id, ability_id in box
            ]
        else:
            pokemon_box = [ x[0] for x in box ]

        used_cards = {
            tag : uses
            for tag, uses in self.db_cards.get_used_cards(game_id)
        }

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

    def get_pokemon_tuple(self, pokemon_id:int, ability_id:int):
        tuple = (
            pokemon_id,
            self.pokemon.get_pokemon_fullname(pokemon_id),
            ability_id, 
            self.pokemon.abilities.get_ability_name(ability_id)
        )
        return tuple


    # INSERT

    def create_game_session(self, user_id:int, gamename:str, dic_options:dict):
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

    def delete_game_session(self, game_id:int=None, user_id:int=None, gamename:str=None) -> bool:
        if game_id is None:
            game_id = self.db_games.get_game_id(user_id, gamename)
            if game_id is None:
                return False

        self.db_games.delete_game(game_id)
        self.db_rolls.delete_rolls(game_id)
        self.db_cards.delete_all_used_cards(game_id)
        return True 


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


    def add_used_card(self, game:GameSession, tag:str):
        # used_cards = { key:value for key,value in self.db.get_used_cards(game.game_id) }
        uses = game.used_cards.get(tag)
        if uses is None:
            uses = 1
            self.db_cards.insert_used_card(
                game.game_id,
                tag,
                uses
            )
        else:
            uses += 1
            self.db_cards.update_used_card(
                game.game_id,
                tag,
                uses
            )
        game.used_cards[tag] = uses


    # Rolls

    def do_roll(self, game:GameSession, pokemon_type:str=None) -> dict:
        mask = None

        if game.options.rolls==0:
            return {}

        if pokemon_type:
            if game.options.tickets==0:
                return {}
            
            mask = (
                (self.pokemon_db.df_filtered.first_type==pokemon_type) 
                | 
                (self.pokemon_db.df_filtered.second_type==pokemon_type)
            )

        # obtener pokemon
        pokemon = self.pokemon.get_random_pokemon(
            game,
            save=True
        )
        if not pokemon:
            return {}

        # gastar tirada
        self.spend_roll(game)

        # gastar ticket
        if pokemon_type:
            self.spend_ticket(game)

        return pokemon

    def reset_rolls_and_box(self, game:GameSession):
        game.options.rolls = game.options.max_rolls
        self.db_games.update_game(
            game.game_id,
            'rolls',
            game.options.max_rolls
        )
        game.pokemon_box = []
        self.db_rolls.delete_rolls(
            game.game_id
        )


    # Cards

    def buy_card(self, game:GameSession, card:Card):
        # gastar dinero
        self.spend_money(game, card.price)
        
        # añadir a cartas usadas
        if card.limit>0:
            self.add_used_card(game, card.tag)

    def check_card_conditions(self, game:GameSession, card:Card) -> bool:
        if card is None:
            return False

        if not game.can_use_card(card):
            return False

        if not game.can_spend_money(card.price):
            return False

        return True

    def use_card_mega(self, game:GameSession):
        tag = 'mega'
        card:Card = self.cards.get(tag)

        if not self.check_card_conditions(game, card):
            return {}

        # obtained_pokemon_list = [ x[0] for x in self.db.get_pokemon_box(game.game_id) ]
        mask = self.pokemon_db.df_filtered.has_mega

        pokemon = self.pokemon.get_random_pokemon(
            game,
            save=True
        )
        if not pokemon:
            return {}

        self.buy_card(game, card)

        return pokemon

    def use_card_fusion(self, game:GameSession, pokemon_id1:int, pokemon_id2:int):
        tag = 'fusion'
        card = self.cards.get(tag)

        if not self.check_card_conditions(game, card):
            return {}

        if len(game.pokemon_box)<2:
            return {}

        # obtener pokemon
        pokemon = self.pokemon.get_random_pokemon(
            game,
            save=True
        )
        if not pokemon:
            return {}

        # borrar pokemons
        self.db_rolls.delete_roll(game.game_id, pokemon_id1)
        self.db_rolls.delete_roll(game.game_id, pokemon_id2)

        self.buy_card(game, card)

        return pokemon

    def use_card_intercambio(self, game:GameSession, pokemon_id:int):
        tag = 'intercambio'
        card = self.cards.get(tag)

        if not self.check_card_conditions(game, card):
            return {}

        if len(game.pokemon_box)==0:
            return {}

        # obtener pokemon
        pokemon = self.pokemon.get_random_pokemon(
            game,
            save=True
        )
        if not pokemon:
            return {}

        # borrar pokemon
        self.db_rolls.delete_roll(game.game_id, pokemon_id)

        self.buy_card(game, card)

        return pokemon

    def use_card_preevo(self, game:GameSession, pokemon_id:int):
        tag = 'preevo'
        card = self.cards.get(tag)

        if not self.check_card_conditions(game, card):
            return

        if len(game.pokemon_box)==0:
            return

        pokemon = self.pokemon.db_pokemon.get_pokemon(pokemon_id)
        if not pokemon:
            return

        preevo_id = pokemon.get('evolves_from_pokemon_id')
        if preevo_id is None:
            return

        preevo = self.pokemon.db_pokemon.get_pokemon(preevo_id)

        ability_id = None
        if game.filters.random_ability:
            ability_id = self.pokemon.abilities.get_random_ability(game.filters.generation)
            preevo['random_ability_id'] = ability_id
            preevo['random_ability_name'] = self.pokemon.abilities.get_ability_name(ability_id)

        # borrar pokemon e insertar preevo
        self.db_rolls.delete_roll(game.game_id, pokemon_id)
        self.db_rolls.insert_roll(game.game_id, preevo_id, ability_id)

        self.buy_card(game, card)

        return preevo

    def use_card_comienzo(self, game:GameSession):
        tag = 'comienzo'
        card = self.cards.get(tag)

        if not self.check_card_conditions(game, card):
            return

        if abs(game.options.rolls - game.options.max_rolls) >= 18:
            return

        self.reset_rolls_and_box(game)
        self.buy_card(game, card)

    def use_card_powerhouse(self, game:GameSession):
        tag = 'powerhouse'
        card = self.cards.get(tag)

        if not self.check_card_conditions(game, card):
            return

        self.buy_card(game, card)

    def use_card_type(self, game:GameSession):
        tag = 'tipo'
        card = self.cards.get(tag)

        if not self.check_card_conditions(game, card):
            return

        self.add_tickets(game, 1)
        self.buy_card(game, card)

    def use_card_aditional(self, game:GameSession, quantity:int):
        tag = 'adicional_' + str(quantity)
        card = self.cards.get(tag)

        if not self.check_card_conditions(game, card):
            return

        self.add_rolls(game, quantity)
        self.buy_card(game, card)
