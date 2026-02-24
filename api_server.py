from flask import Flask, request, g
import sqlite3
import os.path

import scripts.constants as const

from scripts.app_controller import AppController
from scripts.controller.users import UsersController
from scripts.controller.games import GamesController
from scripts.controller.cards import CardsController
from scripts.controller.rolls import RollsController
from scripts.controller.pokemon import PokemonController
from scripts.controller.abilities import AbilitiesController
from scripts.controller.game_cards import GameCardsController

from scripts.game import GameSession, PokemonFilters
from scripts.cards import Cards


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

def error_game_not_found():
    return { 'error':'Sesión de juego no encontrada' }


# USER

@app.route("/user/<username>", methods = ['GET','POST','DELETE'])
def user(username):
    con, cur = get_connection_and_cursor()

    controller_users = UsersController(con, cur, None)

    if request.method == 'GET':
        controller_users.games = GamesController(con, cur)
        user = controller_users.get_user(username)
        return user
    elif request.method == 'POST':
        success = controller_users.insert_user(username)
        return { 'success':success }
    elif request.method == 'DELETE':
        controller_users.games = GamesController(con, cur)
        success = controller_users.delete_user(username=username)
        return { 'success':success }


# GAME

@app.route("/user/<username>/game/<gamename>", methods=['GET','POST','DELETE'])
def game(username, gamename):
    con, cur = get_connection_and_cursor()

    controller_games = GamesController(con, cur)
    controller_users = UsersController(con, cur, controller_games)

    user_id = controller_users.db_users.get_user_id(username)

    if request.method == 'DELETE':
        success = controller_games.delete_game(user_id=user_id, gamename=gamename)
        return { 'success':success }

    if request.method == 'POST':
        dic_options = request.form
        controller_games.create_game(user_id, gamename, dic_options)

    #if request.method == 'GET' or request.method == 'POST':
    game = controller_games.get_game(user_id=user_id, gamename=gamename)
    if not game:
        return error_game_not_found()
    game_dict = controller_games.get_game_simplified_dict(game)
    return game_dict


# ROLL

@app.route("/user/<username>/game/<gamename>/roll", methods=['GET'])
def do_roll(username, gamename):
    con, cur = get_connection_and_cursor()

    controller_games = GamesController(con, cur)
    controller_users = UsersController(con, cur, controller_games)

    game = controller_users.get_game(username, gamename)
    if not game:
        return error_game_not_found()

    pokemon_type = request.args.get('type')
    pokemon = controller_games.do_roll(game, pokemon_type)
    return pokemon


# CARD

@app.route("/user/<username>/game/<gamename>/card/<card_tag>", methods=['GET','POST'])
def use_card(username, gamename, card_tag):
    con, cur = get_connection_and_cursor()

    controller_games = GamesController(con, cur)
    controller_users = UsersController(con, cur, controller_games)
    controller_gamecards = GameCardsController(controller_games)

    game = controller_users.get_game(username, gamename)
    if not game:
        return error_game_not_found()

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
    return pokemon


init_db()

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)