from flask import Flask, request, g
import sqlite3
import os.path

import scripts.classes.constants as const

from scripts.controller.users import UsersController
from scripts.controller.gamemodes import GamemodesController
from scripts.controller.games import GamesController
from scripts.controller.game_cards import GameCardsController

from scripts.classes.status_codes import StatusCode
from scripts.classes.game import GameSession
from scripts.classes.cards import Cards


app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(const.DATABASE_FILE)
    return db

def get_connection_and_cursor():
    con = get_db()
    cur = con.cursor()
    return con, cur

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    # crear la base de datos si no existe, salir si ya existe
    if os.path.isfile(const.DATABASE_FILE):
        return

    with app.app_context():
        con, cur = get_connection_and_cursor()
        # schema
        with app.open_resource(const.SCHEMA_FILE, mode='r') as f:
            cur.executescript(f.read())
        # values
        with app.open_resource(const.POKEMON_VALUES_FILE, mode='r') as f:
            cur.executescript(f.read())
        with app.open_resource(const.ABILITIES_VALUES_FILE, mode='r') as f:
            cur.executescript(f.read())
        con.commit()


# USER

@app.route("/user/", methods = ['GET'])
def users():
    con, cur = get_connection_and_cursor()

    controller_users = UsersController(con, cur)

    if request.method == 'GET':
        return controller_users.get_usernames()
    

@app.route("/user/<username>", methods = ['GET','POST','DELETE'])
def user(username):
    con, cur = get_connection_and_cursor()

    controller_users = UsersController(con, cur)

    if request.method == 'GET':
        user = controller_users.get_user(username)
        if not user:
            return StatusCode.not_found()

        controller_gamemodes = GamemodesController(con, cur)

        # add gamenames
        user_id = user.get('user_id')
        user['games'] = controller_gamemodes.db_gamemodes.get_gamenames_of_user(user_id)
        return user
    
    elif request.method == 'POST':
        user_id = controller_users.get_user_id(username)
        if user_id is not None:
            return StatusCode.duplicated()
            
        controller_users.insert_user(username)

        # return user
        user = controller_users.get_user(username)
        return user
    
    elif request.method == 'DELETE':
        user_id = controller_users.get_user_id(username)
        if user_id is None:
            return StatusCode.not_found()
        
        # delete user
        controller_users.delete_user(user_id)
        
        # delete games
        controller_games = GamesController(con, cur)
        controller_games.delete_games_of_user(user_id)
        
        return StatusCode.ok()


# GAMEMODES

@app.route("/game/", methods=['GET'])
def gamemodes():
    con, cur = get_connection_and_cursor()

    controller_gamemodes = GamemodesController(con, cur)

    if request.method == 'GET':
        return controller_gamemodes.get_all_gamemode_names()


@app.route("/game/<gamename>", methods=['GET','POST','DELETE'])
def gamemode(gamename):
    con, cur = get_connection_and_cursor()

    controller_gamemodes = GamemodesController(con, cur)

    if request.method == 'GET':
        gamemode_id = controller_gamemodes.get_gamemode_id(gamename)
        if gamemode_id is None:
            return StatusCode.not_found()
        
        gamemode = controller_gamemodes.get_gamemode(gamemode_id)
        return gamemode
    
    if request.method == 'POST':
        gamemode_id = controller_gamemodes.get_gamemode_id(gamename)
        if gamemode_id is not None:
            return StatusCode.duplicated()

        dic_options = request.form
        controller_gamemodes.create_gamemode(gamename, dic_options)
        
        # return gamemode
        gamemode = controller_gamemodes.get_gamemode_wih_name(gamename)
        return gamemode
    
    elif request.method == 'DELETE':
        gamemode_id = controller_gamemodes.get_gamemode_id(gamename)
        if gamemode_id is None:
            return StatusCode.not_found()
        
        # delete gamemode
        controller_gamemodes.delete_gamemode(gamemode_id)
        
        # delete games
        controller_games = GamesController(con, cur)
        controller_games.delete_games_of_gamemode(gamemode_id)
        
        return StatusCode.ok()


# GAME

@app.route("/user/<username>/game/<gamename>", methods=['GET','POST','DELETE'])
def game(username, gamename):
    con, cur = get_connection_and_cursor()

    controller_users = UsersController(con, cur)
    
    user_id = controller_users.get_user_id(username)
    if user_id is None:
        return StatusCode.not_found()

    controller_games = GamesController(con, cur)

    if request.method == 'GET':
        gamemode_id = controller_games.db_gamemodes.get_gamemode_id(gamename)
        if gamemode_id is None:
            return StatusCode.not_found()
        
        game_id = controller_games.get_game_id(user_id, gamemode_id)
        if game_id is None:
            return StatusCode.not_found()
        
        # return game dictionary
        game = controller_games.get_game(game_id)
        game_dict = controller_games.get_simple_game_dict(game)
        return game_dict
    
    if request.method == 'POST':
        gamemode_id = controller_games.db_gamemodes.get_gamemode_id(gamename)
        if gamemode_id is None:
            return StatusCode.not_found()
        
        game_id = controller_games.get_game_id(user_id, gamemode_id)
        if game_id is not None:
            return StatusCode.duplicated()
        
        controller_games.create_game(user_id, gamemode_id)

        # return game dictionary
        game_id = controller_games.get_game_id(user_id, gamemode_id)
        game = controller_games.get_game(game_id)
        game_dict = controller_games.get_simple_game_dict(game)
        return game_dict
    
    elif request.method == 'DELETE':
        gamemode_id = controller_games.db_gamemodes.get_gamemode_id(gamename)
        if gamemode_id is None:
            return StatusCode.not_found()
        
        game_id = controller_games.get_game_id(user_id, gamemode_id)
        if game_id is None:
            return StatusCode.not_found()
        
        controller_games.delete_game(user_id)

        return StatusCode.ok()


