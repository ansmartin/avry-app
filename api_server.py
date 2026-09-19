from flask import Flask, request, g
import sqlite3
import os.path

import scripts.constants as const

from scripts.controller.users import UsersController
from scripts.controller.games import GamesController
from scripts.controller.cards import CardsController
from scripts.controller.rolls import RollsController
from scripts.controller.pokemon import PokemonController
from scripts.controller.abilities import AbilitiesController
from scripts.controller.game_cards import GameCardsController

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

def error_user_not_found():
    return { 'success':False, 'error':'Usuario no encontrado' }

def error_gamemode_not_found():
    return { 'success':False, 'error':'Modo de juego no encontrado' }

def error_game_not_found():
    return { 'success':False, 'error':'Sesión de juego no encontrada' }


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
            return error_user_not_found()
        
        controller_games = GamesController(con, cur)

        # add gamenames
        user_id = user.get('user_id')
        user['games'] = controller_games.db_games.get_gamenames_user(user_id)
        
        return user
    
    elif request.method == 'POST':
        success = controller_users.insert_user(username)
        return { 'success':success }
    
    elif request.method == 'DELETE':
        # delete user
        user_id = controller_users.db_users.get_user_id(username)
        if user_id is None:
            return error_user_not_found()
        success_user = controller_users.delete_user(user_id=user_id)
        # delete games
        controller_games = GamesController(con, cur)
        success_games = controller_games.delete_games_of_user(user_id)

        success = (success_user & success_games)
        if success:
            return { 'success':True }
        else:
            return { 
            'success': False,
            'user':{'success':success_user}, 
            'games':{'success':success_games}
        }


# GAMEMODES

@app.route("/game/", methods=['GET'])
def gamemodes():
    con, cur = get_connection_and_cursor()

    controller_games = GamesController(con, cur)

    if request.method == 'GET':
        return controller_games.db_games.get_gamenames()


@app.route("/game/<gamename>", methods=['GET','POST','DELETE'])
def gamemode(gamename):
    con, cur = get_connection_and_cursor()

    controller_games = GamesController(con, cur)

    if request.method == 'GET' or request.method == 'POST':
        if request.method == 'POST':
            # check not repeated
            gamemode_id = controller_games.db_games.get_gamemode_id(gamename)
            if gamemode_id is not None:
                return { 'success':False }
            dic_options = request.form
            controller_games.create_gamemode(gamename, dic_options)

        # return gamemode dictionary
        gamemode = controller_games.get_gamemode(gamename=gamename)
        if not gamemode:
            return error_gamemode_not_found()
        return gamemode
    
    elif request.method == 'DELETE':
        success = controller_games.delete_gamemode(gamename=gamename)
        return { 'success':success }


# GAME

@app.route("/user/<username>/game/<gamename>", methods=['GET','POST','DELETE'])
def game(username, gamename):
    con, cur = get_connection_and_cursor()

    controller_users = UsersController(con, cur)
    user_id = controller_users.db_users.get_user_id(username)
    if user_id is None:
        return error_user_not_found()

    controller_games = GamesController(con, cur)

    if request.method == 'GET' or request.method == 'POST':
        if request.method == 'POST':
            # check gamemode exists
            gamemode_id = controller_games.db_games.get_gamemode_id(gamename)
            if gamemode_id is None:
                return error_gamemode_not_found()
            # check not repeated
            game_id = controller_games.db_games.get_game_id(user_id, gamemode_id=gamemode_id)
            if game_id is not None:
                return { 'success':False }
            controller_games.create_game(user_id, gamemode_id)

        # return game dictionary
        game = controller_games.get_game(user_id=user_id, gamename=gamename)
        if not game:
            return error_game_not_found()
        game_dict = controller_games.get_game_simplified_dict(game)
        return game_dict
    
    elif request.method == 'DELETE':
        success = controller_games.delete_game(user_id=user_id, gamename=gamename)
        return { 'success':success }


# ROLL

@app.route("/user/<username>/game/<gamename>/roll", methods=['GET'])
def do_roll(username, gamename):
    con, cur = get_connection_and_cursor()

    controller_users = UsersController(con, cur)
    user_id = controller_users.db_users.get_user_id(username)
    if user_id is None:
        return error_user_not_found()

    controller_games = GamesController(con, cur)
    game = controller_games.get_game(user_id=user_id, gamename=gamename)
    if not game:
        return error_game_not_found()

    pokemon_type = request.args.get('type')

    pokemon = controller_games.do_roll(game, pokemon_type)

    data = controller_games.pokemon.get_pokemon_important_data(
        pokemon.get('pokemon_id'), 
        pokemon.get('random_ability_id', None)
    )
    return data


# CARD

@app.route("/user/<username>/game/<gamename>/card/<card_tag>", methods=['GET','POST'])
def use_card(username, gamename, card_tag):
    con, cur = get_connection_and_cursor()

    controller_users = UsersController(con, cur)
    user_id = controller_users.db_users.get_user_id(username)
    if user_id is None:
        return error_user_not_found()

    controller_games = GamesController(con, cur)
    game = controller_games.get_game(user_id=user_id, gamename=gamename)
    if not game:
        return error_game_not_found()
    
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