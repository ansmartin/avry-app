from os import system
from numpy import isnan

from scripts.users import UserSystem
from scripts.game import GameSessionManager
from scripts.pokemon import PokemonDatabaseManager
from scripts.cards import Card, CardManager
from scripts.pokemontypes import PokemonTypes


def clear():
    system("clear||cls")

def capitalize_name(text:str):
    words = text.split('-')
    return '-'.join(w.capitalize() for w in words)

def capitalize_all_words(text:str):
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
        - 1: Realizar tirada normal
        - 2: Realizar tirada forzando el tipo (gasta 1 ticket)
        - 3: Comprar ventaja
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
        print(f'      Tiradas restantes: {self.game_manager.game.options.rolls}')
        print(f'      Tiquets para forzar tipo: {self.game_manager.game.options.tickets}')
        print(f'      Dinero: {self.game_manager.game.options.money} monedas')
        print(f'      Puntos de items: {self.game_manager.game.options.item_points}')

    def print_box(self):
        pokemon_list = self.game_manager.get_namelist_of_obtained_pokemon()

        if len(pokemon_list)==0:
            print(f'\nLa lista de Pokémon obtenidos está vacía.')
        else:
            print(f'\nLista de Pokémon obtenidos:')
            for n, pokemon in enumerate(pokemon_list):
                print(f' - {n+1}:\t{pokemon}')

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

    def get_pokemon(self, mask=None) -> bool:
        pokemon = self.database.get_random_pokemon(self.game_manager.game.box._list, mask)

        if pokemon is None:
            print('\nNingún Pokémon cumple con los criterios de búsqueda.')
            return False
        
        # mostrar
        self.print_pokemon(pokemon)

        # guardar pokemon
        pokemon_id = pokemon['id']
        self.game_manager.insert_pokemon(pokemon_id)
        return True


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
                
                if self.user_system.usernames.get_length()==0:
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
                    if self.user_system.load_user(n):
                        self.open_menu_game_sessions()
                        break
                    else:
                        print('Usuario no encontrado.')

            #- 2: Crear nuevo usuario
            elif(option=='2'):
                self.print_users()

                if self.user_system.usernames.can_add_element():
                    print('\nEscribe un nombre para el nuevo usuario:')

                    while True:
                        name = input()

                        if self.user_system.insert_user(name):
                            clear()
                            break
                        else:
                            print('\nEse nombre ya se encuentra en la base de datos, escribe otro diferente:')
                            continue

                else:
                    print('La lista de usuarios está llena, borra alguno para hacer hueco.')

            #- 3: Eliminar usuario
            elif(option=='3'):

                if self.user_system.usernames.get_length()==0:
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

                    # if self.user_system.active_user.username == self.user_system.usernames[n]:
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
        for n, username in enumerate(self.user_system.usernames._list):
            print(f' - {n+1}:\t{username}')

    def print_games(self):
        print('\nSesiones de juego registradas:')
        for n, gamename in enumerate(self.user_system.active_user.games._list):
            print(f' - {n+1}:\t{gamename}')


    def open_menu_game_sessions(self):

        clear()

        while(True):
            self.print_active_user()

            if self.user_system.active_user.games.get_length()==0:
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
                
                if self.user_system.active_user.games.get_length()==0:
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
                    if self.game_manager.load_game(n):
                        clear()
                        self.open_menu_game()
                        break
                    else:
                        print('Sesión de juego no encontrada.')

            #- 2: Crear nueva sesión de juego
            elif(option=='2'):
                if self.user_system.active_user.games.get_length()>0:
                    self.print_games()

                if self.user_system.active_user.games.can_add_element():
                    
                    print('\nEscribe un nombre para la sesión de juego:')
                    name = input()

                    if self.user_system.active_user.games.contains(name):
                        print('\nEse nombre ya se encuentra en la base de datos.')
                        continue


                    print('\n¿Valores de juego por defecto? Escribe 1 para si, escribe otra cosa para no.')
                    default_options = input()

                    options = {}
                    if default_options!='1':
                        print('\nEscribe el número de tiradas disponibles:')
                        options['rolls'] = input()

                        print('\nEscribe el número de tiquets de forzar tipo disponibles:')
                        options['tickets'] = input()

                        print('\nEscribe la cantidad de dinero disponible:')
                        options['money'] = input()

                        print('\nEscribe el número de puntos de item disponibles:')
                        options['item_points'] = input()


                    print('\n¿Valores de filtros por defecto? Escribe 1 para si, escribe otra cosa para no.')
                    default_filters = input()

                    filters = {}
                    if default_filters!='1':
                        print('\nFiltrar por generación del Pokémon.')
                        print('Escribe el número de hasta qué generación aparecen los Pokémon:')
                        filters['generation'] = input()

                        print('\nFiltrar por categoría del Pokémon.')
                        print('¿Incluir míticos? Escribe 1 para si, escribe otra cosa para no.')
                        filters['mythical'] = input()=='1'

                        print('\n¿Incluir legendarios? Escribe 1 para si, escribe otra cosa para no.')
                        filters['legendary'] = input()=='1'

                        print('\n¿Incluir sublegendarios? Escribe 1 para si, escribe otra cosa para no.')
                        filters['sublegendary'] = input()=='1'

                        print('\n¿Incluir pesos pesados? Escribe 1 para si, escribe otra cosa para no.')
                        filters['powerhouse'] = input()=='1'

                        print('\n¿Incluir los demás Pokémon que no pertenezcan a estas categorías? Escribe 1 para si, escribe otra cosa para no.')
                        filters['others'] = input()=='1'

                        print('\nFiltrar por etapa evolutiva del Pokémon.')
                        print('¿Incluir solamente Pokémon en su última etapa evolutiva? Escribe 1 para si, escribe otra cosa para no.')
                        filters['fully_evolved'] = input()=='1'

                    self.game_manager.create_game_session(name, options, filters)
                    clear()
                            
                else:
                    print('La lista de juegos está llena, borra alguno para hacer hueco.')

            #- 3: Eliminar sesión de juego
            elif(option=='3'):
                
                if self.user_system.active_user.games.get_length()==0:
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

                    # if self.user_system.active_user.username == self.user_system.usernames[n]:
                    #     print('No puedes borrar el usuario activo. Elige otro.')
                    #     continue

                    if self.game_manager.delete_game(n):
                        clear()
                        break
                    else:
                        print('Sesión de juego no encontrada.')

            #- 0: Salir
            elif(option=='0'):
                self.user_system.active_user=None
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
                self.roll()
            elif(option=='2'):
                self.roll_with_type()
            elif(option=='3'):
                self.open_menu_cards()
            elif(option=='4'):
                self.game_manager.game.filters.print_options()

            elif(option=='9'):
                clear()
                return
            elif(option=='0'):
                clear()
                quit()

            elif(option=='m'):
                pokemon = self.database.get_random_pokemon(self.game_manager.game.box._list)
                if pokemon is not None:
                    self.print_pokemon(pokemon)
                    print('\nDictionary:')
                    for k,v in pokemon.items():
                        print(f' - {k}: {v}')
            else:
                print('Opción no reconocida.')

            print(MenuManager.TEXT_LINE)

    def roll(self):
        if self.game_manager.game.get_rolls()==0:
            print('\nNo quedan tiradas.')
            return

        # obtener pokemon y gastar tirada
        if self.get_pokemon():
            self.game_manager.spend_roll()

    def roll_with_type(self):
        if self.game_manager.game.get_rolls()==0:
            print('\nNo quedan tiradas.')
            return
        if self.game_manager.game.get_tickets()==0:
            print('\nNo quedan tiquets.')
            return

        print('\nEscribe el tipo del Pokémon:')
        pokemon_type = input().lower()
        if pokemon_type not in PokemonTypes.TYPE_LIST:
            print('\nError: Tipo no identificado.')
            return

        mask = (
            (self.database.df_filtered.first_type==pokemon_type) 
            | 
            (self.database.df_filtered.second_type==pokemon_type)
        )

        # obtener pokemon, gastar ticket y tirada
        if self.get_pokemon(mask):
            self.game_manager.spend_ticket()
            self.game_manager.spend_roll()

    def open_menu_cards(self):
        
        clear()

        while(True):
            self.print_active_user()
            self.print_game_info()
            print(MenuManager.TEXT_LINE)

            print('\n    Lista de cartas de ventaja:')
            for n, card in enumerate(self.card_manager.cards.values()):
                print(f'\n    - {n+1}: {card.name}')
                print(f'        {card.description}')

                if not self.game_manager.can_use_card(card):
                    print(f'        (AGOTADA)')
                    continue
                print(f'        Precio: {card.price} monedas')
                if card.limit>0:
                    print(f'        Limite de usos: {card.limit}')

            print('\n    - 0: Volver al menú principal')
            print('\nEscribe el número de la opción:')

            option = input()
            clear()

            print(f'\nSeleccionada opción {option}')
            
            if(option=='1'):
                self.use_card_mega()
            elif(option=='2'):
                self.print_box()
                self.use_card_fusion()
            elif(option=='3'):
                self.print_box()
                self.use_card_intercambio()
            elif(option=='4'):
                self.print_box()
                self.use_card_preevo()
            elif(option=='5'):
                self.use_card_comienzo()
            elif(option=='6'):
                self.use_card_powerhouse()
            elif(option=='7'):
                self.use_card_type()
            elif(option=='8'):
                self.use_card_aditional(1)
            elif(option=='9'):
                self.use_card_aditional(2)
            elif(option=='10'):
                self.use_card_aditional(3)
            elif(option=='11'):
                self.get_pokemon_with_card_selectiva()
            
            #- 0: Salir
            elif(option=='0'):
                return
            else:
                print('Opción no reconocida.')


    def check_card_conditions(self, card:Card) -> bool:
        if card is None:
            return False

        if not self.game_manager.can_use_card(card):
            print('\nNo puedes usar esa carta porque ya has superado su límite de usos.')
            return False

        if not self.game_manager.game.can_spend_money(card.price):
            print('\nNo tienes suficiente dinero para comprar esa carta.')
            return False

        return True

    def use_card_mega(self):
        tag = 'mega'
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        mask = self.database.df_filtered.has_mega
        
        # obtener pokemon y guardar archivo de juego
        if self.get_pokemon(mask):
            self.game_manager.buy_card_and_save(card)

    def use_card_fusion(self):
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

        # ajustar segunda posicion para cuando se borre la primera
        if position1 < position2:
            position2-=1

        # obtener pokemon y guardar archivo de juego
        if self.get_pokemon():
            self.game_manager.delete_pokemon(position1)
            self.game_manager.delete_pokemon(position2)
            self.game_manager.buy_card_and_save(card)

    def use_card_intercambio(self):
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

        # obtener pokemon y guardar archivo de juego
        if self.get_pokemon():
            self.game_manager.delete_pokemon(pokemon_position)
            self.game_manager.buy_card_and_save(card)

    def use_card_preevo(self):
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
        
        pokemon_id = self.game_manager.game.box.get(pokemon_position)
        preevo_id = self.database.df.loc[pokemon_id].evolves_from_pokemon_id

        if isnan(preevo_id):
            print('\nError: El Pokémon seleccionado no tiene pre-evolución.')
            return

        #get_pokemon()
        pokemon = self.database.df.loc[preevo_id].to_dict()

        # mostrar y guardar pokemon
        self.print_pokemon(pokemon)

        pokemon_id = pokemon['id']
        self.game_manager.insert_pokemon(pokemon_id)
        self.game_manager.delete_pokemon(pokemon_position)

        # guardar archivo de juego
        self.game_manager.buy_card_and_save(card)

    def use_card_comienzo(self):
        tag = 'comienzo'
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        if abs(self.game_manager.game.options.rolls - self.game_manager.game.options.max_rolls) >= 18:
            print('\nNo se puede usar porque ya se han realizado 18 tiradas o más.')
            return

        print('\nTiradas reiniciadas.')
        self.game_manager.reset_rolls_and_box()

        # guardar archivo de juego
        self.game_manager.buy_card_and_save(card)

    def use_card_powerhouse(self):
        tag = 'powerhouse'
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        # guardar archivo de juego
        self.game_manager.buy_card_and_save(card)

    def use_card_type(self):
        tag = 'tipo'
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        print('\nAñadido un tiquet de forzar tipo.')
        self.game_manager.add_tickets(1)

        # guardar archivo de juego
        self.game_manager.buy_card_and_save(card)

    def use_card_aditional(self, rolls:int):
        tag = 'adicional_' + str(rolls)
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        print(f'\nTiradas adicionales añadidas: {rolls}')
        self.game_manager.add_rolls(rolls)

        # guardar archivo de juego
        self.game_manager.buy_card_and_save(card)

    def get_pokemon_with_card_selectiva(self):
        tag = 'selectiva'
        card = self.card_manager.cards.get(tag, None)

        if not self.check_card_conditions(card):
            return

        if self.game_manager.game.get_rolls() < 6:
            return

        pokemon_list = []

        for n in range(6):
            #self.get_pokemon()
            pokemon = self.database.get_random_pokemon(self.game_manager.game.box._list)

            if pokemon is None:
                break

            pokemon_list.append(pokemon)

        if len(pokemon_list)==0:
            print('\nNingún Pokémon cumple con los criterios de búsqueda.')
            return

        clear()
        picks = 0
        while(True):
            print(f'\nTiradas restantes: {self.game_manager.game.get_rolls()}\n')
            
            # mostrar pokemons
            for n, pokemon in enumerate(pokemon_list):
                print(f'- {n+1}')
                self.print_pokemon(pokemon)

            print(f'\nEscribe el número del Pokémon que quieres quedarte (del 1 al {len(pokemon_list)}) (Gastas 1 tirada por cada Pokémon que te quedes).\nEscribe 0 para parar.')

            try:
                pokemon_position = int(input()) - 1
            except:
                clear()
                print('\nError: Posición no detectada.')
                continue

            # termina
            if pokemon_position==-1:
                break

            if pokemon_position<0 or pokemon_position>=len(pokemon_list):
                clear()
                print('\nError: La posición no se encuentra dentro del rango.')
                continue

            clear()
            print('\nTirada gastada.')
            pokemon = pokemon_list.pop(pokemon_position)
            pokemon_id = pokemon['id']
            self.game_manager.insert_pokemon(pokemon_id)
            self.game_manager.spend_roll()
            picks+=1

            # termina
            if picks==5 or len(pokemon_list)==0:
                break
            

        # guardar archivo de juego
        self.game_manager.buy_card_and_save(card)

