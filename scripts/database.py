import pandas as pd
import random

from scripts.filters import PokemonFiltersManager


class PokemonDatabaseManager:

    def __init__(self):
        self.df = pd.read_parquet('../data/pokemon.parquet')
        self.size = self.df.shape[0]
        self.max_position = self.size-1
        self.filterManager = PokemonFiltersManager()
        self.dfFiltered = None
        self.filter_dataset()

    def get_fullname(self, pokemon_id):
        x = self.df.loc[pokemon_id]

        species_name = x['species_name']
        form_name_text = x['form_name_text']
        
        name = species_name.capitalize()
        if(form_name_text is not None):
            name += f' ({form_name_text})'

        return name
        
    def get_random_pokemon(self, box):
        while True:
            
            if self.dfFiltered is None:
                n = random.randint(0, self.max_position)
                pokemon = self.df.iloc[n].to_dict()
            else:
                if(len(self.dfFiltered)==0):
                    return None
                n = random.randint(0, self.dfFiltered.shape[0]-1)
                pokemon = self.dfFiltered.iloc[n].to_dict()

            # comprobar que el pokemon obtenido no está ya en la caja
            if pokemon['id'] in box:
                # repetir
                continue
            else:
                return pokemon

    def filter_dataset(self):
        booleanMask = pd.Series([ True for x in range(self.size) ], index=self.df.index)
        filters = self.filterManager.filters

        # type
        if filters.filter_by_type:
            if filters.any_type:
                booleanMask = (
                    booleanMask & ( 
                        (self.df.first_type==filters.any_type)
                        |
                        (self.df.second_type==filters.any_type)
                    )
                )
            elif filters.first_type & filters.second_type:
                booleanMask = (
                    booleanMask & ( 
                        (self.df.first_type==filters.first_type)
                        &
                        (self.df.second_type==filters.second_type)
                    )
                )
            elif filters.first_type:
                booleanMask = (
                    booleanMask & (self.df.first_type==filters.first_type)
                )
            elif filters.second_type:
                booleanMask = (
                    booleanMask & (self.df.second_type==filters.first_type)
                )
        
        # generation
        if filters.filter_by_generation:
            booleanMask_gens = pd.Series([ False for x in range(self.size) ], index=self.df.index)
            for gen in filters.generations:
                booleanMask_gens = (
                    booleanMask_gens | (self.df.pokemon_generation_number==gen)
                )
            booleanMask = booleanMask & booleanMask_gens

        # category
        if filters.filter_by_category:
            booleanMask_cat = pd.Series([ False for x in range(self.size) ], index=self.df.index)
            if filters.mythical:
                booleanMask_cat = (
                    booleanMask_cat | (self.df.is_mythical)
                )
            if filters.legendary:
                booleanMask_cat = (
                    booleanMask_cat | (self.df.is_legendary)
                )
            if filters.sublegendary:
                booleanMask_cat = (
                    booleanMask_cat | (self.df.is_sublegendary)
                )
            if filters.powerhouse:
                booleanMask_cat = (
                    booleanMask_cat | (self.df.is_powerhouse)
                )
            if filters.others:
                booleanMask_cat = (
                    booleanMask_cat | 
                    (
                        (~self.df.is_legendary) &
                        (~self.df.is_sublegendary) &
                        (~self.df.is_mythical) &
                        (~self.df.is_powerhouse)
                    )
                )
            booleanMask = booleanMask & booleanMask_cat

        # evolved
        if filters.fully_evolved:
            booleanMask = (
                booleanMask & (self.df.evolutions_ids.apply(len)==0)
            )

        # transformation
        if filters.has_mega:
            booleanMask = (
                booleanMask & (self.df.has_mega)
            )
        if filters.has_gmax:
            booleanMask = (
                booleanMask & (self.df.has_gmax)
            )

        # nuevo conjunto de datos filtrados
        self.dfFiltered = self.df.loc[booleanMask]

    def deactivate_filters(self):
        self.dfFiltered = None