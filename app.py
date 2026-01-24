from os import system
from scripts.users import UserSystem
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

def empty_box():
    userSystem.activeUser.pokemonBox.init_box()
    userSystem.save_data()
    print('\nLa caja ha sido vaciada.')


def get_pokemon():
    if(userSystem.activeUser.pokemonBox.is_full()):
        maxBoxSize = userSystem.activeUser.pokemonBox.size
        print(f'\nSe ha alcanzado el límite de Pokémon en la caja ({maxBoxSize}/{maxBoxSize}). No se pueden obtener más Pokémon.')
        return

    pokemon = database.get_random_pokemon(userSystem.activeUser.pokemonBox.box)
    
    # mostrar y guardar pokemon
    print_pokemon(pokemon)
    userSystem.add_pokemon_in_box(pokemon['id'])


def print_pokemon(pokemon):

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


def print_box():
    box = userSystem.activeUser.pokemonBox.get_box()
    maxBoxSize = userSystem.activeUser.pokemonBox.size
    if box is None:
        print(f'\nLa caja está vacía. 0/{maxBoxSize}')
        for n in range(userSystem.activeUser.pokemonBox.size):
            print(f' - {n+1}:\t*')
    else:
        print(f'\nLista de Pokémon obtenidos: {userSystem.activeUser.pokemonBox.number_of_pokemon_stored}/{maxBoxSize}')
        n=1
        for pokemon_id in box:
            if(pokemon_id):
                print(f' - {n}:\t{database.get_fullname(pokemon_id)}')
            else:
                print(f' - {n}:\t*')
            n+=1


def print_users():
    print('\nUsuarios registrados:')
    for n, user in enumerate(userSystem.users):
        print(f' - {n+1}:\t{user.username}')


def load_user():

    while(True):
        print_users()
        print(menu_users)
        print('\nEscribe el número de la opción:')

        option = input()
        clear()

        print_users()

        print(f'Seleccionada opción {option}')

        #- 1: Cargar usuario
        if(option=='1'):

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
                if userSystem.change_active_user(n):
                    # volver al menu principal
                    clear()
                    return
                else:
                    print('Usuario no encontrado.')
            
        #- 2: Crear nuevo usuario
        elif(option=='2'):

            if userSystem.can_add_user():
                print('\nEscribe un nombre para el usuario:')
                name = input()

                while True:
                    if userSystem.username_available(name):
                        print('\nEse nombre ya se encuentra en la base de datos, escribe otro diferente:')
                        name = input()
                    else:
                        userSystem.add_user(name)
                        clear()
                        break
            else:
                print('La lista de usuarios está llena, borra alguno para hacer hueco.')
            
        #- 3: Eliminar usuario
        elif(option=='3'):

            while(True):
                print('\nEscribe el número del usuario que quieres eliminar.\nEscribe 0 para cancelar.')
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
                
                if not userSystem.position_is_in_range(n):
                    print('Usuario no encontrado.')
                    continue
                
                if userSystem.activeUser.username == userSystem.users[n].username:
                    print('No puedes borrar el usuario activo. Elige otro.')
                    continue
                
                if userSystem.delete_user(n):
                    clear()
                    break
                else:
                    print('Usuario no encontrado.')
        #- 0: Salir
        elif(option=='0'):
            return
        else:
            print('Opción no reconocida.')


def open_cards_menu():
    
    while(True):
        clear()
        print('\n    Lista de cartas de ventaja:')
        n=1
        for c in cardManager.cards.values():
            print(f'\n    - {n}: {c.name}')
            print(f'        {c.description}')
            n+=1
        print('\n    - 0: Volver al menú principal')
        print('\nEscribe el número de la opción:')

        option = input()
        clear()

        print(f'Seleccionada opción {option}')
        
        if(option=='1'):
            get_random_pokemon_mega()
        
        #- 0: Salir
        elif(option=='0'):
            return
        else:
            print('Opción no reconocida.')


def get_random_pokemon_mega():
    tag = 'mega'
    card = cardManager.cards.get(tag, None)
    if card is None:
        return

    if userSystem.activeUser.can_pay_card(card.price) and cardManager.can_use_card(tag, user):
        if(userSystem.activeUser.pokemonBox.is_full()):
            print('\nNo se puede usar porque se ha alcanzado el límite de Pokémon en la caja.')
            return
        



menu = """\n
MENU PRINCIPAL

    Opciones:
    - 1: Realizar tirada
    - 2: Ver caja
    - 3: Reiniciar caja
    - 4: Mostrar filtros activos
    - 5: Usar carta de ventaja
    - 6: Cambiar de usuario

    - 0: Cerrar aplicación
"""
menu_users = """\n
    Opciones:
    - 1: Cargar usuario
    - 2: Crear nuevo usuario
    - 3: Eliminar usuario

    - 0: Volver al menú principal
"""

line = '\n------------------------------------'


clear()
userSystem = UserSystem()
database = PokemonDatabaseManager()
cardManager = CardManager()


while(True):
    print(f'\nUsuario: {userSystem.activeUser.username}')
    
    print(line + menu + line)
    print('\nEscribe el número de la opción:')

    option = input()
    clear()

    print(f'Seleccionada opción {option}')

    if(option=='1'):
        get_pokemon()
    elif(option=='2'):
        print_box()
    elif(option=='3'):
        empty_box()
    elif(option=='4'):
        database.filterManager.print_options()
    elif(option=='5'):
        open_cards_menu()
    elif(option=='6'):
        load_user()
    elif(option=='0'):
        clear()
        break
    elif(option=='m'):
        pokemon = database.get_random_pokemon(userSystem.activeUser.pokemonBox.box)
        if pokemon is not None:
            print_pokemon(pokemon)
            print('\nDictionary:')
            for k,v in pokemon.items():
                print(f' - {k}: {v}')
    else:
        print('Opción no reconocida.')


