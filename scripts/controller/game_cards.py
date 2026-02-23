from scripts.controller.games import GamesController
from scripts.game import GameSession
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
        tag = Cards.TAG_MEGA
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return {}

        additional_filters = { 'has_mega':True }

        pokemon = self.games.pokemon.get_random_pokemon(game, additional_filters)
        if not pokemon:
            return {}
        
        self.games.insert_roll(game, pokemon)
        self.games.spend_roll(game)

        self.buy_card(game, card)

        return pokemon

    def use_card_fusion(self, game:GameSession, pokemon_id1:int, pokemon_id2:int):
        tag = Cards.TAG_FUSION
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return {}

        if len(game.pokemon_box.box)<2:
            return {}

        # obtener pokemon
        pokemon = self.games.pokemon.get_random_pokemon(game)
        if not pokemon:
            return {}
        
        self.games.insert_roll(game, pokemon)

        # borrar pokemons
        self.games.delete_roll(game, pokemon_id1)
        self.games.delete_roll(game, pokemon_id2)

        self.buy_card(game, card)

        return pokemon

    def use_card_intercambio(self, game:GameSession, pokemon_id:int):
        tag = Cards.TAG_INTERCAMBIO
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return {}

        if len(game.pokemon_box.box)==0:
            return {}

        if not game.pokemon_box.box.get(pokemon_id):
            return {}

        # obtener pokemon
        pokemon = self.games.pokemon.get_random_pokemon(game)
        if not pokemon:
            return {}

        self.games.insert_roll(game, pokemon)

        # borrar pokemon
        self.games.delete_roll(game, pokemon_id)

        self.buy_card(game, card)

        return pokemon

    def use_card_preevo(self, game:GameSession, pokemon_id:int):
        tag = Cards.TAG_PREEVO
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return

        if len(game.pokemon_box.box)==0:
            return

        if not game.pokemon_box.box.get(pokemon_id):
            return {}

        pokemon = self.games.pokemon.get_pokemon(pokemon_id)
        if not pokemon:
            return

        preevo_id = pokemon.get('evolves_from_pokemon_id')
        if preevo_id is None:
            return

        preevo = self.games.pokemon.get_pokemon(
            preevo_id, 
            game.filters.random_ability, 
            game.filters.generation
        )

        # borrar pokemon e insertar preevo
        self.games.delete_roll(game, pokemon_id)
        self.games.insert_roll(game, preevo)

        self.buy_card(game, card)

        return preevo

    def use_card_comienzo(self, game:GameSession):
        tag = Cards.TAG_COMIENZO
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return

        if abs(game.options.rolls - game.options.max_rolls) >= 18:
            return

        self.games.reset_rolls_and_box(game)
        self.buy_card(game, card)

    def use_card_powerhouse(self, game:GameSession):
        tag = Cards.TAG_2_POWERHOUSE
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return

        self.buy_card(game, card)

    def use_card_tiquet_tipo(self, game:GameSession):
        tag = Cards.TAG_TICKET_TIPO
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return

        self.games.add_tickets(game, 1)
        self.buy_card(game, card)

    def use_card_aditional(self, game:GameSession, quantity:int):
        tag = Cards.get_tag_adicional(quantity)
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return

        self.games.add_rolls(game, quantity)
        self.buy_card(game, card)

    def use_card_selectiva(self, game:GameSession):
        tag = Cards.TAG_SELECTIVA
        card = self.cards_dict.get(tag)

        if not self.check_card_conditions(game, card):
            return

        quantity = 6
        if game.options.rolls < (quantity-1):
            return

        pokemon_dicts_list = self.games.pokemon.get_multiple_random_pokemons(game, quantity)
        return pokemon_dicts_list

    def use_card_selectiva_final(self, game:GameSession, pokemon_dict:dict):
        tag = Cards.TAG_SELECTIVA
        card = self.cards_dict.get(tag)

        for pokemon_id,ability_id in pokemon_dict.items():
            pokemon = self.games.pokemon.get_pokemon(int(pokemon_id))
            pokemon['random_ability_id'] = int(ability_id)
            self.games.insert_roll(game, pokemon)
            self.games.spend_roll(game)

        self.buy_card(game, card)