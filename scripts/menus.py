from os import system

from scripts.users import User
from scripts.game import GameSession, GameSessionManager
from scripts.filters import PokemonFilters
from scripts.pokemontypes import PokemonTypes
from scripts.cards import Card


def clear():
    system("clear||cls")

def capitalize_name(text:str):
    words = text.split('-')
    return '-'.join(w.capitalize() for w in words)

def capitalize_all_words(text:str):
    words = text.replace('-',' ').split()
    return ' '.join(w.capitalize() for w in words)


class MenuManager():

    def __init__(self, game_manager : GameSessionManager):
        self.game_manager = game_manager
        self.user:User = None
        self.game:GameSession = None


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

    TEXT_POKEMON_SEARCH_ERROR = '\nNingún Pokémon cumple con los criterios de búsqueda.'


    def print_users(self, usernames:list):
        print('\nUsuarios registrados:')
        for n, username in enumerate(usernames):
            print(f' - {n+1}:\t{username}')

    def print_games(self):
        print('\nSesiones de juego registradas:')
        for n, gamename in enumerate(self.user.games):
            print(f' - {n+1}:\t{gamename}')

    def print_user(self):
        print(f'\nUsuario: {self.user.username}')

    def print_game_info(self):
        print(f'\nSesión de juego: {self.game.name}')
        print(f'\n   Datos de la sesión de juego')
        print(f'      Tiradas restantes: {self.game.options.rolls}')
        print(f'      Tiquets para forzar tipo: {self.game.options.tickets}')
        print(f'      Dinero: {self.game.options.money} monedas')
        print(f'      Puntos de items: {self.game.options.item_points}')

    def print_filters(self, filters:PokemonFilters):
        print('\nFiltros:')
        print(f' - filtrar por generación')
        print(f'   - obtener Pokémon hasta la generación: {filters.generation}')
        print(f' - filtrar por categoría')
        print(f'   - mythical: {filters.mythical}')
        print(f'   - legendary: {filters.legendary}')
        print(f'   - sublegendary: {filters.sublegendary}')
        print(f'   - powerhouse: {filters.powerhouse}')
        print(f'   - el resto de Pokémon: {filters.others}')
        print(f' - obtener sólo Pokémon completamente evolucionados: {filters.fully_evolved}')
        print(f' - obtener habilidades randomizadas: {filters.random_ability}')
        # print(f' - obtener sólo Pokémon que puedan mega-evolucionar: {filters.has_mega}')
        # print(f' - obtener sólo Pokémon que puedan gigamaxizar: {filters.has_gmax}')

    def print_box(self):
        if len(self.game.pokemon_box)==0:
            print(f'\nLa lista de Pokémon obtenidos está vacía.')
        else:
            print(f'\nLista de Pokémon obtenidos:')
            for n, pokemon in enumerate(self.game.pokemon_box):
                pokemon_id = pokemon[0]
                ability_id = pokemon[1]
                row = f' - {n+1}:\t{self.game_manager.pokemon_db.get_fullname(pokemon_id)}'#   (ID: {pokemon_id})'
                if ability_id:
                    row += f'   (Habilidad: {self.game_manager.pokemon_db.get_ability_name(ability_id)})'
                print(row)

    def print_pokemon(self, pokemon:dict):
        # nombre
        species_name:str = pokemon['species_name']
        form_name_text:str = pokemon['form_name_text']
        # generacion
        pokemon_generation_number:int = pokemon['pokemon_generation_number']
        # tipos
        first_type:str = pokemon['first_type']
        second_type:str = pokemon['second_type']
        # habilidades
        first_ability:str = pokemon['first_ability']
        second_ability:str = pokemon['second_ability']
        hidden_ability:str = pokemon['hidden_ability']
        # sprite
        sprite_default:str = pokemon['sprite_default']

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
        
        random_ability = pokemon.get('random_ability_name')
        if random_ability:
            print(f'\tHabilidad (random): {random_ability}')
        else:
            abilities = f'\tHabilidad: {capitalize_all_words(first_ability)}'
            if(second_ability is not None):
                abilities += f' / {capitalize_all_words(second_ability)}'
            print(abilities)
            if(hidden_ability is not None):
                print(f'\tHabilidad oculta: {capitalize_all_words(hidden_ability)}')

        print(f'\tIlustración: {sprite_default}')


    # MENU MANAGE USERS
    # =======================================================================

    def open_menu_users(self):

        clear()

        usernames_list = self.game_manager.user_system.db.get_usernames()

        while(True):
            self.print_users(usernames_list)

            print(MenuManager.TEXT_MENU_MANAGE_USERS)

            print('\nEscribe el número de la opción:')
            option = input()
            clear()

            print(f'\nSeleccionada opción {option}')

            #- 1: Cargar usuario
            if(option=='1'):
                
                if len(usernames_list)==0:
                    print('No hay usuarios registrados.')
                    continue

                self.print_users(usernames_list)

                while(True):
                    print('\nEscribe el número del usuario que quieres cargar:')
                    option = input()

                    try:
                        n = int(option)
                        n-=1
                    except:
                        print('Número no reconocido.')
                        continue

                    if n>=0 and n<len(usernames_list):
                        username = usernames_list[n]

                        # cargar usuario
                        user = self.game_manager.user_system.get_user(username)
                        if user:
                            self.user = User(
                                user_id = user.get('user_id'),
                                username = user.get('username'),
                                games = user.get('games')
                            )
                            self.open_menu_game_sessions()
                            break
                        else:
                            print('Usuario no encontrado.')
                    else:
                        print('La posición se sale del rango.')

            #- 2: Crear nuevo usuario
            elif(option=='2'):
                self.print_users(usernames_list)

                if len(usernames_list) < self.game_manager.user_system.MAX_USERS:
                    print('\nEscribe un nombre para el nuevo usuario:')

                    while True:
                        name = input()

                        if self.game_manager.user_system.insert_user(name):
                            usernames_list.append(name)
                            clear()
                            break
                        else:
                            print('\nEse nombre ya se encuentra en la base de datos, escribe otro diferente:')
                            continue

                else:
                    print('La lista de usuarios está llena, borra alguno para hacer hueco.')

            #- 3: Eliminar usuario
            elif(option=='3'):

                if len(usernames_list)==0:
                    print('No hay usuarios registrados.')
                    continue

                self.print_users(usernames_list)

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
                    
                    if n>=0 and n<len(usernames_list):
                        username = usernames_list[n]

                        if self.game_manager.user_system.delete_user(username):
                            usernames_list.pop(n)
                            clear()
                            break
                        else:
                            print('Usuario no encontrado.')
                    else:
                        print('La posición se sale del rango.')

            #- 0: Salir
            elif(option=='0'):
                clear()
                return
            else:
                print('Opción no reconocida.')



    # MENU MANAGE GAME SESSIONS
    # =======================================================================

    def open_menu_game_sessions(self):

        clear()

        while(True):
            self.print_user()

            if len(self.user.games)==0:
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
                
                if len(self.user.games)==0:
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

                    if n>=0 and n<len(self.user.games):
                        gamename = self.user.games[n]

                        # cargar partida
                        self.game = self.game_manager.get_game_session(self.user.user_id, gamename)
                        if self.game is not None:
                            clear()
                            self.open_menu_game()
                            break
                        else:
                            print('Sesión de juego no encontrada.')
                    else:
                        print('La posición se sale del rango.')

            #- 2: Crear nueva sesión de juego
            elif(option=='2'):
                if len(self.user.games)>0:
                    self.print_games()

                if len(self.user.games) <= User.MAX_GAMES:
                    
                    print('\nEscribe un nombre para la sesión de juego:')
                    name = input()

                    if name in self.user.games:
                        print('\nEse nombre ya se encuentra registrado.')
                        continue

                    options = {}

                    print('\n¿Valores de juego por defecto? Escribe 1 para si, escribe otra cosa para no.')
                    default_options = input()

                    options['default_options'] = default_options=='1'

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

                    options['default_filters'] = default_filters=='1'

                    if default_filters!='1':
                        print('\nFiltrar por generación del Pokémon.')
                        print('Escribe el número de hasta qué generación aparecen los Pokémon:')
                        options['generation'] = input()

                        print('\nFiltrar por categoría del Pokémon.')
                        print('¿Incluir míticos? Escribe 1 para si, escribe otra cosa para no.')
                        options['mythical'] = input()=='1'

                        print('\n¿Incluir legendarios? Escribe 1 para si, escribe otra cosa para no.')
                        options['legendary'] = input()=='1'

                        print('\n¿Incluir sublegendarios? Escribe 1 para si, escribe otra cosa para no.')
                        options['sublegendary'] = input()=='1'

                        print('\n¿Incluir pesos pesados? Escribe 1 para si, escribe otra cosa para no.')
                        options['powerhouse'] = input()=='1'

                        print('\n¿Incluir los demás Pokémon que no pertenezcan a estas categorías? Escribe 1 para si, escribe otra cosa para no.')
                        options['others'] = input()=='1'

                        print('\nFiltrar por etapa evolutiva del Pokémon.')
                        print('¿Incluir solamente Pokémon en su última etapa evolutiva? Escribe 1 para si, escribe otra cosa para no.')
                        options['fully_evolved'] = input()=='1'

                        print('\n¿Obtener habilidades randomizadas? (De cualquier Pokémon posible) Escribe 1 para si, escribe otra cosa para no.')
                        options['random_ability'] = input()=='1'

                    self.game_manager.create_game_session(self.user.user_id, name, options)
                    self.user.games.append(name)
                    clear()
                            
                else:
                    print('La lista de juegos está llena, borra alguno para hacer hueco.')

            #- 3: Eliminar sesión de juego
            elif(option=='3'):
                
                if len(self.user.games)==0:
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

                    if n>=0 and n<len(self.user.games):
                        gamename = self.user.games[n]
                        if self.game_manager.delete_game_session(self.user.user_id, gamename):
                            self.user.games.pop(n)
                            clear()
                            break
                        else:
                            print('Sesión de juego no encontrada.')
                    else:
                        print('La posición se sale del rango.')

            #- 0: Salir
            elif(option=='0'):
                clear()
                return
            else:
                print('Opción no reconocida.')



    # MENU GAME
    # =======================================================================

    def open_menu_game(self):

        while(True):
            self.print_user()
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
                self.print_filters()

            elif(option=='9'):
                clear()
                return
            elif(option=='0'):
                clear()
                quit()

            elif(option=='m'):
                pokemon = self.game_manager.get_random_pokemon(
                    [ x[0] for x in self.game.pokemon_box ], 
                    self.game.filters.random_ability
                )
                if pokemon:
                    self.print_pokemon(pokemon)
            else:
                print('Opción no reconocida.')

            print(MenuManager.TEXT_LINE)


    def roll(self):
        if self.game.options.rolls==0:
            print('\nNo quedan tiradas.')
            return

        #obtained_pokemon_list = [ x[0] for x in self.game_manager.db.get_pokemon_box(game.game_id) ]
        pokemon_list = [ x[0] for x in self.game.pokemon_box ]
        pokemon = self.game_manager.do_roll(self.game, pokemon_list)
        if not pokemon:
            print(MenuManager.TEXT_POKEMON_SEARCH_ERROR)
            return

        self.game.pokemon_box.append(
            (pokemon.get('id'), pokemon.get('random_ability_id'))
        )

        self.print_pokemon(pokemon)

    def roll_with_type(self):
        if self.game.options.rolls==0:
            print('\nNo quedan tiradas.')
            return
        if self.game.options.tickets==0:
            print('\nNo quedan tiquets.')
            return

        print('\nEscribe el tipo del Pokémon:')
        pokemon_type = input().lower()
        if pokemon_type not in PokemonTypes.TYPE_LIST:
            print('\nError: Tipo no identificado.')
            return

        #obtained_pokemon_list = [ x[0] for x in self.game_manager.db.get_pokemon_box(game.game_id) ]
        pokemon_list = [ x[0] for x in self.game.pokemon_box ]
        pokemon = self.game_manager.do_roll_with_type(self.game, pokemon_list, pokemon_type)
        if not pokemon:
            print(MenuManager.TEXT_POKEMON_SEARCH_ERROR)
            return

        self.game.pokemon_box.append(
            (pokemon.get('id'), pokemon.get('random_ability_id'))
        )

        self.print_pokemon(pokemon)



    # MENU CARDS
    # =======================================================================

    def open_menu_cards(self):
        
        clear()

        while(True):
            self.print_user()
            self.print_game_info()
            print(MenuManager.TEXT_LINE)

            print('\n    Lista de cartas de ventaja:')
            for n, card in enumerate(self.game_manager.cards.values()):
                print(f'\n    - {n+1}: {card.name}')
                print(f'        {card.description}')

                if not self.game.can_use_card(card):
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
                self.use_card_fusion()
            elif(option=='3'):
                self.use_card_intercambio()
            elif(option=='4'):
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
                self.use_card_selectiva()
            
            #- 0: Salir
            elif(option=='0'):
                return
            else:
                print('Opción no reconocida.')


    def check_card_conditions(self, card:Card) -> bool:
        if card is None:
            return False

        if not self.game.can_use_card(card):
            print('\nNo puedes usar esa carta porque ya has superado su límite de usos.')
            return False

        if not self.game.can_spend_money(card.price):
            print('\nNo tienes suficiente dinero para comprar esa carta.')
            return False

        return True

    def use_card_mega(self):
        tag = 'mega'
        card = self.game_manager.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        pokemon = self.game_manager.use_card_mega()
        if not pokemon:
            print(MenuManager.TEXT_POKEMON_SEARCH_ERROR)
            return

        # mostrar
        self.print_pokemon(pokemon)

    def use_card_fusion(self):
        tag = 'fusion'
        card = self.game_manager.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        if len(self.game.pokemon_box)<2:
            print('\nNo se puede usar porque no tienes más de 2 Pokémon.')
            return

        self.print_box()

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

        box_length = len(self.game.pokemon_box)
        if (
            (position1<0 or position1>box_length) 
            or 
            (position2<0 or position2>box_length) 
        ):
            print('\nError: Posiciones no detectadas.')
            return

        pokemon = self.game_manager.use_card_fusion(
            pokemon_id1 = self.game.pokemon_box[position1][0],
            pokemon_id2 = self.game.pokemon_box[position2][0]
        )
        if not pokemon:
            print(MenuManager.TEXT_POKEMON_SEARCH_ERROR)
            return

        # mostrar
        self.print_pokemon(pokemon)

    def use_card_intercambio(self):
        tag = 'intercambio'
        card = self.game_manager.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        if len(self.game.pokemon_box)==0:
            print('\nNo se puede usar porque no tienes ningún Pokémon.')
            return

        self.print_box()

        try:
            print('\nEscribe el número de la posición del Pokémon a intercambiar:')
            pokemon_position = int(input()) - 1
        except:
            print('\nError: Posición no detectada.')
            return
        
        if (
            pokemon_position<0 or pokemon_position>len(self.game.pokemon_box)
        ):
            print('\nError: Posición no detectada.')
            return

        pokemon_id = self.game.pokemon_box[pokemon_position][0]
        pokemon = self.game_manager.use_card_intercambio(pokemon_id)
        if not pokemon:
            print(MenuManager.TEXT_POKEMON_SEARCH_ERROR)
            return

        # mostrar
        self.print_pokemon(pokemon)

    def use_card_preevo(self):
        tag = 'preevo'
        card = self.game_manager.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        if len(self.game.pokemon_box)==0:
            print('\nNo se puede usar porque no tienes ningún Pokémon.')
            return

        self.print_box()

        try:
            print('\nEscribe el número de la posición del Pokémon que quieres cambiar por su pre-evolución:')
            pokemon_position = int(input()) - 1
        except:
            print('\nError: Posición no detectada.')
            return

        if (
            pokemon_position<0 or pokemon_position>len(self.game.pokemon_box)
        ):
            print('\nError: Posición no detectada.')
            return

        pokemon_id = self.game.pokemon_box[pokemon_position][0]
        pokemon = self.game_manager.use_card_preevo(pokemon_id)
        if not pokemon:
            print(MenuManager.TEXT_POKEMON_SEARCH_ERROR)
            return

        # mostrar
        self.print_pokemon(pokemon)

    def use_card_comienzo(self):
        tag = 'comienzo'
        card = self.game_manager.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        if abs(self.game.options.rolls - self.game.options.max_rolls) >= 18:
            print('\nNo se puede usar porque ya se han realizado 18 tiradas o más.')
            return

        self.game_manager.use_card_comienzo()
        print('\nTiradas reiniciadas.')

    def use_card_powerhouse(self):
        tag = 'powerhouse'
        card = self.game_manager.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        self.game_manager.use_card_powerhouse()

    def use_card_type(self):
        tag = 'tipo'
        card = self.game_manager.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        self.game_manager.use_card_type()

    def use_card_aditional(self, rolls:int):
        tag = 'adicional_' + str(rolls)
        card = self.game_manager.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        self.game_manager.use_card_aditional(rolls)
        print(f'\nTiradas adicionales añadidas: {rolls}')

    def use_card_selectiva(self, game:GameSession):
        tag = 'selectiva'
        card = self.game_manager.cards.get(tag)

        if not self.check_card_conditions(card):
            return

        if game.options.rolls < 6:
            return

        pokemon_list = []
        obtained_pokemon_list = [ x[0] for x in self.game.pokemon_box ]

        for n in range(6):
            pokemon = self.game_manager.get_random_pokemon(
                obtained_pokemon_list,
                self.game.filters.random_ability
            )

            if not pokemon:
                continue

            pokemon_list.append(pokemon)
            obtained_pokemon_list.append(pokemon.get('id'))

        if len(pokemon_list)==0:
            print(MenuManager.TEXT_POKEMON_SEARCH_ERROR)
            return

        clear()
        picks = 0
        while(True):
            print(f'\nTiradas restantes: {game.options.rolls}\n')
            
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
            pokemon_id = pokemon.get('id')
            ability_id = pokemon.get('random_ability_id')
            self.game_manager.user_system.db.insert_pokemon(game.game_id, pokemon_id, ability_id)
            self.game_manager.spend_roll(game)
            picks+=1

            # termina
            if picks==5 or len(pokemon_list)==0:
                break

        self.game_manager.buy_card(card)

