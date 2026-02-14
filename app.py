from scripts.db import DatabaseManager
from scripts.game import GameSessionManager
from scripts.menus import MenuManager

try:
    db = DatabaseManager()
    game_manager = GameSessionManager(db)

    menu = MenuManager(game_manager)
    menu.open_menu_users()
finally:
    print('Closing database connection')
    game_manager.db.connection.close()
