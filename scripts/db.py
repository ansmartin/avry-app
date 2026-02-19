from sqlite3 import Connection, Cursor

from scripts.database.users import UsersDatabase
from scripts.database.games import GamesDatabase
from scripts.database.rolls import RollsDatabase
from scripts.database.cards import CardsDatabase
from scripts.database.pokemon import PokemonDatabase
from scripts.database.abilities import AbilitiesDatabase


class DatabaseModel:
    
    def __init__(self, connection:Connection):
        self.connection = connection
        self.cur = self.connection.cursor()

        self.users = UsersDatabase(self.connection, self.cur)
        self.games = GamesDatabase(self.connection, self.cur)
        self.rolls = RollsDatabase(self.connection, self.cur)
        self.cards = CardsDatabase(self.connection, self.cur)
        self.pokemon = PokemonDatabase(self.connection, self.cur)
        self.abilities = AbilitiesDatabase(self.connection, self.cur)
