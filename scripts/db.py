from sqlite3 import Connection, Cursor

from scripts.db_users import UsersDatabase
from scripts.db_games import GamesDatabase
from scripts.db_rolls import RollsDatabase
from scripts.db_cards import CardsDatabase
from scripts.db_pokemon import PokemonDatabase
from scripts.db_abilities import AbilitiesDatabase


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
