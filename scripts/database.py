import random
import pandas as pd

from scripts.filters import PokemonFilters


class PokemonDatabaseManager:

    def __init__(self):
        self.df = pd.read_parquet('../data/pokemon.parquet')
        self.df_filtered = None
        self.filters = PokemonFilters()
        self.filter_dataset()

    def get_fullname(self, pokemon_id):
        pokemon = self.df.loc[pokemon_id]

        species_name = pokemon['species_name']
        form_name_text = pokemon['form_name_text']

        name = species_name.capitalize()
        if form_name_text is not None:
            name += f' ({form_name_text})'

        return name

    def get_random_pokemon(self, box_list, mask=None):

        # escoger dataframe
        if self.df_filtered is None:
            dataframe = self.df
        else:
            if len(self.df_filtered)==0:
                return None
            dataframe = self.df_filtered

        # pasar filtros adicionales
        if mask is not None:
            dataframe = dataframe.loc[mask]

        # quitar ya obtenidos
        new_mask = dataframe.id.apply(lambda x : x not in box_list)
        dataframe = dataframe.loc[new_mask]

        if dataframe.shape[0]==0:
            return None

        # obtener pokemon aleatorio
        n = random.randint(0, dataframe.shape[0]-1)
        pokemon = dataframe.iloc[n].to_dict()
        return pokemon

    def filter_dataset(self):
        boolean_mask = pd.Series( [True] * self.df.shape[0], index=self.df.index)

        # type
        if self.filters.filter_by_type:
            if self.filters.any_type:
                boolean_mask = (
                    boolean_mask & ( 
                        (self.df.first_type==self.filters.any_type)
                        |
                        (self.df.second_type==self.filters.any_type)
                    )
                )
            elif self.filters.first_type & self.filters.second_type:
                boolean_mask = (
                    boolean_mask & ( 
                        (self.df.first_type==self.filters.first_type)
                        &
                        (self.df.second_type==self.filters.second_type)
                    )
                )
            elif self.filters.first_type:
                boolean_mask = (
                    boolean_mask & (self.df.first_type==self.filters.first_type)
                )
            elif self.filters.second_type:
                boolean_mask = (
                    boolean_mask & (self.df.second_type==self.filters.first_type)
                )

        # generation
        if self.filters.filter_by_generation:
            boolean_mask_gens = pd.Series( [False] * self.df.shape[0], index=self.df.index)
            for gen in self.filters.generations:
                boolean_mask_gens = (
                    boolean_mask_gens | (self.df.pokemon_generation_number==gen)
                )
            boolean_mask = boolean_mask & boolean_mask_gens

        # category
        if self.filters.filter_by_category:
            boolean_mask_cat = pd.Series( [False] * self.df.shape[0], index=self.df.index)
            if self.filters.mythical:
                boolean_mask_cat = (
                    boolean_mask_cat | (self.df.is_mythical)
                )
            if self.filters.legendary:
                boolean_mask_cat = (
                    boolean_mask_cat | (self.df.is_legendary)
                )
            if self.filters.sublegendary:
                boolean_mask_cat = (
                    boolean_mask_cat | (self.df.is_sublegendary)
                )
            if self.filters.powerhouse:
                boolean_mask_cat = (
                    boolean_mask_cat | (self.df.is_powerhouse)
                )
            if self.filters.others:
                boolean_mask_cat = (
                    boolean_mask_cat | 
                    (
                        (~self.df.is_legendary) &
                        (~self.df.is_sublegendary) &
                        (~self.df.is_mythical) &
                        (~self.df.is_powerhouse)
                    )
                )
            boolean_mask = boolean_mask & boolean_mask_cat

        # evolved
        if self.filters.fully_evolved:
            boolean_mask = (
                boolean_mask & (self.df.evolutions_ids.apply(len)==0)
            )

        # transformation
        if self.filters.has_mega:
            boolean_mask = (
                boolean_mask & (self.df.has_mega)
            )
        if self.filters.has_gmax:
            boolean_mask = (
                boolean_mask & (self.df.has_gmax)
            )

        # nuevo conjunto de datos filtrados
        self.df_filtered = self.df.loc[boolean_mask]

    # def deactivate_filters(self):
    #     self.dfFiltered = None
