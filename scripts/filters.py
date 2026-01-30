
class PokemonFilters:

    def __init__(self):
        self.filter_by_type = False
        self.first_type = None
        self.second_type = None
        self.any_type = None

        #self.random_ability_same_pokemon = False
        #self.random_ability_any_pokemon = False

        self.filter_by_generation = False
        self.generations = [1,2,3,4,5,6,7,8,9]

        self.filter_by_category = True
        self.mythical = False
        self.legendary = False
        self.sublegendary = True
        self.powerhouse = True
        self.others = True

        self.fully_evolved = True

        self.has_mega = False
        self.has_gmax = False


    def print_options(self):
        print('\nFiltros:')

        print(f' - filtrar por tipo: {self.filter_by_type}')
        if self.filter_by_type:
            print(f' - first_type: {self.first_type}')
            print(f' - second_type: {self.second_type}')
            print(f' - any_type: {self.any_type}')

        print(f' - filtrar por generación: {self.filter_by_generation}')
        if self.filter_by_generation:
            print(f' - generations: {self.generations}')
            
        print(f' - filtrar por categoría: {self.filter_by_category}')
        if self.filter_by_category:
            print(f'   - mythical: {self.mythical}')
            print(f'   - legendary: {self.legendary}')
            print(f'   - sublegendary: {self.sublegendary}')
            print(f'   - powerhouse: {self.powerhouse}')
            print(f'   - el resto de Pokémon: {self.others}')

        print(f' - obtener sólo Pokémon completamente evolucionados: {self.fully_evolved}')
        print(f' - obtener sólo Pokémon que puedan mega-evolucionar: {self.has_mega}')
        print(f' - obtener sólo Pokémon que puedan gigamaxizar: {self.has_gmax}')
