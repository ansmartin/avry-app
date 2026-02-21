from scripts.db import DatabaseModel

class RollsController:

    def __init__(self, db:DatabaseModel):
        self.db_rolls = db.rolls
