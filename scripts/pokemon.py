import random
import pandas as pd

import scripts.constants as const
from scripts.filters import PokemonFilters


class PokemonDatabaseManager:

    def __init__(self):
        self.df = pd.read_parquet(const.DF_POKEMON_PATH)
        self.df_filtered = None
        self.abilities = pd.read_parquet(const.DF_ABILITIES_PATH)
        self.abilities_filtered = None

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
            if self.df_filtered.shape[0]==0:
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

    def filter_dataset(self, filters:PokemonFilters):
        dataframe = self.df

        # type
        # if filters.filter_by_type:
        #     if filters.any_type:
        #         mask = (
        #             (dataframe.first_type==filters.any_type)
        #             |
        #             (dataframe.second_type==filters.any_type)
        #         )
        #         dataframe = dataframe.loc[mask]
        #     elif filters.first_type and filters.second_type:
        #         mask = (
        #             (dataframe.first_type==filters.first_type)
        #             &
        #             (dataframe.second_type==filters.second_type)
        #         )
        #         dataframe = dataframe.loc[mask]
        #     elif filters.first_type:
        #         mask = dataframe.first_type==filters.first_type
        #         dataframe = dataframe.loc[mask]
        #     elif filters.second_type:
        #         mask = dataframe.second_type==filters.second_type
        #         dataframe = dataframe.loc[mask]

        # generation
        if filters.generation != PokemonFilters.DEFAULT_GENERATION:
            mask = dataframe.pokemon_generation_number.apply(lambda x : x <= filters.generation)
            dataframe = dataframe.loc[mask]

        # evolved
        if filters.fully_evolved:
            mask = dataframe.evolutions_ids.apply(len)==0
            dataframe = dataframe.loc[mask]

        # transformation
        # if filters.has_mega:
        #     mask = dataframe.has_mega
        #     dataframe = dataframe.loc[mask]

        # if filters.has_gmax:
        #     mask = dataframe.has_gmax
        #     dataframe = dataframe.loc[mask]

        # category
        mask = pd.Series([False] * dataframe.shape[0], index=dataframe.index)
        if filters.mythical:
            mask = (
                mask | (dataframe.is_mythical)
            )
        if filters.legendary:
            mask = (
                mask | (dataframe.is_legendary)
            )
        if filters.sublegendary:
            mask = (
                mask | (dataframe.is_sublegendary)
            )
        if filters.powerhouse:
            mask = (
                mask | (dataframe.is_powerhouse)
            )
        if filters.others:
            mask = (
                mask | 
                (
                    (~dataframe.is_mythical) &
                    (~dataframe.is_legendary) &
                    (~dataframe.is_sublegendary) &
                    (~dataframe.is_powerhouse)
                )
            )
        dataframe = dataframe.loc[mask]

        # filtrar habilidades
        if filters.random_ability:
            self.filter_abilities(filters.generation)

        # nuevo conjunto de datos filtrados
        self.df_filtered = dataframe

    def filter_abilities(self, generation:int):
        dataframe = self.abilities
        mask = dataframe.generation.apply(lambda x : x <= generation)
        self.abilities_filtered = dataframe.loc[mask]

    def get_random_ability(self) -> dict:
        if self.abilities_filtered.shape[0]==0:
            return {}

        n = random.randint(0, self.abilities_filtered.shape[0]-1)
        row = self.abilities_filtered.iloc[n]
        return row.to_dict()

    def get_ability_name(self, ability_id:int):
        return self.abilities.loc[ability_id].ability_name

    # def deactivate_filters(self):
    #     self.dfFiltered = None
