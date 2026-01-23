import pandas as pd
import random
import json


class PokemonDatabase:

    def __init__(self):
        self.df = pd.read_parquet('../data/pokemon.parquet')
        self.max_position = len(self.df)-1
        
    def get_random_pokemon(self):
        n = random.randint(0, self.max_position)
        return self.df.iloc[n].to_dict()

    def get_fullname(self, pokemon_id):
        x = self.df.loc[pokemon_id]

        species_name = x['species_name']
        form_name_text = x['form_name_text']
        
        name = species_name.capitalize()
        if(form_name_text is not None):
            name += f' ({form_name_text})'

        return name