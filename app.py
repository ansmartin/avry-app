from numpy import isnan

from scripts.users import UserSystem
from scripts.game import GameSessionManager
from scripts.database import PokemonDatabaseManager
from scripts.cards import CardManager
from scripts.menus import MenuManager


def empty_box():
    user_system.active_user.reset()
    user_system.save_data()
    print('\nLa caja ha sido vaciada.')



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

    mask = database.df_filtered.has_mega
    
    get_pokemon(mask)

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
        not user_system.active_user.pokemon_box.position_is_in_range(position1) 
        or 
        not user_system.active_user.pokemon_box.position_is_in_range(position2)
    ):
        print('\nError: Posiciones no detectadas.')
        return

    # usar carta
    card_manager.add_used_card(tag, user_system.active_user)
    user_system.pay(card.price)

    # ajustar segunda posicion para cuando se borre la primera
    if position1 < position2:
        position2-=1

    user_system.active_user.pokemon_box.delete_pokemon(position1)
    user_system.active_user.pokemon_box.delete_pokemon(position2)
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
    user_system.active_user.pokemon_box.poke_list[pokemon_position] = preevo_id
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
    
    mask = (
        (database.df_filtered.first_type==pokemon_type) 
        | 
        (database.df_filtered.second_type==pokemon_type)
    )

    get_pokemon(mask)

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





user_system = UserSystem()
game_manager = GameSessionManager(user_system)
database = PokemonDatabaseManager()
card_manager = CardManager()


menu = MenuManager(user_system, game_manager, database, card_manager)
menu.open_menu_users()
