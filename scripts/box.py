class PokemonBox:

    def __init__(self):
        self.max_size = 20
        self.init_box()
    

    def init_box(self):
        self.box = []

    def is_full(self):
        return len(self.box)==self.max_size
    
    def position_is_in_range(self, position):
        return position>=0 and position<len(self.box)

    def save_pokemon(self, pokemon_id):
        if(self.is_full()):
            return False

        self.box.append(pokemon_id)
        return True

    def delete_pokemon(self, position):
        if(self.position_is_in_range(position)):
            self.box.pop(position)
            return True

        return False
    
    def get_pokemon(self, position):
        if(self.position_is_in_range(position)):
            return self.box[position]
        else:
            return None

    def get_length(self):
        return len(self.box)