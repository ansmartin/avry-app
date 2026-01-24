from os import system
from scripts.users import UserSystem
from scripts.database import PokemonDatabaseManager


def clear():
    system("clear||cls")

def capitalize_name(text):
    words = text.split('-')
    return '-'.join(w.capitalize() for w in words)

def capitalize_all_words(text):
    words = text.replace('-',' ').split()
    return ' '.join(w.capitalize() for w in words)

def save_pokemon(pokemon_id):
    user.pokemonBox.save_pokemon(pokemon_id)
    userSystem.save_data()

def empty_box():
    user.pokemonBox.init_box()
    userSystem.save_data()
    print('\nLa caja ha sido vaciada.')

def print_pokemon_data():
    if(user.pokemonBox.is_full()):
        print('\nSe ha alcanzado el límite de Pokémon en la caja.')
        return

    x = database.get_random_pokemon()

    evolutions = None
    for element in x['evolutions_ids']:
        if(evolutions is None):
            evolutions = str(element)
        else:
            evolutions = evolutions + ',' + str(element)
        
    x['evolutions_ids'] = evolutions
    #print(json.dumps(x, indent=4))

    species_name = x['species_name']
    form_name_text = x['form_name_text']

    first_type = x['first_type']
    second_type = x['second_type']

    first_ability = x['first_ability']
    second_ability = x['second_ability']
    hidden_ability = x['hidden_ability']

    pokemon_generation_number = x['pokemon_generation_number']
    evolves_from_pokemon_id = x['evolves_from_pokemon_id']
    is_default = x['is_default']
    is_baby = x['is_baby']
    is_powerhouse = x['is_powerhouse']
    is_legendary = x['is_legendary']
    is_sublegendary = x['is_sublegendary']
    is_mythical = x['is_mythical']
    has_mega = x['has_mega']
    has_gmax = x['has_gmax']
    sprite_default = x['sprite_default']

    print('\nPokémon aleatorio obtenido:')

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
    save_pokemon(x['id'])


def print_box():
    box = user.pokemonBox.get_box()
    if box is None:
        print('\nLa caja está vacía. 0/20')
        for n in range(user.pokemonBox.size):
            print(f' - {n+1}:\t*')
    else:
        print(f'\nLista de Pokémon obtenidos: {user.pokemonBox.number_of_pokemon_stored}/20')
        n=1
        for pokemon_id in box:
            if(pokemon_id):
                print(f' - {n}:\t{database.get_fullname(pokemon_id)}')
            else:
                print(f' - {n}:\t*')
            n+=1


def print_users():
    print('\nUsuarios registrados:')

    for n, u in enumerate(userSystem.users):
        print(f' - {n+1}:\t{u.username}')


def load_user():
    global user

    while(True):
        print_users()
        print(menu_users)
        print('\nEscribe el número de la opción:')

        option = input()
        clear()

        print(f'Seleccionada opción {option}')

        #- 1: Cargar usuario
        if(option=='1'):
            if(len(userSystem.users)==0):
                print('\nNo hay usuarios guardados, crea uno primero.')
                continue

            print_users()

            while(True):
                print('\nEscribe el número del usuario que quieres cargar:')

                option = input()

                try:
                    n = int(option)
                    n-=1
                except:
                    print('Número no reconocido.')
                    continue

                user = userSystem.get_user(n)
                if(user):
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
            if(len(userSystem.users)==0):
                print('\nNo hay usuarios guardados, crea uno primero.')
                continue

            print_users()

            while(True):
                print('\nEscribe el número del usuario que quieres eliminar.\nEscribe 0 para cancelar.')
                option = input()
                
                try:
                    n = int(option)
                    n-=1
                except:
                    print('Número no reconocido.')
                    continue

                if n < 0:
                    clear()
                    break
                
                if user.username == userSystem.users[n].username:
                    print('No puedes borrar el usuario activo. Elige otro.')
                    continue
                
                if userSystem.delete_user(n):
                    clear()
                    break
                else:
                    print('Usuario no encontrado.')
        #- 9: Salir
        elif(option=='9'):
            if user is None:
                quit()
            else:
                return
        else:
            print('Opción no reconocida.')
            



menu = """\n
MENU PRINCIPAL

    Opciones:
    - 1: Cambiar de usuario
    - 2: Obtener Pokémon aleatorio
    - 3: Ver caja
    - 4: Reiniciar caja
    - 5: Mostrar filtros activos

    - 9: Cerrar aplicación
"""
menu_users = """\n
    Opciones:
    - 1: Cargar usuario
    - 2: Crear nuevo usuario
    - 3: Eliminar usuario

    - 9: Volver al menú principal
"""

line = '\n------------------------------------'


clear()
userSystem = UserSystem()
user = userSystem.get_user(0)
database = PokemonDatabaseManager()


while(True):
    print(f'\nUsuario: {user.username}')
    
    print(line + menu + line)
    print('\nEscribe el número de la opción:')

    option = input()
    clear()

    print(f'Seleccionada opción {option}')

    if(option=='1'):
        load_user()
    elif(option=='2'):
        print_pokemon_data()
    elif(option=='3'):
        print_box()
    elif(option=='4'):
        empty_box()
    elif(option=='5'):
        database.filterManager.print_options()
    elif(option=='9'):
        clear()
        break
    elif(option=='m'):
        pokemon = database.get_random_pokemon()
        if pokemon is not None:
            print('\nPokemon:')
            for k,v in pokemon.items():
                print(f' - {k}: {v}')
    else:
        print('Opción no reconocida.')


