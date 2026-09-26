import requests
from os import system


API_URL = 'http://localhost:8080'
API_URL_GAMEMODE = API_URL + '/game/'
API_URL_USER = API_URL + '/user/'
API_URL_USER_GAME = API_URL_USER + '{}/game/{}'
API_URL_USER_GAME_ROLL = API_URL_USER_GAME + '/roll'


TEXT_LINE = '\n------------------------------------'

TEXT_MENU_PRINCIPAL = """\nMENÚ PRINCIPAL

    Opciones:
    - 1: Gestionar modos de juego
    - 2: Gestionar usuarios y sus partidas

    - 0: Cerrar aplicación
"""

TEXT_MENU_MANAGE_GAMEMODES = """\n
    Opciones:
    - 1: Ver modos de juego disponibles
    - 2: Crear nuevo modo de juego
    - 3: Eliminar modo de juego

    - 0: Volver atrás
"""

TEXT_MENU_MANAGE_USERS = """\n
    Opciones:
    - 1: Cargar usuario
    - 2: Crear nuevo usuario
    - 3: Eliminar usuario

    - 0: Volver atrás
"""

TEXT_MENU_MANAGE_GAMESESSIONS = """\n
    Opciones:
    - 1: Cargar partida
    - 2: Apuntarse a una partida
    - 3: Quitarse de una partida

    - 0: Volver al menú de usuarios
"""

TEXT_MENU_PLAY_GAME = """\n
    Opciones:
    - 1: Realizar tirada normal
    - 2: Realizar tirada forzando el tipo (gasta 1 ticket)
    - 3: Comprar ventaja
    - 4: Mostrar filtros activos

    - 9: Cerrar aplicación
    - 0: Volver a la pantalla de usuario
"""
TEXT_MENU_PLAY_GAME = TEXT_LINE + TEXT_MENU_PLAY_GAME + TEXT_LINE

TEXT_INSERT_NUMBER = '\nEscribe el número de la opción:'

TEXT_SELECTED_OPTION = '\nSeleccionada opción {}'

TEXT_OPTION_NOT_RECOGNIZED = 'Opción no reconocida.'

TEXT_POKEMON_SEARCH_ERROR = '\nNingún Pokémon cumple con los criterios de búsqueda.'

TEXT_USER = '\nUsuario: {}'

TEXT_GAME = '\nPartida: {}'

TEXT_NO_USERS = 'No hay usuarios registrados.'

TEXT_NO_GAMEMODES = 'No hay modos de juego registrados.'

TEXT_NO_GAMESESSIONS = 'No hay partidas registradas.'


def clear():
    system("clear||cls")


# MENU
# =======================================================================

def open_menu():

    clear()

    while(True):
        print(TEXT_MENU_PRINCIPAL)

        print(TEXT_INSERT_NUMBER)
        option = input()
        clear()

        print(TEXT_SELECTED_OPTION.format(option))

        #- 1: Gestionar modos de juego
        if(option=='1'):
            open_menu_gamemodes()

        #- 2: Gestionar usuarios y sus partidas
        elif(option=='2'):
            open_menu_users()

        #- 0: Salir
        elif(option=='0'):
            clear()
            return
        else:
            print(TEXT_OPTION_NOT_RECOGNIZED)


# MENU MANAGE GAMEMODES
# =======================================================================

