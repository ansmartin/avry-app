
from scripts.db import DatabaseModel
from scripts.controller.users import UsersController
from scripts.controller.games import GamesController
from scripts.controller.game_cards import GameCardsController


class AppController:
    
    def __init__(self, connection):
        self.db = DatabaseModel(connection)
        self.games = GamesController(self.db)
        self.users = UsersController(self.db, self.games)
        self.game_cards = GameCardsController(self.games)
