import sqlite3

import scripts.constants as const
from scripts.app_controller import AppController
from scripts.menus import MenuManager

try:
    connection = sqlite3.connect(const.DATABASE_PATH)

    app = AppController(connection)

    menu = MenuManager(app)
    menu.open_menu_users()
finally:
    print('Closing database connection')
    connection.close()