# ROLL

@app.route("/user/<username>/game/<gamename>/roll", methods=['GET'])
def do_roll(username, gamename):
    con, cur = get_connection_and_cursor()

    controller_users = UsersController(con, cur)

    user_id = controller_users.get_user_id(username)
    if user_id is None:
        return StatusCode.not_found()
    
    controller_games = GamesController(con, cur)

    gamemode_id = controller_games.db_gamemodes.get_gamemode_id(gamename)
    if gamemode_id is None:
        return StatusCode.not_found()
    
    game_id = controller_games.get_game_id(user_id, gamemode_id)
    if game_id is None:
        return StatusCode.not_found()

    game = controller_games.get_game(game_id)

    pokemon_type = request.args.get('type')

    pokemon = controller_games.do_roll(game, pokemon_type)
    if not pokemon:
        return {}

    data = controller_games.pokemon.get_pokemon_important_data(
        pokemon.get('pokemon_id'), 
        pokemon.get('random_ability_id')
    )
    return data


# CARD

@app.route("/user/<username>/game/<gamename>/card/<card_tag>", methods=['GET','POST'])
def use_card(username, gamename, card_tag):
    con, cur = get_connection_and_cursor()

    controller_users = UsersController(con, cur)

    user_id = controller_users.get_user_id(username)
    if user_id is None:
        return StatusCode.not_found()

    controller_games = GamesController(con, cur)
    
    gamemode_id = controller_games.db_gamemodes.get_gamemode_id(gamename)
    if gamemode_id is None:
        return StatusCode.not_found()
    
    game_id = controller_games.get_game_id(user_id, gamemode_id)
    if game_id is None:
        return StatusCode.not_found()
    
    game = controller_games.get_game(game_id)
    
    controller_gamecards = GameCardsController(controller_games)

    if card_tag == Cards.TAG_MEGA:
        pokemon = controller_gamecards.use_card_mega(game)
        return pokemon
    elif card_tag == Cards.TAG_FUSION:
        pokemon_id1 = int(request.form.get('pokemon_id1'))
        pokemon_id2 = int(request.form.get('pokemon_id2'))
        pokemon = controller_gamecards.use_card_fusion(game,pokemon_id1,pokemon_id2)
        return pokemon
    elif card_tag == Cards.TAG_INTERCAMBIO:
        pokemon_id = int(request.form.get('pokemon_id'))
        pokemon = controller_gamecards.use_card_intercambio(game,pokemon_id)
        return pokemon
    elif card_tag == Cards.TAG_PREEVO:
        pokemon_id = int(request.form.get('pokemon_id'))
        pokemon = controller_gamecards.use_card_preevo(game,pokemon_id)
        return pokemon
    elif card_tag == Cards.TAG_COMIENZO:
        controller_gamecards.use_card_comienzo(game)
    elif card_tag == Cards.TAG_2_POWERHOUSE:
        controller_gamecards.use_card_powerhouse(game)
    elif card_tag == Cards.TAG_TICKET_TIPO:
        controller_gamecards.use_card_tiquet_tipo(game)
    elif card_tag == Cards.TAG_ADICIONAL_1:
        controller_gamecards.use_card_aditional(game, 1)
    elif card_tag == Cards.TAG_ADICIONAL_2:
        controller_gamecards.use_card_aditional(game, 2)
    elif card_tag == Cards.TAG_ADICIONAL_3:
        controller_gamecards.use_card_aditional(game, 3)
    elif card_tag == Cards.TAG_SELECTIVA:
        # primera parte
        if request.method == 'GET':
            pokemon_list = controller_gamecards.use_card_selectiva(game)
            return { 'pokemon_list':pokemon_list }
        # segunda parte
        elif request.method == 'POST':
            pokemons = request.form
            controller_gamecards.use_card_selectiva_final(game, pokemons)

    return { 'success':True }


# POKEMON

@app.route("/random_pokemon", methods=['GET'])
def random_pokemon():
    con, cur = get_connection_and_cursor()

    controller_games = GamesController(con, cur)

    game = GameSession(game_id=0, user_id=0, gamename='')
    pokemon = controller_games.pokemon.get_random_pokemon(game)

    data = controller_games.pokemon.get_pokemon_important_data(
        pokemon.get('pokemon_id')
    )
    return data


init_db()

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)