import pickle

from scripts.box import PokemonBox


class User:

    def __init__(self, username):
        self.username = username
        self.pokemonBox = PokemonBox()
        self.init_variables()

    def init_variables(self):
        self.money = 10000 # default
        self.usedCards = {}

    def reset(self):
        self.pokemonBox.init_box()
        self.init_variables()


class UserSystem:

    def __init__(self):
        self.max_users = 128
        self.data_path = './data/users.p'
        self.load_data()
        self.activeUser = self.users[0]
            
    def load_data(self):
        # carga los datos guardados
        try:
            self.users = pickle.load( open(self.data_path, "rb") )

            if not isinstance(self.users, list) or not isinstance(self.users[0], User):
                raise TypeError(f"Error al cargar el archivo \"{self.data_path}\", se creará uno nuevo.")
                
        # si hay algún error, crea nuevos datos
        except:
            self.users = []
            self.add_user('admin')
            # self.save_data()

    def save_data(self):
        pickle.dump( self.users, open(self.data_path, "wb") )

    def username_available(self, username):
        for u in self.users:
            if u.username == username:
                return True
        return False

    def position_is_in_range(self, position):
        return position>=0 and position<len(self.users)

    def can_add_user(self):
        return len(self.users) < self.max_users

    def add_user(self, username):
        self.users.append(User(username))
        self.save_data()

    def add_pokemon_in_box(self, pokemon_id):
        success = self.activeUser.pokemonBox.save_pokemon(pokemon_id)
        if success:
            self.save_data()

    def delete_user(self, position):
        if self.position_is_in_range(position):
            self.users.pop(position)
            self.save_data()
            return True
        else:
            return False

    def get_user(self, position):
        if self.position_is_in_range(position):
            return self.users[position]
        else:
            return None

    def change_active_user(self, position):
        user = self.get_user(position)

        if user is None:
            return False
        else:
            self.activeUser = user
            return True

    def can_pay(self, price):
        return self.activeUser.money >= price

    def pay(self, price):
        self.activeUser.money -= price

    
        