from scripts.users import UserSystem
from scripts.game import GameSessionManager
from scripts.pokemon import PokemonDatabaseManager
from scripts.cards import CardManager
from scripts.menus import MenuManager

database = PokemonDatabaseManager()
user_system = UserSystem()
game_manager = GameSessionManager(user_system, database)
card_manager = CardManager()

menu = MenuManager(user_system, game_manager, database, card_manager)
menu.open_menu_users()
