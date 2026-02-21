from scripts.database.rolls import RollsDatabase

class RollsController:

    def __init__(self, connection, cursor):
        self.db_rolls = RollsDatabase(connection, cursor)
