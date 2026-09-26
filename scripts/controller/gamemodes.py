from scripts.database.gamemodes import GamemodesDatabase
from scripts.classes.game import GameProperties, PokemonFilters

class GamemodesController:
    
    def __init__(self, connection, cursor):
        self.db_gamemodes = GamemodesDatabase(connection, cursor)


    # SELECT

    def get_gamemode(self, gamemode_id:int) -> dict:
        if gamemode_id is None:
            return {}

        return self.db_gamemodes.get_gamemode(gamemode_id)

    def get_gamemode_wih_name(self, gamename:str) -> dict:
        if gamename is None:
            return {}
        
        gamemode_id = self.db_gamemodes.get_gamemode_id(gamename)
        if gamemode_id is None:
            return {}
        
        return self.get_gamemode(gamemode_id)
    
    def get_gamemode_id(self, gamename:str) -> int|None:
        return self.db_gamemodes.get_gamemode_id(gamename)

    def get_all_gamemode_names(self) -> list[str]:
        return self.db_gamemodes.get_all_gamemode_names()


    # INSERT

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

        self.db_gamemodes.insert_gamemode(
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

    def delete_gamemode(self, gamemode_id:int):
        self.db_gamemodes.delete_gamemode(gamemode_id)


    # UPDATE
