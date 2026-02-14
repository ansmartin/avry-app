
class PokemonFilters:
    
    DEFAULT_GENERATION = 9

    def __init__(self,
            # filter by type
            # filter_by_type:bool = False,
            # first_type:str = None,
            # second_type:str = None,
            # any_type:str = None,

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
        # self.filter_by_type = bool(filter_by_type)
        # self.first_type = first_type
        # self.second_type = second_type
        # self.any_type = any_type
        self.generation = generation
        self.mythical = bool(mythical)
        self.legendary = bool(legendary)
        self.sublegendary = bool(sublegendary)
        self.powerhouse = bool(powerhouse)
        self.others = bool(others)
        self.fully_evolved = bool(fully_evolved)
        self.random_ability = bool(random_ability)
        # self.has_mega = False
        # self.has_gmax = False
