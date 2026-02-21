import sqlite3

import scripts.constants as const
from scripts.app_controller import AppController
from scripts.menus import MenuManager

try:
    connection = sqlite3.connect(const.DATABASE_PATH)
    cursor = connection.cursor()

    app = AppController(connection, cursor)

    menu = MenuManager(app)
    menu.open_menu_users()
finally:
    print('Closing database connection')
    connection.close()
