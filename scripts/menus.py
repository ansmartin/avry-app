from os import system
from numpy import isnan

from scripts.users import UserSystem
from scripts.game import GameSessionManager
from scripts.database import PokemonDatabaseManager
from scripts.cards import CardManager


def clear():
    system("clear||cls")

def capitalize_name(text):
    words = text.split('-')
    return '-'.join(w.capitalize() for w in words)

def capitalize_all_words(text):
    words = text.replace('-',' ').split()
    return ' '.join(w.capitalize() for w in words)


class MenuManager():

    def __init__(self, user_system : UserSystem, game_manager : GameSessionManager, database : PokemonDatabaseManager, card_manager : CardManager):
        self.user_system = user_system
        self.game_manager = game_manager
        self.database = database
        self.card_manager = card_manager


    TEXT_LINE = '\n------------------------------------'

    TEXT_MENU_MANAGE_USERS = """\n
        Opciones:
        - 1: Cargar usuario
        - 2: Crear nuevo usuario
        - 3: Eliminar usuario

        - 0: Cerrar aplicación
    """

    TEXT_MENU_MANAGE_GAMES = """\n
        Opciones:
        - 1: Cargar sesión de juego
        - 2: Crear nueva sesión de juego
        - 3: Eliminar sesión de juego

        - 0: Volver al menú de usuarios
    """

    TEXT_MENU_PLAY_GAME = """\n
        Opciones:
        - 1: Realizar tirada
        - 2: Comprar ventaja
        - 3: Reiniciar partida
        - 4: Mostrar filtros activos

        - 9: Elegir otra sesión de juego
        - 0: Cerrar aplicación
    """
    TEXT_MENU_PLAY_GAME = TEXT_LINE + TEXT_MENU_PLAY_GAME + TEXT_LINE


    def print_active_user(self):
        print(f'\nUsuario: {self.user_system.active_user.username}')

    def print_game_info(self):
        print(f'\nSesión de juego: {self.game_manager.game.name}')

        print(f'\n   Datos de la sesión de juego')
        print(f'      Tiradas restantes: {self.game_manager.game.rolls}')
        print(f'      Tiquets: {self.game_manager.game.tickets}')
        print(f'      Dinero: {self.game_manager.game.money}')
        print(f'      Puntos de items: {self.game_manager.game.item_points}')

    def print_box(self):
        box = self.game_manager.game.box.poke_list

        if len(box)==0:
            print(f'\nLa lista de Pokémon obtenidos está vacía.')
        else:
            print(f'\nLista de Pokémon obtenidos:')
            n=1
            for pokemon_id in box:
                if(pokemon_id):
                    print(f' - {n}:\t{self.database.get_fullname(pokemon_id)}')
                else:
                    print(f' - {n}:\t*')
                n+=1

    def print_pokemon(self, pokemon : dict):

        species_name = pokemon['species_name']
        form_name_text = pokemon['form_name_text']

        pokemon_generation_number = pokemon['pokemon_generation_number']

        first_type = pokemon['first_type']
        second_type = pokemon['second_type']

        first_ability = pokemon['first_ability']
        second_ability = pokemon['second_ability']
        hidden_ability = pokemon['hidden_ability']

        sprite_default = pokemon['sprite_default']

        print('\nPokémon obtenido:')

        name = f'\tNombre: {species_name.capitalize()}'
        if(form_name_text is not None):
            name += f' ({form_name_text})'
        print(name)

        print(f'\tGeneración: {pokemon_generation_number}')
        
        types = f'\tTipo: {first_type.capitalize()}'
        if(second_type is not None):
            types += f' / {second_type.capitalize()}'
        print(types)
        
        abilities = f'\tHabilidad: {capitalize_all_words(first_ability)}'
        if(second_ability is not None):
            abilities += f' / {capitalize_all_words(second_ability)}'
        print(abilities)

        if(hidden_ability is not None):
            print(f'\tHabilidad oculta: {capitalize_all_words(hidden_ability)}')

        print(f'\tIlustración: {sprite_default}')


    # def box_is_full(self):
    #     if self.game_manager.game.box.is_full():
    #         maxSizeBox = self.game_manager.game.box.max_size
    #         print(f'\nSe ha alcanzado el límite de Pokémon en la caja ({maxSizeBox}/{maxSizeBox}). No se pueden obtener más Pokémon.')
    #         return True

    def get_pokemon(self, mask=None):
        pokemon = self.database.get_random_pokemon(self.game_manager.game.box.poke_list, mask)

        if pokemon is None:
            print('\nNingún Pokémon cumple con los criterios de búsqueda.')
            return False
        
        # mostrar y guardar pokemon
        self.print_pokemon(pokemon)
        self.game_manager.add_pokemon_in_box(pokemon['id'])


    def open_menu_users(self):

        clear()

        while(True):
            self.print_users()

            print(MenuManager.TEXT_MENU_MANAGE_USERS)

            print('\nEscribe el número de la opción:')
            option = input()
            clear()

            print(f'\nSeleccionada opción {option}')

            #- 1: Cargar usuario
            if(option=='1'):
                
                if len(self.user_system.usernames_list)==0:
                    print('No hay usuarios registrados.')
                    continue

                self.print_users()

                while(True):
                    print('\nEscribe el número del usuario que quieres cargar:')
                    option = input()

                    try:
                        n = int(option)
                        n-=1
                    except:
                        print('Número no reconocido.')
                        continue

                    # cargar usuario
                    if self.user_system.change_user(n):
                        self.open_menu_user_active()
                        break
                    else:
                        print('Usuario no encontrado.')

            #- 2: Crear nuevo usuario
            elif(option=='2'):
                self.print_users()

                if self.user_system.can_add_user():
                    print('\nEscribe un nombre para el nuevo usuario:')

                    while True:
                        name = input()

                        if not self.user_system.name_is_available(name):
                            print('\nEse nombre ya se encuentra en la base de datos, escribe otro diferente:')
                            continue
                        
                        self.user_system.add_user(name)
                        clear()
                        break

                else:
                    print('La lista de usuarios está llena, borra alguno para hacer hueco.')

            #- 3: Eliminar usuario
            elif(option=='3'):

                if len(self.user_system.usernames_list)==0:
                    print('No hay usuarios registrados.')
                    continue

                self.print_users()

                print('\nEscribe el número del usuario que quieres eliminar.\nEscribe 0 para cancelar.')

                while(True):
                    option = input()

                    if option == '0':
                        clear()
                        break

                    try:
                        n = int(option)
                        n-=1
                    except:
                        print('Número no reconocido.')
                        continue

                    # if not self.user_system.position_is_in_range(n):
                    #     print('Usuario no encontrado.')
                    #     continue

                    # if self.user_system.active_user.username == self.user_system.usernames_list[n]:
                    #     print('No puedes borrar el usuario activo. Elige otro.')
                    #     continue

                    if self.user_system.remove_user(n):
                        clear()
                        break
                    else:
                        print('Usuario no encontrado.')

            #- 0: Salir
            elif(option=='0'):
                clear()
                return
            else:
                print('Opción no reconocida.')


    def print_users(self):
        print('\nUsuarios registrados:')
        for n, username in enumerate(self.user_system.usernames_list):
            print(f' - {n+1}:\t{username}')

    def print_games(self):
        print('\nSesiones de juego registradas:')
        for n, gamename in enumerate(self.user_system.active_user.games):
            print(f' - {n+1}:\t{gamename}')


    def open_menu_user_active(self):

        clear()

        while(True):
            self.print_active_user()

            if len(self.user_system.active_user.games)==0:
                print('\nEste usuario todavía no tiene sesiones de juego registradas.')
            else:
                self.print_games()

            print(MenuManager.TEXT_MENU_MANAGE_GAMES)

            print('\nEscribe el número de la opción:')
            option = input()
            clear()

            print(f'\nSeleccionada opción {option}')

            #- 1: Cargar sesión de juego
            if(option=='1'):
                
                if len(self.user_system.active_user.games)==0:
                    print('No hay sesiones de juego registradas.')
                    continue

                self.print_games()

                while(True):
                    print('\nEscribe el número de la sesión de juego que quieres cargar:')
                    option = input()

                    try:
                        n = int(option)
                        n-=1
                    except:
                        print('Número no reconocido.')
                        continue

                    # cargar
                    if self.game_manager.change_game(n):
                        clear()
                        self.open_menu_game()
                        break
                    else:
                        print('Sesión de juego no encontrada.')

            #- 2: Crear nueva sesión de juego
            elif(option=='2'):
                if len(self.user_system.active_user.games)>0:
                    self.print_games()

                if self.game_manager.can_add_game():
                    
                    print('\nEscribe un nombre para la sesión de juego:')
                    name = input()

                    if not self.game_manager.name_is_available(name):
                        print('\nEse nombre ya se encuentra en la base de datos.')
                        continue
                    
                    print('\n¿Valores por defecto? Escribe 1 para si, escribe otra cosa para no.')
                    default = input()

                    if default=='1':
                        self.game_manager.add_game_default(name)
                        clear()
                        continue

                    print('\nEscribe el número de tiradas disponibles:')
                    rolls = input()

                    print('\nEscribe el número de tiquets disponibles:')
                    tickets = input()

                    print('\nEscribe la cantidad de dinero disponible:')
                    money = input()

                    print('\nEscribe el número de puntos de item disponibles:')
                    item_points = input()

                    self.game_manager.add_game_with_options(name, rolls, tickets, money, item_points)
                    clear()
                            
                else:
                    print('La lista de juegos está llena, borra alguno para hacer hueco.')

            #- 3: Eliminar sesión de juego
            elif(option=='3'):
                
                if len(self.user_system.active_user.games)==0:
                    print('No hay sesiones de juego registradas.')
                    continue

                self.print_games()

                print('\nEscribe el número de la sesión de juego que quieres eliminar.\nEscribe 0 para cancelar.')

                while(True):
                    option = input()

                    if option == '0':
                        clear()
                        break

                    try:
                        n = int(option)
                        n-=1  
                    except:
                        print('Número no reconocido.')
                        continue

                    # if not self.game_manager.position_is_in_range(n):
                    #     print('Sesión de juego no encontrada.')
                    #     continue

                    # if self.user_system.active_user.username == self.user_system.usernames_list[n]:
                    #     print('No puedes borrar el usuario activo. Elige otro.')
                    #     continue

                    if self.game_manager.remove_game(n):
                        clear()
                        break
                    else:
                        print('Sesión de juego no encontrada.')

            #- 0: Salir
            elif(option=='0'):
                clear()
                return
            else:
                print('Opción no reconocida.')


    def open_menu_game(self):
        while(True):
            self.print_active_user()
            self.print_game_info()
            self.print_box()
            
            print(MenuManager.TEXT_MENU_PLAY_GAME)

            print('\nEscribe el número de la opción:')
            option = input()
            clear()

            print(f'Seleccionada opción {option}')

            if(option=='1'):
                if self.game_manager.game.rolls>0:
                    self.game_manager.game.rolls-=1
                    self.get_pokemon()
            elif(option=='2'):
                self.open_menu_cards()
            elif(option=='3'):
                self.game_manager.reset_game()
                print('\nSesión de juego reiniciada.')
            elif(option=='4'):
                self.database.filter_manager.print_options()

            elif(option=='9'):
                clear()
                return
            elif(option=='0'):
                clear()
                quit()

            elif(option=='m'):
                pokemon = self.database.get_random_pokemon(self.game_manager.game.box.poke_list)
                if pokemon is not None:
                    self.print_pokemon(pokemon)
                    print('\nDictionary:')
                    for k,v in pokemon.items():
                        print(f' - {k}: {v}')
            else:
                print('Opción no reconocida.')


    def open_menu_cards(self):
        
        clear()

        while(True):
            self.print_active_user()
            print(MenuManager.TEXT_LINE)
            print('\n    Lista de cartas de ventaja:')
            n=1
            for c in self.card_manager.cards.values():
                print(f'\n    - {n}: {c.name}')
                print(f'        {c.description}')
                n+=1
                if not self.card_manager.can_use_card(c.tag, self.user_system.active_user):
                    print(f'        (AGOTADA)')
                    continue
                print(f'        Precio: {c.price}')
                if c.limit>0:
                    print(f'        Limite de usos: {c.limit}')

            print('\n    - 0: Volver al menú principal')
            print('\nEscribe el número de la opción:')

            option = input()
            clear()

            print(f'\nSeleccionada opción {option}')
            
            if(option=='1'):
                self.get_pokemon_with_card_mega()
            elif(option=='2'):
                self.print_box()
                self.get_pokemon_with_card_fusion()
            elif(option=='3'):
                self.print_box()
                self.get_pokemon_with_card_intercambio()
            elif(option=='4'):
                self.print_box()
                self.get_pokemon_with_card_preevo()
            elif(option=='5'):
                self.get_pokemon_with_card_comienzo()
            elif(option=='6'):
                print(f'NO IMPLEMENTADA TODAVÍA')
            elif(option=='7'):
                print('\nEscribe el tipo del Pokémon:')
                pokemon_type = input()
                self.get_pokemon_with_card_type(pokemon_type)
            elif(option=='8'):
                self.get_pokemon_with_card_aditional(1)
            elif(option=='9'):
                self.get_pokemon_with_card_aditional(2)
            elif(option=='10'):
                self.get_pokemon_with_card_aditional(3)
            elif(option=='11'):
                print(f'NO IMPLEMENTADA TODAVÍA')
                #get_pokemon_with_card_selectiva()
            
            #- 0: Salir
            elif(option=='0'):
                return
            else:
                print('Opción no reconocida.')
            


    def check_card_conditions(self, card):
        if card is None:
            return False

        if not self.card_manager.can_use_card(card.tag, self.user_system.active_user):
            print('\nNo puedes usar esa carta porque ya has superado su límite de usos.')
            return False

        if not self.user_system.can_pay(card.price):
            print('\nNo tienes suficiente dinero para comprar esa carta.')
            return False

        return True

    def get_pokemon_with_card_mega(self):
        tag = 'mega'
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        # if self.box_is_full():
        #     return
        
        # usar carta
        self.card_manager.add_used_card(tag, self.user_system.active_user)
        self.game_manager.pay(card.price)

        mask = self.database.df_filtered.has_mega
        
        self.get_pokemon(mask)

    def get_pokemon_with_card_fusion(self):
        tag = 'fusion'
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        if self.game_manager.game.box.get_length()<2:
            print('\nNo se puede usar porque no tienes más de 2 Pokémon.')
            return

        try:
            print('\nEscribe el número de la posición del primer Pokémon a eliminar:')
            position1 = int(input()) - 1
            print('\nEscribe el número de la posición del segundo Pokémon a eliminar:')
            position2 = int(input()) - 1
        except:
            print('\nError: Posición no detectada.')
            return
        
        if position1==position2:
            print('\nError: Las posiciones tienen que ser diferentes.')
            return

        if (
            not self.game_manager.game.box.position_is_in_range(position1) 
            or 
            not self.game_manager.game.box.position_is_in_range(position2)
        ):
            print('\nError: Posiciones no detectadas.')
            return

        # usar carta
        self.card_manager.add_used_card(tag, self.user_system.active_user)
        self.game_manager.pay(card.price)

        # ajustar segunda posicion para cuando se borre la primera
        if position1 < position2:
            position2-=1

        self.game_manager.game.box.delete_pokemon(position1)
        self.game_manager.game.box.delete_pokemon(position2)
        self.get_pokemon()

    def get_pokemon_with_card_intercambio(self):
        tag = 'intercambio'
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        if self.game_manager.game.box.get_length()==0:
            print('\nNo se puede usar porque no tienes ningún Pokémon.')
            return

        try:
            print('\nEscribe el número de la posición del Pokémon a intercambiar:')
            pokemon_position = int(input()) - 1
        except:
            print('\nError: Posición no detectada.')
            return
        
        if (
            not self.game_manager.game.box.position_is_in_range(pokemon_position) 
        ):
            print('\nError: Posición no detectada.')
            return

        # usar carta
        self.card_manager.add_used_card(tag, self.user_system.active_user)
        self.game_manager.pay(card.price)

        self.game_manager.game.box.delete_pokemon(pokemon_position)
        self.get_pokemon()

    def get_pokemon_with_card_preevo(self):
        tag = 'preevo'
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        if self.game_manager.game.box.get_length()==0:
            print('\nNo se puede usar porque no tienes ningún Pokémon.')
            return

        try:
            print('\nEscribe el número de la posición del Pokémon que quieres cambiar por su pre-evolución:')
            pokemon_position = int(input()) - 1
        except:
            print('\nError: Posición no detectada.')
            return
        
        if (
            not self.game_manager.game.box.position_is_in_range(pokemon_position) 
        ):
            print('\nError: Posición no detectada.')
            return
        
        pokemon_id = self.game_manager.game.box.get_pokemon(pokemon_position)
        preevo_id = self.database.df.loc[pokemon_id].evolves_from_pokemon_id

        if isnan(preevo_id):
            print('\nError: El Pokémon seleccionado no tiene pre-evolución.')
            return

        # usar carta
        self.card_manager.add_used_card(tag, self.user_system.active_user)
        self.game_manager.pay(card.price)
        
        self.game_manager.game.box.delete_pokemon(pokemon_position)

        #get_pokemon()
        pokemon = self.database.df.loc[preevo_id].to_dict()

        # mostrar y guardar pokemon
        self.print_pokemon(pokemon)
        self.game_manager.game.box.poke_list[pokemon_position] = preevo_id
        self.game_manager.save_file_game()

    def get_pokemon_with_card_comienzo(self):
        tag = 'comienzo'
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        if self.game_manager.game.box.get_length()>=18:
            print('\nNo se puede usar porque ya se han realizado más de 18 tiradas.')
            return

        # usar carta
        self.card_manager.add_used_card(tag, self.user_system.active_user)
        self.game_manager.pay(card.price)

        self.game_manager.game.box.init_box()
        print('\nTiradas reiniciadas.')

    def get_pokemon_with_card_type(self, pokemon_type):
        tag = 'tipo'
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        # if self.box_is_full():
        #     return

        # usar carta
        self.card_manager.add_used_card(tag, self.user_system.active_user)
        self.game_manager.pay(card.price)
        
        mask = (
            (self.database.df_filtered.first_type==pokemon_type) 
            | 
            (self.database.df_filtered.second_type==pokemon_type)
        )

        self.get_pokemon(mask)

    def get_pokemon_with_card_aditional(self, number_ad):
        tag = 'adicional_' + str(number_ad)
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        # if self.box_is_full():
        #     return

        # usar carta
        self.card_manager.add_used_card(tag, self.user_system.active_user)
        self.game_manager.pay(card.price)

        for _ in range(number_ad):
            self.get_pokemon()

    def get_pokemon_with_card_selectiva(self):
        tag = 'selectiva'
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        # if self.box_is_full():
        #     return

        # usar carta
        self.card_manager.add_used_card(tag, self.user_system.active_user)
        self.game_manager.pay(card.price)

        for _ in range(6):
            self.get_pokemon()

