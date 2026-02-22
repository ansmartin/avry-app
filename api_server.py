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

from scripts.game import PokemonFilters, GameSession


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


# USERS

@app.route("/user", methods=['GET'])
def get_user():
    connection = get_db()
    cursor = connection.cursor()

    username = request.args.get('username')
    if not username:
        return {}

    controller_games = GamesController(connection, cursor)
    controller_users = UsersController(connection, cursor, controller_games)
    user = controller_users.get_user(username)
    return user


# GAMES

@app.route("/game", methods=['GET'])
def get_game():
    connection = get_db()
    cursor = connection.cursor()

    user_id = request.args.get('user_id')
    gamename = request.args.get('gamename')
    if not user_id or not gamename:
        return {}

    controller_games = GamesController(connection, cursor)
    game = controller_games.get_game_session(user_id=user_id, gamename=gamename)
    if not game:
        return {}

    game_dict = game.to_dict()
    box = game_dict['pokemon_box']['box']
    new_box = { 
        pokemon_id : controller_games.pokemon.get_pokemon_important_data(pokemon_id,ability_id)
        for pokemon_id,ability_id in box.items()
    }
    game_dict['pokemon_box']['box'] = new_box
    return game_dict

@app.route("/do_roll", methods=['GET'])
def do_roll():
    connection = get_db()
    cursor = connection.cursor()

    game_id = request.args.get('game_id')
    pokemon_type = request.args.get('pokemon_type')
    if not game_id:
        return {}

    controller_games = GamesController(connection, cursor)
    game = controller_games.get_game_session(game_id=game_id)
    if not game:
        return {}

    pokemon = controller_games.do_roll(game, pokemon_type)
    return pokemon


# POKEMON

@app.route("/random_pokemon", methods=['GET'])
def get_pokemon():
    connection = get_db()
    cursor = connection.cursor()

    controller_games = GamesController(connection, cursor)

    game = GameSession(game_id=0, user_id=0, gamename='')
    pokemon = controller_games.pokemon.get_random_pokemon(game)
    return pokemon

@app.route("/pokemon_ids", methods=['GET'])
def get_pokemon_ids():
    connection = get_db()
    cursor = connection.cursor()

    controller_pokemon = PokemonController(connection, cursor)

    filters = PokemonFilters(
        generation=3, 
        mythical=True, 
        legendary=True, 
        sublegendary=True, 
        powerhouse=False, 
        others=False, 
        fully_evolved=True
    )

    ids = controller_pokemon.db_pokemon.get_pokemon_ids(filters)
    ids_list = list(ids)
    ids_list.sort()

    pokemon_list = [ controller_pokemon.get_pokemon_fullname(x) for x in ids_list ]
    return { 'pokemon_list' : pokemon_list}


init_db()
app.run(debug=True)