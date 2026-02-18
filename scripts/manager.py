
from scripts.db import DatabaseManager
from scripts.manager_users import UserManager
from scripts.manager_games import GameSessionManager


class AppManager:
    
    def __init__(self, connection):
        self.db = DatabaseManager(connection)
        self.user_manager = UserManager(self.db)
        self.game_manager = GameSessionManager(self.db)

        self.user_manager.set_game_manager(self.game_manager)
