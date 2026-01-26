from os import system
from numpy import isnan

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
    user_system.active_user.reset()
    user_system.save_data()
    print('\nLa caja ha sido vaciada.')

def print_active_user():
    print(f'\nUsuario: {user_system.active_user.username}')
    print(f'Dinero: {user_system.active_user.money}')

def box_is_full():
    if user_system.active_user.pokemon_box.is_full():
        maxSizeBox = user_system.active_user.pokemon_box.max_size
        print(f'\nSe ha alcanzado el límite de Pokémon en la caja ({maxSizeBox}/{maxSizeBox}). No se pueden obtener más Pokémon.')
        return True


def check_card_conditions(card):
    if card is None:
        return False

    if not card_manager.can_use_card(card.tag, user_system.active_user):
        print('\nNo puedes usar esa carta porque ya has superado su límite de usos.')
        return False

    if not user_system.can_pay(card.price):
        print('\nNo tienes suficiente dinero para comprar esa carta.')
        return False

    return True

def get_pokemon(filtersMask=None):
    if box_is_full():
        return

    pokemon = database.get_random_pokemon(user_system.active_user.pokemon_box.box, filtersMask)

    if pokemon is None:
        print('\nNingún Pokémon cumple con los criterios de búsqueda.')
        return
    
    # mostrar y guardar pokemon
    print_pokemon(pokemon)
    user_system.add_pokemon_in_box(pokemon['id'])

def get_pokemon_with_card_mega():
    tag = 'mega'
    card = card_manager.cards.get(tag, None)

    if not check_card_conditions(card):
        return

    if box_is_full():
        return
    
    # usar carta
    card_manager.add_used_card(tag, user_system.active_user)
    user_system.pay(card.price)

    filtersMask = database.df_filtered.has_mega
    
    get_pokemon(filtersMask)

def get_pokemon_with_card_fusion():

    tag = 'fusion'
    card = card_manager.cards.get(tag, None)

    if not check_card_conditions(card):
        return

    if user_system.active_user.pokemon_box.get_length()<2:
        print('\nNo se puede usar porque no tienes más de 2 Pokémon.')
        return

    try:
        print('\nEscribe el número de la posición del primer Pokémon a eliminar:')
        option1 = int(input()) - 1
        print('\nEscribe el número de la posición del segundo Pokémon a eliminar:')
        option2 = int(input()) - 1
    except:
        print('\nError: Posición no detectada.')
        return

    if (
        not user_system.active_user.pokemon_box.position_is_in_range(pokemon_positions[0]) 
        or 
        not user_system.active_user.pokemon_box.position_is_in_range(pokemon_positions[1])
    ):
        print('\nError: Posiciones no detectadas.')
        return

    # usar carta
    card_manager.add_used_card(tag, user_system.active_user)
    user_system.pay(card.price)

    user_system.active_user.pokemon_box.delete_pokemon(pokemon_positions[0])
    user_system.active_user.pokemon_box.delete_pokemon(pokemon_positions[1])
    get_pokemon()

def get_pokemon_with_card_intercambio():

    tag = 'intercambio'
    card = card_manager.cards.get(tag, None)

    if not check_card_conditions(card):
        return

    if user_system.active_user.pokemon_box.get_length()==0:
        print('\nNo se puede usar porque no tienes ningún Pokémon.')
        return

    try:
        print('\nEscribe el número de la posición del Pokémon a intercambiar:')
        pokemon_position = int(input()) - 1
    except:
        print('\nError: Posición no detectada.')
        return
    
    if (
        not user_system.active_user.pokemon_box.position_is_in_range(pokemon_position) 
    ):
        print('\nError: Posición no detectada.')
        return

    # usar carta
    card_manager.add_used_card(tag, user_system.active_user)
    user_system.pay(card.price)

    user_system.active_user.pokemon_box.delete_pokemon(pokemon_position)
    get_pokemon()

def get_pokemon_with_card_preevo():

    tag = 'preevo'
    card = card_manager.cards.get(tag, None)

    if not check_card_conditions(card):
        return

    if user_system.active_user.pokemon_box.get_length()==0:
        print('\nNo se puede usar porque no tienes ningún Pokémon.')
        return

    try:
        print('\nEscribe el número de la posición del Pokémon que quieres cambiar por su pre-evolución:')
        pokemon_position = int(input()) - 1
    except:
        print('\nError: Posición no detectada.')
        return
    
    if (
        not user_system.active_user.pokemon_box.position_is_in_range(pokemon_position) 
    ):
        print('\nError: Posición no detectada.')
        return
    
    pokemon_id = user_system.active_user.pokemon_box.get_pokemon(pokemon_position)
    preevo_id = database.df.loc[pokemon_id].evolves_from_pokemon_id

    if isnan(preevo_id):
        print('\nError: El Pokémon seleccionado no tiene pre-evolución.')
        return

    # usar carta
    card_manager.add_used_card(tag, user_system.active_user)
    user_system.pay(card.price)
    
    user_system.active_user.pokemon_box.delete_pokemon(pokemon_position)

    #get_pokemon()
    pokemon = database.df.loc[preevo_id].to_dict()

    # mostrar y guardar pokemon
    print_pokemon(pokemon)
    user_system.active_user.pokemon_box.box[pokemon_position] = preevo_id
    user_system.save_data()

