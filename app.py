import sqlite3

import scripts.constants as const
from scripts.game import GameSessionManager
from scripts.menus import MenuManager

try:
    connection = sqlite3.connect(const.DATABASE_PATH)

    game_manager = GameSessionManager(connection)

    menu = MenuManager(game_manager)
    menu.open_menu_users()
finally:
    print('Closing database connection')
    connection.close()
