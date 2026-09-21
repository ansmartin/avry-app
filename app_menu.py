import requests
from os import system


API_URL = 'http://localhost:8080'
API_URL_GAMEMODE = API_URL + '/game/'
API_URL_USER = API_URL + '/user/'


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
    - 1: Ver partidas a las que te has apuntado
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

    - 9: Elegir otra sesión de juego
    - 0: Cerrar aplicación
"""
TEXT_MENU_PLAY_GAME = TEXT_LINE + TEXT_MENU_PLAY_GAME + TEXT_LINE

TEXT_INSERT_NUMBER = '\nEscribe el número de la opción:'

TEXT_SELECTED_OPTION = '\nSeleccionada opción {}'

TEXT_OPTION_NOT_RECOGNIZED = 'Opción no reconocida.'

TEXT_POKEMON_SEARCH_ERROR = '\nNingún Pokémon cumple con los criterios de búsqueda.'


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
                print('No hay modos de juego registrados.')
                continue

            print('\nModos de juego:')
            for x in gamenames_list:
                print('- {}'.format(x))

        #- 2: Crear nuevo modo de juego
        elif(option=='2'):
                
            print('\nEscribe un nombre para el nuevo modo de juego:')
            name = input()

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

                # print('\n¿Incluir los demás Pokémon que no pertenezcan a estas categorías? Escribe 1 para sí, escribe otra cosa para no.')
                # options['others'] = input()=='1'

                print('\nFiltrar por etapa evolutiva del Pokémon.')
                print('¿Incluir solamente Pokémon en su última etapa evolutiva? Escribe 1 para sí, escribe otra cosa para no.')
                options['fully_evolved'] = input()=='1'

                print('\n¿Obtener habilidades randomizadas? (De cualquier Pokémon posible) Escribe 1 para sí, escribe otra cosa para no.')
                options['random_ability'] = input()=='1'

            response = requests.post(API_URL_GAMEMODE+name, json=options)
            print(response.text)

        #- 3: Eliminar modo de juego
        elif(option=='3'):
            response = requests.get(API_URL_GAMEMODE)
            gamenames_list = response.json()

            if not gamenames_list:
                print('No hay modos de juego registrados.')
                continue

            print('\nModos de juego:')
            for x in gamenames_list:
                print('- {}'.format(x))

            print('\nEscribe el nombre del modo de juego que quieres eliminar:')
            name = input()

            response = requests.delete(API_URL_GAMEMODE+name)
            print(response.text)

        #- 0: Salir
        elif(option=='0'):
            clear()
            return
        else:
            print('Opción no reconocida.')



# MENU MANAGE USERS
# =======================================================================

def open_menu_users(self):
    pass


open_menu()