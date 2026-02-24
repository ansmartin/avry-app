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
        db = get_db()
        # schema
        with app.open_resource(const.SCHEMA_FILE, mode='r') as f:
            db.cursor().executescript(f.read())
        # values
        with app.open_resource(const.POKEMON_VALUES_FILE, mode='r') as f:
            db.cursor().executescript(f.read())
        with app.open_resource(const.ABILITIES_VALUES_FILE, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def error_game_not_found():
    return { 'error':'Sesión de juego no encontrada' }


# USER

@app.route("/user/<username>", methods = ['GET','POST','DELETE'])
def user(username):
    connection = get_db()
    cursor = connection.cursor()

    controller_users = UsersController(connection, cursor, None)

    if request.method == 'GET':
        controller_users.games = GamesController(connection, cursor)
        user = controller_users.get_user(username)
        return user
    elif request.method == 'POST':
        success = controller_users.insert_user(username)
        return { 'success':success }
    elif request.method == 'DELETE':
        controller_users.games = GamesController(connection, cursor)
        success = controller_users.delete_user(username=username)
        return { 'success':success }


# GAME

@app.route("/user/<username>/game/<gamename>", methods=['GET','DELETE'])
def game(username, gamename):
    connection = get_db()
    cursor = connection.cursor()

    controller_games = GamesController(connection, cursor)
    controller_users = UsersController(connection, cursor, controller_games)

    game = controller_users.get_game(username, gamename)
    if not game:
        return error_game_not_found()

    if request.method == 'GET':
        game_dict = controller_games.get_game_simplified_dict(game)
        return game_dict
    elif request.method == 'DELETE':
        success = controller_games.delete_game(game_id=game.game_id)
        return { 'success':success }


# ROLL

@app.route("/user/<username>/game/<gamename>/roll", methods=['GET'])
def do_roll(username, gamename):
    connection = get_db()
    cursor = connection.cursor()

    controller_games = GamesController(connection, cursor)
    controller_users = UsersController(connection, cursor, controller_games)

    game = controller_users.get_game(username, gamename)
    if not game:
        return error_game_not_found()

    pokemon_type = request.args.get('type')
    pokemon = controller_games.do_roll(game, pokemon_type)
    return pokemon


# CARD

@app.route("/user/<username>/game/<gamename>/card/<card_tag>", methods=['GET'])
def use_card(username, gamename, card_tag):
    connection = get_db()
    cursor = connection.cursor()

    controller_games = GamesController(connection, cursor)
    controller_users = UsersController(connection, cursor, controller_games)
    controller_gamecards = GameCardsController(controller_games)

    game = controller_users.get_game(username, gamename)
    if not game:
        return error_game_not_found()

    if card_tag == Cards.TAG_MEGA:
        pokemon = controller_gamecards.use_card_mega(game)
        return pokemon
    elif card_tag == Cards.TAG_FUSION:
        pokemon_id1 = int(request.args.get('pokemon_id1'))
        pokemon_id2 = int(request.args.get('pokemon_id2'))
        pokemon = controller_gamecards.use_card_fusion(game,pokemon_id1,pokemon_id2)
        return pokemon
    elif card_tag == Cards.TAG_INTERCAMBIO:
        pokemon_id = int(request.args.get('pokemon_id'))
        pokemon = controller_gamecards.use_card_intercambio(game,pokemon_id)
        return pokemon
    elif card_tag == Cards.TAG_PREEVO:
        pokemon_id = int(request.args.get('pokemon_id'))
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
        pokemons = request.args.get('pokemons')
        if not pokemons:
            # primera parte
            pokemon_list = controller_gamecards.use_card_selectiva(game)
            return { 'pokemon_list':pokemon_list }
        else:
            # segunda parte
            controller_gamecards.use_card_selectiva_final(game, pokemons)

    return {}


# POKEMON

@app.route("/random_pokemon", methods=['GET'])
def random_pokemon():
    connection = get_db()
    cursor = connection.cursor()

    controller_games = GamesController(connection, cursor)

    game = GameSession(game_id=0, user_id=0, gamename='')
    pokemon = controller_games.pokemon.get_random_pokemon(game)
    return pokemon


init_db()
app.run(debug=True)