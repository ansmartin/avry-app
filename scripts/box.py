class PokemonBox:

    def __init__(self):
        self.init_box()

    def init_box(self):
        self.poke_list = []

    def position_is_in_range(self, position):
        return position>=0 and position<len(self.poke_list)

    def add_pokemon(self, pokemon_id):
        self.poke_list.append(pokemon_id)

    def delete_pokemon(self, position):
        if(self.position_is_in_range(position)):
            self.poke_list.pop(position)
            return True

        return False

    def get_pokemon(self, position):
        if(self.position_is_in_range(position)):
            return self.poke_list[position]

        return None

    def get_length(self):
        return len(self.poke_list)
