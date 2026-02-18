import sqlite3

import scripts.constants as const
from scripts.manager import AppManager
from scripts.menus import MenuManager

try:
    connection = sqlite3.connect(const.DATABASE_PATH)

    app = AppManager(connection)

    menu = MenuManager(app)
    menu.open_menu_users()
finally:
    print('Closing database connection')
    connection.close()
