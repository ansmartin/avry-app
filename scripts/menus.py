from os import system

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


    line = '\n------------------------------------'

    text_menu_users = """\n
        Opciones:
        - 1: Cargar usuario
        - 2: Crear nuevo usuario
        - 3: Eliminar usuario

        - 0: Cerrar aplicación
    """

    text_menu_user_active = """\n
        Opciones:
        - 1: Cargar sesión de juego
        - 2: Crear nueva sesión de juego
        - 3: Eliminar sesión de juego

        - 0: Volver al menú de usuarios
    """

    text_menu = """
        Opciones:
        - 1: Realizar tirada
        - 2: Ver caja
        - 3: Reiniciar caja
        - 4: Mostrar filtros activos
        - 5: Usar carta de ventaja

        - 9: Elegir otra sesión de juego
        - 0: Cerrar aplicación
    """
    text_menu = line + text_menu + line


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
        maxSizeBox = self.game_manager.game.box.max_size

        print(f'\nLista de Pokémon obtenidos: {self.game_manager.game.box.get_length()}/{maxSizeBox}')

        if len(box)>0:
            n=1
            for pokemon_id in box:
                if(pokemon_id):
                    print(f' - {n}:\t{self.database.get_fullname(pokemon_id)}')
                else:
                    print(f' - {n}:\t*')
                n+=1

    def print_pokemon(self, pokemon):

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


    def box_is_full(self):
        if self.game_manager.game.box.is_full():
            maxSizeBox = self.game_manager.game.box.max_size
            print(f'\nSe ha alcanzado el límite de Pokémon en la caja ({maxSizeBox}/{maxSizeBox}). No se pueden obtener más Pokémon.')
            return True

    def get_pokemon(self, mask=None):
        # if box_is_full():
        #     return

        pokemon = self.database.get_random_pokemon(self.game_manager.game.box.poke_list, mask)

        if pokemon is None:
            print('\nNingún Pokémon cumple con los criterios de búsqueda.')
            return False
        
        # mostrar y guardar pokemon
        self.print_pokemon(pokemon)
        self.game_manager.add_pokemon_in_box(pokemon['id'])
        return True


    def open_menu_users(self):

        clear()

        while(True):
            self.print_users()

            print(MenuManager.text_menu_users)

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
                    print('\nEscribe un nombre para el usuario:')

                    while True:
                        name = input()
                        if self.user_system.add_user(name):
                            clear()
                            break
                        else:
                            print('\nEse nombre ya se encuentra en la base de datos, escribe otro diferente:')

                else:
                    print('La lista de usuarios está llena, borra alguno para hacer hueco.')

            #- 3: Eliminar usuario
            elif(option=='3'):
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

                    if not self.user_system.position_is_in_range(n):
                        print('Usuario no encontrado.')
                        continue

                    # if self.user_system.active_user.username == self.user_system.usernames_list[n]:
                    #     print('No puedes borrar el usuario activo. Elige otro.')
                    #     continue

                    if self.user_system.delete_user(n):
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
            print('')
            self.print_games()

            print(MenuManager.text_menu_user_active)

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
                self.print_games()

                if self.game_manager.can_add_game():
                    print('\nEscribe un nombre para la sesión de juego:')

                    while True:
                        name = input()
                        if self.game_manager.add_game(name):
                            clear()
                            break
                        else:
                            print('\nEse nombre ya se encuentra en la base de datos, escribe otro diferente:')

                else:
                    print('La lista de juegos está llena, borra alguno para hacer hueco.')

            #- 3: Eliminar sesión de juego
            elif(option=='3'):
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

                    if not self.game_manager.position_is_in_range(n):
                        print('Sesión de juego no encontrada.')
                        continue

                    # if self.user_system.active_user.username == self.user_system.usernames_list[n]:
                    #     print('No puedes borrar el usuario activo. Elige otro.')
                    #     continue

                    if self.game_manager.delete_game(n):
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
            
            print(MenuManager.text_menu)

            print('\nEscribe el número de la opción:')
            option = input()
            clear()

            print(f'Seleccionada opción {option}')

            if(option=='1'):
                if self.game_manager.game.rolls>0:
                    if self.get_pokemon():
                        self.game_manager.game.rolls-=1
            elif(option=='2'):
                self.open_menu_cards()

            elif(option=='3'):
                empty_box()
            elif(option=='4'):
                database.filter_manager.print_options()

            elif(option=='9'):
                clear()
                return
            elif(option=='0'):
                clear()
                quit()

            elif(option=='m'):
                pokemon = database.get_random_pokemon(game_manager.game.box.poke_list)
                if pokemon is not None:
                    print_pokemon(pokemon)
                    print('\nDictionary:')
                    for k,v in pokemon.items():
                        print(f' - {k}: {v}')
            else:
                print('Opción no reconocida.')


    def open_menu_cards(self):
        
        clear()
        self.print_active_user()

        while(True):
            print(MenuManager.line)
            print('\n    Lista de cartas de ventaja:')
            n=1
            for c in card_manager.cards.values():
                print(f'\n    - {n}: {c.name}')
                print(f'        {c.description}')
                n+=1
                if not card_manager.can_use_card(c.tag, user_system.active_user):
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
                get_pokemon_with_card_mega()
            elif(option=='2'):
                print_box()
                get_pokemon_with_card_fusion()
            elif(option=='3'):
                print_box()
                get_pokemon_with_card_intercambio()
            elif(option=='4'):
                print_box()
                get_pokemon_with_card_preevo()
            elif(option=='5'):
                get_pokemon_with_card_comienzo()
            elif(option=='6'):
                print(f'NO IMPLEMENTADA TODAVÍA')
            elif(option=='7'):
                print('\nEscribe el tipo del Pokémon:')
                pokemon_type = input()
                get_pokemon_with_card_type(pokemon_type)
            elif(option=='8'):
                get_pokemon_with_card_aditional(1)
            elif(option=='9'):
                get_pokemon_with_card_aditional(2)
            elif(option=='10'):
                get_pokemon_with_card_aditional(3)
            elif(option=='11'):
                print(f'NO IMPLEMENTADA TODAVÍA')
                #get_pokemon_with_card_selectiva()
            
            #- 0: Salir
            elif(option=='0'):
                return
            else:
                print('Opción no reconocida.')

            print_active_user()
            
