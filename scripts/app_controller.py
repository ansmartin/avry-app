
from scripts.controller.users import UsersController
from scripts.controller.games import GamesController
from scripts.controller.game_cards import GameCardsController


class AppController:
    
    def __init__(self, connection, cursor):

        self.games = GamesController(connection, cursor)
        self.users = UsersController(connection, cursor, self.games)

        self.game_cards = GameCardsController(self.games)
