import random
import pandas as pd

from scripts.filters import PokemonFiltersManager


class PokemonDatabaseManager:

    def __init__(self):
        self.df = pd.read_parquet('../data/pokemon.parquet')
        self.df_filtered = None
        self.filter_manager = PokemonFiltersManager()
        self.filter_dataset()

    def get_fullname(self, pokemon_id):
        pokemon = self.df.loc[pokemon_id]

        species_name = pokemon['species_name']
        form_name_text = pokemon['form_name_text']

        name = species_name.capitalize()
        if form_name_text is not None:
            name += f' ({form_name_text})'

        return name

    def get_random_pokemon(self, box, mask=None):

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

        if dataframe.shape[0]==0:
            return None

        # obtener pokemon
        while True:
            n = random.randint(0, dataframe.shape[0]-1)
            pokemon = dataframe.iloc[n].to_dict()

            # comprobar que el pokemon obtenido no está ya en la caja
            if pokemon['id'] in box:
                # repetir
                continue
            else:
                return pokemon

    def filter_dataset(self):
        boolean_mask = pd.Series([ True for x in range(self.df.shape[0]) ], index=self.df.index)
        filters = self.filter_manager.filters

        # type
        if filters.filter_by_type:
            if filters.any_type:
                boolean_mask = (
                    boolean_mask & ( 
                        (self.df.first_type==filters.any_type)
                        |
                        (self.df.second_type==filters.any_type)
                    )
                )
            elif filters.first_type & filters.second_type:
                boolean_mask = (
                    boolean_mask & ( 
                        (self.df.first_type==filters.first_type)
                        &
                        (self.df.second_type==filters.second_type)
                    )
                )
            elif filters.first_type:
                boolean_mask = (
                    boolean_mask & (self.df.first_type==filters.first_type)
                )
            elif filters.second_type:
                boolean_mask = (
                    boolean_mask & (self.df.second_type==filters.first_type)
                )

        # generation
        if filters.filter_by_generation:
            boolean_mask_gens = pd.Series([ False for x in range(self.df.shape[0]) ], index=self.df.index)
            for gen in filters.generations:
                boolean_mask_gens = (
                    boolean_mask_gens | (self.df.pokemon_generation_number==gen)
                )
            boolean_mask = boolean_mask & boolean_mask_gens

        # category
        if filters.filter_by_category:
            boolean_mask_cat = pd.Series([ False for x in range(self.df.shape[0]) ], index=self.df.index)
            if filters.mythical:
                boolean_mask_cat = (
                    boolean_mask_cat | (self.df.is_mythical)
                )
            if filters.legendary:
                boolean_mask_cat = (
                    boolean_mask_cat | (self.df.is_legendary)
                )
            if filters.sublegendary:
                boolean_mask_cat = (
                    boolean_mask_cat | (self.df.is_sublegendary)
                )
            if filters.powerhouse:
                boolean_mask_cat = (
                    boolean_mask_cat | (self.df.is_powerhouse)
                )
            if filters.others:
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
        if filters.fully_evolved:
            boolean_mask = (
                boolean_mask & (self.df.evolutions_ids.apply(len)==0)
            )

        # transformation
        if filters.has_mega:
            boolean_mask = (
                boolean_mask & (self.df.has_mega)
            )
        if filters.has_gmax:
            boolean_mask = (
                boolean_mask & (self.df.has_gmax)
            )

        # nuevo conjunto de datos filtrados
        self.df_filtered = self.df.loc[boolean_mask]

    # def deactivate_filters(self):
    #     self.dfFiltered = None
