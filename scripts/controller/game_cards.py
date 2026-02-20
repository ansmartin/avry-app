from scripts.controller.games import GamesController
from scripts.game import GameOptions, PokemonFilters, GameSession
from scripts.cards import Card, Cards

class GameCardsController:

    def __init__(self, games:GamesController):
        self.games = games
        self.cards_dict = Cards.get_all_cards()


    def check_card_conditions(self, game:GameSession, card:Card) -> bool:
        if card is None:
            return False

        if not game.can_use_card(card):
            return False

        if not game.can_spend_money(card.price):
            return False

        return True

    def buy_card(self, game:GameSession, card:Card):
        # gastar dinero
        self.games.spend_money(game, card.price)
        
        # añadir a cartas usadas
        if card.limit>0:
            self.add_used_card(game, card.tag)

    def add_used_card(self, game:GameSession, tag:str):
        uses = game.used_cards.get(tag)
        if uses is None:
            uses = 1
            self.games.cards.db_cards.insert_used_card(
                game.game_id,
                tag,
                uses
            )
        else:
            uses += 1
            self.games.cards.db_cards.update_used_card(
                game.game_id,
                tag,
                uses
            )
        game.used_cards[tag] = uses


    # Cards

    def use_card_mega(self, game:GameSession):
        tag = 'mega'
        card:Card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return {}

        mask = self.pokemon_db.df_filtered.has_mega

        pokemon = self.games.pokemon.get_random_pokemon(game)
        if not pokemon:
            return {}
        
        self.games.rolls.insert_roll(game.game_id, pokemon)

        self.buy_card(game, card)

        return pokemon

    def use_card_fusion(self, game:GameSession, pokemon_id1:int, pokemon_id2:int):
        tag = 'fusion'
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return {}

        if len(game.pokemon_box)<2:
            return {}

        # obtener pokemon
        pokemon = self.games.pokemon.get_random_pokemon(game)
        if not pokemon:
            return {}
        
        self.games.rolls.insert_roll(game.game_id, pokemon)

        # borrar pokemons
        self.games.rolls.db_rolls.delete_roll(game.game_id, pokemon_id1)
        self.games.rolls.db_rolls.delete_roll(game.game_id, pokemon_id2)

        self.buy_card(game, card)

        return pokemon

    def use_card_intercambio(self, game:GameSession, pokemon_id:int):
        tag = 'intercambio'
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return {}

        if len(game.pokemon_box)==0:
            return {}

        # obtener pokemon
        pokemon = self.games.pokemon.get_random_pokemon(game)
        if not pokemon:
            return {}
        
        self.games.rolls.insert_roll(game.game_id, pokemon)

        # borrar pokemon
        self.games.rolls.db_rolls.delete_roll(game.game_id, pokemon_id)

        self.buy_card(game, card)

        return pokemon

    def use_card_preevo(self, game:GameSession, pokemon_id:int):
        tag = 'preevo'
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return

        if len(game.pokemon_box)==0:
            return

        pokemon = self.games.pokemon.db_pokemon.get_pokemon(pokemon_id)
        if not pokemon:
            return

        preevo_id = pokemon.get('evolves_from_pokemon_id')
        if preevo_id is None:
            return

        preevo = self.games.pokemon.get_pokemon(preevo_id, game.filters)

        # borrar pokemon e insertar preevo
        self.games.rolls.db_rolls.delete_roll(game.game_id, pokemon_id)
        self.games.rolls.insert_roll(game.game_id, preevo)

        self.buy_card(game, card)

        return preevo

    def use_card_comienzo(self, game:GameSession):
        tag = 'comienzo'
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return

        if abs(game.options.rolls - game.options.max_rolls) >= 18:
            return

        self.games.reset_rolls_and_box(game)
        self.buy_card(game, card)

    def use_card_powerhouse(self, game:GameSession):
        tag = 'powerhouse'
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return

        self.buy_card(game, card)

    def use_card_type(self, game:GameSession):
        tag = 'tipo'
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return

        self.games.add_tickets(game, 1)
        self.buy_card(game, card)

    def use_card_aditional(self, game:GameSession, quantity:int):
        tag = 'adicional_' + str(quantity)
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return

        self.games.add_rolls(game, quantity)
        self.buy_card(game, card)