def open_menu_gamemodes():

    clear()

    while(True):
        print(TEXT_MENU_MANAGE_GAMEMODES)

        print(TEXT_INSERT_NUMBER)
        option = input()
        clear()

        print(TEXT_SELECTED_OPTION.format(option))

        #- 1: Ver modos de juego disponibles
        if(option=='1'):
            response = requests.get(API_URL_GAMEMODE)
            gamenames_list = response.json()

            if not gamenames_list:
                print(TEXT_NO_GAMEMODES)
                continue

            print('\nModos de juego:')
            for x in gamenames_list:
                print('- {}'.format(x))

        #- 2: Crear nuevo modo de juego
        elif(option=='2'):
                
            print('\nEscribe un nombre para el nuevo modo de juego:')
            name = input()

            if len(name)==0:
                continue

            response = requests.get(API_URL_GAMEMODE)
            gamenames_list = response.json()

            if name in gamenames_list:
                print('\nEse nombre ya se encuentra registrado.')
                continue

            options = {}

            options['name'] = name

            print('\n¿Valores de juego por defecto? Escribe 1 para sí, escribe otra cosa para no.')
            default_options = input()

            if default_options!='1':
                print('\nEscribe el número de tiradas disponibles:')
                options['rolls'] = input()

                print('\nEscribe el número de tiquets de forzar tipo disponibles:')
                options['tickets'] = input()

                print('\nEscribe la cantidad de dinero disponible:')
                options['money'] = input()

                print('\nEscribe el número de puntos de item disponibles:')
                options['item_points'] = input()


            print('\n¿Valores de filtros por defecto? Escribe 1 para sí, escribe otra cosa para no.')
            default_filters = input()

            if default_filters!='1':
                print('\nFiltrar por generación del Pokémon.')
                print('Escribe el número de hasta qué generación aparecen los Pokémon:')
                options['generation'] = input()

                print('\nFiltrar por categoría del Pokémon.')
                print('¿Incluir míticos? Escribe 1 para sí, escribe otra cosa para no.')
                options['mythical'] = input()=='1'

                print('\n¿Incluir legendarios? Escribe 1 para sí, escribe otra cosa para no.')
                options['legendary'] = input()=='1'

                print('\n¿Incluir sublegendarios? Escribe 1 para sí, escribe otra cosa para no.')
                options['sublegendary'] = input()=='1'

                print('\n¿Incluir pesos pesados? Escribe 1 para sí, escribe otra cosa para no.')
                options['powerhouse'] = input()=='1'

                print('\nFiltrar por etapa evolutiva del Pokémon.')
                print('¿Incluir solamente Pokémon en su última etapa evolutiva? Escribe 1 para sí, escribe otra cosa para no.')
                options['fully_evolved'] = input()=='1'

                print('\n¿Obtener habilidades randomizadas? (De cualquier Pokémon posible) Escribe 1 para sí, escribe otra cosa para no.')
                options['random_ability'] = input()=='1'

            response = requests.post(API_URL_GAMEMODE+name, data=options)
            print(response.text)

        #- 3: Eliminar modo de juego
        elif(option=='3'):
            response = requests.get(API_URL_GAMEMODE)
            gamenames_list = response.json()

            if not gamenames_list:
                print(TEXT_NO_GAMEMODES)
                continue

            print('\nModos de juego:')
            for x in gamenames_list:
                print('- {}'.format(x))

            print('\nEscribe el nombre del modo de juego que quieres eliminar:')
            name = input()

            clear()

            if len(name)==0:
                continue

            response = requests.delete(API_URL_GAMEMODE+name)
            print(response.text)

        #- 0: Salir
        elif(option=='0'):
            clear()
            return
        else:
            print(TEXT_OPTION_NOT_RECOGNIZED)


# MENU MANAGE USERS
# =======================================================================

def open_menu_users():
    
    clear()
    
    response = requests.get(API_URL_USER)
    usernames_list = response.json()

    while(True):
        print('\nUsuarios:')
        for x in usernames_list:
            print('- {}'.format(x))

        print(TEXT_MENU_MANAGE_USERS)

        print(TEXT_INSERT_NUMBER)
        option = input()

        print(TEXT_SELECTED_OPTION.format(option))

        #- 1: Cargar usuario
        if(option=='1'):
            
            if len(usernames_list)==0:
                print(TEXT_NO_USERS)
                continue

            while(True):
                print('\nEscribe el nombre del usuario que quieres cargar:')
                name = input()

                if len(name)==0:
                    clear()
                    break

                if name not in usernames_list:
                    print('Usuario no encontrado.')
                    continue

                open_menu_gamesessions(name)
                break

        #- 2: Crear nuevo usuario
        elif(option=='2'):
            print('\nEscribe un nombre para el nuevo usuario:')
            name = input()

            clear()

            if len(name)==0:
                continue
            
            response = requests.post(API_URL_USER+name)
            print(response.text)

            # update usernames_list
            response = requests.get(API_URL_USER)
            usernames_list = response.json()

        #- 3: Eliminar usuario
        elif(option=='3'):
            
            if len(usernames_list)==0:
                print(TEXT_NO_USERS)
                continue
            
            print('\nEscribe el nombre del usuario que quieres eliminar:')

            name = input()

            clear()

            if len(name)==0:
                continue
            
            response = requests.delete(API_URL_USER+name)
            print(response.text)

            # update usernames_list
            response = requests.get(API_URL_USER)
            usernames_list = response.json()

        #- 0: Salir
        elif(option=='0'):
            clear()
            return
        else:
            print(TEXT_OPTION_NOT_RECOGNIZED)


# MENU GAMESESSIONS
# =======================================================================

