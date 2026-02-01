
class PokemonFilters:
    
    DEFAULT_GENERATION = 9

    def __init__(self,
            # filter by type
            filter_by_type:bool = False,
            first_type:str = None,
            second_type:str = None,
            any_type:str = None,

            # filter by generation
            generation:int = DEFAULT_GENERATION,

            # filter by category
            mythical:bool = False,
            legendary:bool = False,
            sublegendary:bool = True,
            powerhouse:bool = True,
            others:bool = True,

            # filter by stage
            fully_evolved:bool = True
        ):
        self.filter_by_type = filter_by_type
        self.first_type = first_type
        self.second_type = second_type
        self.any_type = any_type
        self.generation = generation
        self.mythical = mythical
        self.legendary = legendary
        self.sublegendary = sublegendary
        self.powerhouse = powerhouse
        self.others = others
        self.fully_evolved = fully_evolved
        # self.has_mega = False
        # self.has_gmax = False
        # self.random_ability_same_pokemon = False
        # self.random_ability_any_pokemon = False


    def print_options(self):
        print('\nFiltros:')

        print(f' - filtrar por tipo: {self.filter_by_type}')
        if self.filter_by_type:
            print(f'   - first_type: {self.first_type}')
            print(f'   - second_type: {self.second_type}')
            print(f'   - any_type: {self.any_type}')

        print(f' - filtrar por generación')
        print(f'   - obtener Pokémon hasta la generación: {self.generation}')
            
        print(f' - filtrar por categoría')
        print(f'   - mythical: {self.mythical}')
        print(f'   - legendary: {self.legendary}')
        print(f'   - sublegendary: {self.sublegendary}')
        print(f'   - powerhouse: {self.powerhouse}')
        print(f'   - el resto de Pokémon: {self.others}')

        print(f' - obtener sólo Pokémon completamente evolucionados: {self.fully_evolved}')

        # print(f' - obtener sólo Pokémon que puedan mega-evolucionar: {self.has_mega}')
        # print(f' - obtener sólo Pokémon que puedan gigamaxizar: {self.has_gmax}')
