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
        self.rest = False

        self.fully_evolved = False

        self.has_mega = False
        self.has_gmax = False


class PokemonFiltersManager:

    def __init__(self):
        self.data_path = './data/filters.p'
        self.load_data()

    def load_data(self):
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
