import random

from scripts.database.abilities import AbilitiesDatabase

class AbilitiesController:

    def __init__(self, connection, cursor):
        self.db_abilities = AbilitiesDatabase(connection, cursor)


    # GET

    def get_random_ability(self, generation:int) -> int|None:
        abilities_ids = self.db_abilities.get_abilities(generation)
        if not abilities_ids:
            return None

        n = random.randint(0, len(abilities_ids)-1)
        ability = abilities_ids[n]
        return ability

    def get_ability_name(self, ability_id:int) -> str|None:
        if ability_id is None:
            return None

        ability_name = self.db_abilities.get_ability_name(ability_id)
        return ability_name
