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

class PokemonFilters:
    
    DEFAULT_GENERATION = 9

    def __init__(self,
            # filter by generation
            generation:int = DEFAULT_GENERATION,
            # filter by category
            mythical:bool = False,
            legendary:bool = False,
            sublegendary:bool = True,
            powerhouse:bool = True,
            others:bool = True,
            # filter by stage
            fully_evolved:bool = True,
            # random ability
            random_ability:bool = False
        ):
        self.generation = generation
        self.mythical = bool(mythical)
        self.legendary = bool(legendary)
        self.sublegendary = bool(sublegendary)
        self.powerhouse = bool(powerhouse)
        self.others = bool(others)
        self.fully_evolved = bool(fully_evolved)
        self.random_ability = bool(random_ability)

class PokemonBox:
    
    def __init__(self, pokemons:dict, advanced:bool=False):
        self.box = pokemons
        self.advanced = advanced

    def reset(self):
        self.box = {}

class GameSession:
    
    def __init__(self, 
            game_id:int,
            user_id:int,
            gamename:str, 
            options:GameOptions = None, 
            filters:PokemonFilters = None,
            pokemon_box:PokemonBox = None,
            used_cards:dict = None
        ):
        self.game_id = game_id
        self.user_id = user_id
        self.gamename = gamename
        self.options = options if options else GameOptions()
        self.filters = filters if filters else PokemonFilters()
        self.pokemon_box = pokemon_box if pokemon_box else PokemonBox()
        self.used_cards = used_cards if used_cards else {}

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