def open_menu_gamesessions(username:str):
    
    clear()

    response = requests.get(API_URL_USER+username)
    user:dict = response.json()
    gamenames_list = user.get('games')

    while(True):
        print(TEXT_USER.format(username))

        print('\nPartidas:')
        for x in gamenames_list:
            print('- {}'.format(x))

        print(TEXT_MENU_MANAGE_GAMESESSIONS)
        
        print(TEXT_INSERT_NUMBER)
        option = input()

        print(TEXT_SELECTED_OPTION.format(option))

        #- 1: Cargar partida
        if(option=='1'):
            
            if len(gamenames_list)==0:
                print(TEXT_NO_GAMESESSIONS)
                continue

            while(True):
                print('\nEscribe el nombre de la partida que quieres cargar:')
                name = input()

                if len(name)==0:
                    clear()
                    break

                if name not in gamenames_list:
                    print('Partida no encontrada.')
                    continue

                open_menu_game(username, name)
                break

        #- 2: Apuntarse a partida
        elif(option=='2'):
            
            response = requests.get(API_URL_GAMEMODE)
            gamenames_availables_list = response.json()

            if not gamenames_availables_list:
                clear()
                print(TEXT_NO_GAMEMODES)
                continue
            
            print('\nModos de juego:')
            for x in gamenames_availables_list:
                print('- {}'.format(x))
            
            print('\nEscribe el nombre del modo de juego con el que quieres empezar una partida (creará una partida con ese mismo nombre):')
            name = input()

            clear()

            if len(name)==0:
                continue
            
            if name not in gamenames_availables_list:
                print('Modo de juego no encontrado.')
                continue
            
            if name in gamenames_list:
                print('Ya estabas unido a una partida con este modo de juego.')
                continue
            
            response = requests.post(API_URL_USER_GAME.format(username, name))
            print(response.text)

            # update
            response = requests.get(API_URL_USER+username)
            user:dict = response.json()
            gamenames_list = user.get('games')

        #- 3: Quitarse de partida
        elif(option=='3'):
            
            response = requests.get(API_URL_USER+username)
            user:dict = response.json()

            gamenames_list = user.get('games')

            if not gamenames_list:
                print(TEXT_NO_GAMESESSIONS)
                continue
            
            print('\nEscribe el nombre de la partida que quieres eliminar:')

            name = input()

            clear()

            if len(name)==0:
                continue
            
            response = requests.delete(API_URL_USER_GAME.format(username, name))
            print(response.text)

            # update
            response = requests.get(API_URL_USER+username)
            user:dict = response.json()
            gamenames_list = user.get('games')

        #- 0: Salir
        elif(option=='0'):
            clear()
            return
        else:
            print(TEXT_OPTION_NOT_RECOGNIZED)


# MENU GAME
# =======================================================================

def open_menu_game(username:str, gamename:str):
    
    clear()

    while(True):
        print(TEXT_USER.format(username))
        print(TEXT_GAME.format(gamename))
        print_game_info(username, gamename)
        print_box()

        print(TEXT_MENU_PLAY_GAME)

        print(TEXT_INSERT_NUMBER)
        option = input()
        clear()

        print(TEXT_SELECTED_OPTION.format(option))

        if(option=='1'):
            roll(username, gamename)
        elif(option=='2'):
            roll(username, gamename, spend_ticket=True)
        elif(option=='3'):
            open_menu_cards()
        elif(option=='4'):
            print_filters(gamename)

        elif(option=='9'):
            clear()
            quit()
        elif(option=='0'):
            clear()
            return

        else:
            print(TEXT_OPTION_NOT_RECOGNIZED)

        print(TEXT_LINE)

def print_game_info(username, gamename):
    response = requests.get(API_URL_USER_GAME.format(username, gamename))
    game:dict = response.json()
    game_properties:dict = game.get('game_properties')
    print(f'\n   Datos de la sesión de juego')
    print(f'      Tiradas restantes: {game_properties.get('rolls')}')
    print(f'      Tiquets para forzar tipo: {game_properties.get('tickets')}')
    print(f'      Dinero: {game_properties.get('money')} monedas')
    print(f'      Puntos de items: {game_properties.get('item_points')}')

def print_filters(gamename):
    response = requests.get(API_URL_GAMEMODE+gamename)
    gamemode:dict = response.json()
    print('\nFiltros:')
    print(f' - filtrar por generación')
    print(f'   - obtener Pokémon hasta la generación: {gamemode.get('generation')}')
    print(f' - filtrar por categoría')
    print(f'   - mythical: {str(bool(gamemode.get('mythical')))}')
    print(f'   - legendary: {str(bool(gamemode.get('legendary')))}')
    print(f'   - sublegendary: {str(bool(gamemode.get('sublegendary')))}')
    print(f'   - powerhouse: {str(bool(gamemode.get('powerhouse')))}')
    print(f' - obtener sólo Pokémon completamente evolucionados: {str(bool(gamemode.get('fully_evolved')))}')
    print(f' - obtener habilidades randomizadas: {str(bool(gamemode.get('random_ability')))}')
    #print(f'   - el resto de Pokémon: {gamemode.get('')}')
    # print(f' - obtener sólo Pokémon que puedan mega-evolucionar: {gamemode.get('')}')
    # print(f' - obtener sólo Pokémon que puedan gigamaxizar: {gamemode.get('')}')


def print_box():
    pass

def roll(username:str, gamename:str, spend_ticket:bool=False):
    response = requests.get(API_URL_USER_GAME_ROLL.format(username, gamename))
    print('\n')
    print(response.text)

def open_menu_cards():
    pass


open_menu()