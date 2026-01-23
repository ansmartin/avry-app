class PokemonBox:

    def __init__(self):
        self.size = 20
        self.max_position = self.size-1
        self.init_box()
    

    def init_box(self):
        self.box = [ None for n in range(self.size) ]
        self.number_of_pokemon_stored = 0

    def is_full(self):
        return self.number_of_pokemon_stored==self.size
    
    def position_is_in_range(self, position):
        return position>=0 and position<self.size


    def save_pokemon(self, pokemon_id):
        if(self.is_full()):
            return False

        for n in range(self.size):
            if(self.box[n] is None):
                self.box[n] = pokemon_id
                self.number_of_pokemon_stored+=1
                return True

        return False

    def delete_pokemon(self, position):
        if(self.position_is_in_range(position)):
            if(self.box[position]):
                self.box[position] = None
                self.number_of_pokemon_stored-=1
                return True

        return False
    
    def get_pokemon(self, position):
        if(self.position_is_in_range(position)):
            return self.box[position]
        else:
            return None

    def get_box(self):
        if(self.number_of_pokemon_stored==0):
            return None
        else:
            return self.box
