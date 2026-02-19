
from scripts.db import DatabaseModel
from scripts.controller.users import UsersController


class AppController:
    
    def __init__(self, connection):
        self.db = DatabaseModel(connection)
        self.users = UsersController(self.db)
