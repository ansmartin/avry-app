import pickle

from scripts.box import PokemonBox


class User:

    def __init__(self, username):
        self.username = username
        self.money = 10000 # default
        self.pokemonBox = PokemonBox()
        

class UserSystem:

    def __init__(self):
        self.max_users = 128
        self.data_path = './data/users.p'
        self.load_data()
            
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

    def can_add_user(self):
        if len(self.users) < self.max_users:
            return True
        else:
            return False

    def username_available(self, username):
        for user in self.users:
            if user.username == username:
                return True
        return False

    def position_is_in_range(self, position):
        return position>=0 and position<len(self.users)

    def add_user(self, username):
        self.users.append(User(username))
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


    
        