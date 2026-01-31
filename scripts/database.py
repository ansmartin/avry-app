import random
import pandas as pd

from scripts.filters import PokemonFilters


class PokemonDatabaseManager:

    def __init__(self):
        self.df = pd.read_parquet('../data/pokemon.parquet')
        self.df_filtered = None
        self.filters = PokemonFilters()
        self.filter_dataset()

    def get_fullname(self, pokemon_id:int) -> str:
        pokemon = self.df.loc[pokemon_id]

        species_name = pokemon['species_name']
        form_name_text = pokemon['form_name_text']

        name = species_name.capitalize()
        if form_name_text is not None:
            name += f' ({form_name_text})'

        return name

    def get_random_pokemon(self, box_list:list, mask=None):

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
        dataframe = self.df

        # type
        if self.filters.filter_by_type:
            if self.filters.any_type:
                mask = (
                    (dataframe.first_type==self.filters.any_type)
                    |
                    (dataframe.second_type==self.filters.any_type)
                )
                dataframe = dataframe.loc[mask]
            elif self.filters.first_type and self.filters.second_type:
                mask = (
                    (dataframe.first_type==self.filters.first_type)
                    &
                    (dataframe.second_type==self.filters.second_type)
                )
                dataframe = dataframe.loc[mask]
            elif self.filters.first_type:
                mask = dataframe.first_type==self.filters.first_type
                dataframe = dataframe.loc[mask]
            elif self.filters.second_type:
                mask = dataframe.second_type==self.filters.second_type
                dataframe = dataframe.loc[mask]

        # generation
        if self.filters.filter_by_generation and len(self.filters.generations)>0:
            mask = dataframe.pokemon_generation_number.apply(lambda x : x in self.filters.generations)
            dataframe = dataframe.loc[mask]

        # evolved
        if self.filters.fully_evolved:
            mask = dataframe.evolutions_ids.apply(len)==0
            dataframe = dataframe.loc[mask]

        # transformation
        if self.filters.has_mega:
            mask = dataframe.has_mega
            dataframe = dataframe.loc[mask]

        if self.filters.has_gmax:
            mask = dataframe.has_gmax
            dataframe = dataframe.loc[mask]

        # category
        if self.filters.filter_by_category:
            mask = pd.Series([False] * dataframe.shape[0], index=dataframe.index)
            if self.filters.mythical:
                mask = (
                    mask | (dataframe.is_mythical)
                )
            if self.filters.legendary:
                mask = (
                    mask | (dataframe.is_legendary)
                )
            if self.filters.sublegendary:
                mask = (
                    mask | (dataframe.is_sublegendary)
                )
            if self.filters.powerhouse:
                mask = (
                    mask | (dataframe.is_powerhouse)
                )
            if self.filters.others:
                mask = (
                    mask | 
                    (
                        (~dataframe.is_legendary) &
                        (~dataframe.is_sublegendary) &
                        (~dataframe.is_mythical) &
                        (~dataframe.is_powerhouse)
                    )
                )
            dataframe = dataframe.loc[mask]

        # nuevo conjunto de datos filtrados
        self.df_filtered = dataframe

    # def deactivate_filters(self):
    #     self.dfFiltered = None
