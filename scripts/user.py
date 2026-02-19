
class User:

    MAX_GAMES = 128

    def __init__(self, user_id:int, username:str, games:list = None):
        self.user_id = user_id
        self.username = username
        self.games = games if games else []
