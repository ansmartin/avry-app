import pandas as pd
import random

from scripts.filters import PokemonFiltersManager


class PokemonDatabaseManager:

    def __init__(self):
        self.df = pd.read_parquet('../data/pokemon.parquet')
        self.size = self.df.shape[0]
        self.max_position = self.size-1
        self.filterManager = PokemonFiltersManager()
        self.df_filtered = None

    def get_fullname(self, pokemon_id):
        x = self.df.loc[pokemon_id]

        species_name = x['species_name']
        form_name_text = x['form_name_text']
        
        name = species_name.capitalize()
        if(form_name_text is not None):
            name += f' ({form_name_text})'

        return name
        
    def get_random_pokemon(self):
        if self.df_filtered is None:
            n = random.randint(0, self.max_position)
            return self.df.iloc[n].to_dict()
        else:
            if(len(self.df_filtered)==0):
                return None
            n = random.randint(0, self.df_filtered.shape[0]-1)
            return self.df_filtered.iloc[n].to_dict()

    def filter_dataset(self):
        booleanIndex = pd.Series([ True for x in range(self.size) ])
        filters = self.filterManager.filters

        # type
        if filters.filter_by_type:
            if filters.any_type:
                booleanIndex = (
                    booleanIndex & ( 
                        (self.df.first_type==filters.any_type)
                        |
                        (self.df.second_type==filters.any_type)
                    )
                )
            elif filters.first_type & filters.second_type:
                booleanIndex = (
                    booleanIndex & ( 
                        (self.df.first_type==filters.first_type)
                        &
                        (self.df.second_type==filters.second_type)
                    )
                )
            elif filters.first_type:
                booleanIndex = (
                    booleanIndex & (self.df.first_type==filters.first_type)
                )
            elif filters.second_type:
                booleanIndex = (
                    booleanIndex & (self.df.second_type==filters.first_type)
                )
        
        # generation
        if filters.filter_by_generation:
            booleanIndex_gens = pd.Series([ False for x in range(self.size) ])
            for gen in filters.generations:
                booleanIndex_gens = (
                    booleanIndex_gens | (self.df.pokemon_generation_number==gen)
                )
            booleanIndex = booleanIndex & booleanIndex_gens

        # specifics
        if not filters.show_all_pokemon:
            booleanIndex_aux = pd.Series([ False for x in range(self.size) ])
            if filters.fully_evolved:
                booleanIndex_aux = (
                    booleanIndex_aux | (self.df.evolutions_ids.apply(len)==0)
                )
            if filters.powerhouse:
                booleanIndex_aux = (
                    booleanIndex_aux | (self.df.is_powerhouse)
                )
            if filters.legendary:
                booleanIndex_aux = (
                    booleanIndex_aux | (self.df.is_legendary)
                )
            if filters.sublegendary:
                booleanIndex_aux = (
                    booleanIndex_aux | (self.df.is_sublegendary)
                )
            if filters.mythical:
                booleanIndex_aux = (
                    booleanIndex_aux | (self.df.is_mythical)
                )
            if filters.has_mega:
                booleanIndex_aux = (
                    booleanIndex_aux | (self.df.has_mega)
                )
            if filters.has_gmax:
                booleanIndex_aux = (
                    booleanIndex_aux | (self.df.has_gmax)
                )
            booleanIndex = booleanIndex & booleanIndex_aux

        # nuevo conjunto de datos filtrados
        self.df_filtered = self.df.loc[booleanIndex]

    def deactivate_filters(self):
        self.df_filtered = None
        self.filterManager.reset()