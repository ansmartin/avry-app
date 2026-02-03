from scripts.db import DatabaseManager
from scripts.pokemon import PokemonDatabaseManager
from scripts.users import UserSystem
from scripts.game import GameSessionManager
from scripts.cards import CardManager
from scripts.menus import MenuManager

try:
    db = DatabaseManager()
    database = PokemonDatabaseManager()
    user_system = UserSystem(db)
    game_manager = GameSessionManager(user_system, database)
    card_manager = CardManager()

    menu = MenuManager(user_system, game_manager, database, card_manager)
    menu.open_menu_users()
finally:
    print('Closing database connection')
    db.connection.close()