def get_pokemon_with_card_comienzo():
    tag = 'comienzo'
    card = card_manager.cards.get(tag, None)

    if not check_card_conditions(card):
        return

    if user_system.active_user.pokemon_box.get_length()>=18:
        print('\nNo se puede usar porque ya se han realizado más de 18 tiradas.')
        return

    # usar carta
    card_manager.add_used_card(tag, user_system.active_user)
    user_system.pay(card.price)

    user_system.active_user.pokemon_box.init_box()
    print('\nTiradas reiniciadas.')

def get_pokemon_with_card_type(pokemon_type):
    tag = 'tipo'
    card = card_manager.cards.get(tag, None)

    if not check_card_conditions(card):
        return

    if box_is_full():
        return

    # usar carta
    card_manager.add_used_card(tag, user_system.active_user)
    user_system.pay(card.price)
    
    filtersMask = (
        (database.df_filtered.first_type==pokemon_type) 
        | 
        (database.df_filtered.second_type==pokemon_type)
    )

    get_pokemon(filtersMask)

def get_pokemon_with_card_aditional(number_ad):
    tag = 'adicional_' + str(number_ad)
    card = card_manager.cards.get(tag, None)

    if not check_card_conditions(card):
        return

    if box_is_full():
        return

    # usar carta
    card_manager.add_used_card(tag, user_system.active_user)
    user_system.pay(card.price)

    for _ in range(number_ad):
        get_pokemon()

def get_pokemon_with_card_selectiva():
    tag = 'selectiva'
    card = card_manager.cards.get(tag, None)

    if not check_card_conditions(card):
        return

    if box_is_full():
        return

    # usar carta
    card_manager.add_used_card(tag, user_system.active_user)
    user_system.pay(card.price)

    for _ in range(6):
        get_pokemon()


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
    box = user_system.active_user.pokemon_box.box
    maxSizeBox = user_system.active_user.pokemon_box.max_size
    if len(box)==0:
        print(f'\nLa caja está vacía. 0/{maxSizeBox}')
        for n in range(user_system.active_user.pokemon_box.max_size):
            print(f' - {n+1}:\t*')
    else:
        print(f'\nLista de Pokémon obtenidos: {user_system.active_user.pokemon_box.get_length()}/{maxSizeBox}')
        n=1
        for pokemon_id in box:
            if(pokemon_id):
                print(f' - {n}:\t{database.get_fullname(pokemon_id)}')
            else:
                print(f' - {n}:\t*')
            n+=1


def print_users():
    print('\nUsuarios registrados:')
    for n, user in enumerate(user_system.users):
        print(f' - {n+1}:\t{user.username}')


def open_menu_users():

    while(True):
        print_users()
        print(menu_users)
        print('\nEscribe el número de la opción:')

        option = input()
        clear()
        
        print_users()

        print(f'\nSeleccionada opción {option}')

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
                if user_system.change_active_user(n):
                    # volver al menu principal
                    clear()
                    return
                else:
                    print('Usuario no encontrado.')
            
        #- 2: Crear nuevo usuario
        elif(option=='2'):

            if user_system.can_add_user():
                print('\nEscribe un nombre para el usuario:')

                while True:
                    name = input()
                    if user_system.username_available(name):
                        print('\nEse nombre ya se encuentra en la base de datos, escribe otro diferente:')
                    else:
                        user_system.add_user(name)
                        clear()
                        break
            else:
                print('La lista de usuarios está llena, borra alguno para hacer hueco.')
            
        #- 3: Eliminar usuario
        elif(option=='3'):

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
                
                if not user_system.position_is_in_range(n):
                    print('Usuario no encontrado.')
                    continue
                
                if user_system.active_user.username == user_system.users[n].username:
                    print('No puedes borrar el usuario activo. Elige otro.')
                    continue
                
                if user_system.delete_user(n):
                    clear()
                    break
                else:
                    print('Usuario no encontrado.')
        #- 0: Salir
        elif(option=='0'):
            return
        else:
            print('Opción no reconocida.')


def open_menu_cards():
    
    clear()
    print_active_user()

    while(True):
        print(line)
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
user_system = UserSystem()
database = PokemonDatabaseManager()
card_manager = CardManager()


while(True):
    print_active_user()
    
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
        database.filter_manager.print_options()
    elif(option=='5'):
        open_menu_cards()
    elif(option=='6'):
        open_menu_users()
    elif(option=='0'):
        clear()
        break
    elif(option=='m'):
        pokemon = database.get_random_pokemon(user_system.active_user.pokemon_box.box)
        if pokemon is not None:
            print_pokemon(pokemon)
            print('\nDictionary:')
            for k,v in pokemon.items():
                print(f' - {k}: {v}')
    else:
        print('Opción no reconocida.')


