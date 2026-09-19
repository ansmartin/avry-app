from scripts.cards import Card

class GameProperties:
    
    MAX_ROLLS = 1000
    MAX_TICKETS = 1000
    MAX_MONEY = 999_999_999
    MAX_ITEM_POINTS = 999_999_999

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
        self.max_rolls = self.rolls = GameProperties.DEFAULT_ROLLS
        self.tickets = GameProperties.DEFAULT_TICKETS
        self.money = GameProperties.DEFAULT_MONEY
        self.item_points = GameProperties.DEFAULT_ITEM_POINTS

class PokemonFilters:
    
    DEFAULT_GENERATION = 9
    DEFAULT_MYTHICAL = False
    DEFAULT_LEGENDARY = False
    DEFAULT_SUBLEGENDARY = True
    DEFAULT_POWERHOUSE = True
    DEFAULT_FULLY_EVOLVED = True
    DEFAULT_RANDOM_ABILITY = False

    def __init__(self,
            # filter by generation
            generation:int = DEFAULT_GENERATION,
            # filter by category
            mythical:bool = DEFAULT_MYTHICAL,
            legendary:bool = DEFAULT_LEGENDARY,
            sublegendary:bool = DEFAULT_SUBLEGENDARY,
            powerhouse:bool = DEFAULT_POWERHOUSE,
            # filter by stage
            fully_evolved:bool = DEFAULT_FULLY_EVOLVED,
            # random ability
            random_ability:bool = DEFAULT_RANDOM_ABILITY
        ):
        self.generation = generation
        self.mythical = bool(mythical)
        self.legendary = bool(legendary)
        self.sublegendary = bool(sublegendary)
        self.powerhouse = bool(powerhouse)
        self.fully_evolved = bool(fully_evolved)
        self.random_ability = bool(random_ability)

class PokemonBox:
    
    def __init__(self, box:dict={}, advanced:bool=False):
        self.box = box
        self.advanced = advanced

    def reset(self):
        self.box = {}

class GameSession:
    
    def __init__(self, 
            game_id:int,
            user_id:int,
            gamename:str, 
            properties:GameProperties = None, 
            filters:PokemonFilters = None,
            pokemon_box:PokemonBox = None,
            used_cards:dict = None
        ):
        self.game_id = game_id
        self.user_id = user_id
        self.gamename = gamename
        self.properties = properties if properties else GameProperties()
        self.filters = filters if filters else PokemonFilters()
        self.pokemon_box = pokemon_box if pokemon_box else PokemonBox()
        self.used_cards = used_cards if used_cards else {}

    def to_dict(self) -> dict:
        game_dict = {
            'game_id' : self.game_id,
            'user_id' : self.user_id,
            'gamename' : self.gamename,
            'game_properties' : self.properties.__dict__,
            'game_filters' : self.filters.__dict__,
            'pokemon_box': self.pokemon_box.__dict__,
            'used_cards' : self.used_cards
        }
        return game_dict

    def can_spend_roll(self) -> bool:
        return self.properties.rolls > 0

    def can_spend_ticket(self) -> bool:
        return self.properties.tickets > 0

    def can_spend_money(self, price:int) -> bool:
        return self.properties.money >= price

    def can_spend_item_points(self, points:int) -> bool:
        return self.properties.item_points >= points

    def can_use_card(self, card:Card) -> bool:
        if card.limit==0: 
            # sin limite
            return True

        uses = self.used_cards.get(card.tag, 0)
        return uses < card.limit
