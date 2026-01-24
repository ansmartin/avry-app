import pickle


class PokemonFilters:
    def __init__(self):
        self.reset()

    def reset(self):
        self.filter_by_type = False
        self.first_type = None
        self.second_type = None
        self.any_type = None

        #self.random_ability_same_pokemon = False
        #self.random_ability_any_pokemon = False

        self.filter_by_generation = False
        self.generations = None

        self.show_all_pokemon = True
        self.legendary = False
        self.sublegendary = False
        self.mythical = False
        self.powerhouse = False
        self.others = False

        self.fully_evolved = True

        self.has_mega = False
        self.has_gmax = False


class PokemonFiltersManager:

    def __init__(self):
        self.read_options_file = False
        self.data_path = './data/filters.p'
        self.load_data()

    def load_data(self):
        if not self.read_options_file:
            self.filters = PokemonFilters()
            return

        # carga los datos guardados
        try:
            self.filters = pickle.load( open(self.data_path, "rb") )
            
            if not isinstance(self.filters, PokemonFilters):
                raise TypeError(f"Error al cargar el archivo \"{self.data_path}\", se creará uno nuevo.")

        # si hay algún error, crea nuevos datos
        except:
            self.filters = PokemonFilters()
            self.save_data()

    def save_data(self):
        pickle.dump( self.filters, open(self.data_path, "wb") )

    
    def print_options(self):
        print('\nFiltros:')

        print(f' - filtrar por tipo: {self.filters.filter_by_type}')
        if self.filters.filter_by_type:
            print(f' - first_type: {self.filters.first_type}')
            print(f' - second_type: {self.filters.second_type}')
            print(f' - any_type: {self.filters.any_type}')

        print(f' - filtrar por generación: {self.filters.filter_by_generation}')
        if self.filters.filter_by_generation:
            print(f' - generations: {self.filters.generations}')
            
        print(f' - filtrar por categoría: {not self.filters.show_all_pokemon}')
        if not self.filters.show_all_pokemon:
            print(f' - legendary: {self.filters.legendary}')
            print(f' - sublegendary: {self.filters.sublegendary}')
            print(f' - mythical: {self.filters.mythical}')
            print(f' - powerhouse: {self.filters.powerhouse}')
            print(f' - el resto de Pokémon: {self.filters.others}')

        print(f' - obtener sólo Pokémon completamente evolucionados: {self.filters.fully_evolved}')
        print(f' - obtener sólo Pokémon que puedan mega-evolucionar: {self.filters.has_mega}')
        print(f' - obtener sólo Pokémon que puedan gmaxizar: {self.filters.has_gmax}')
        
