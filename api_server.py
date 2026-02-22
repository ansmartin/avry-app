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

from scripts.game import PokemonFilters


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


@app.route("/pokemon", methods=['GET'])
def get_pokemon():
    connection = get_db()
    cursor = connection.cursor()

    controller_games = GamesController(connection, cursor)

    game_id = 1
    game = controller_games.get_game_session(game_id=game_id)
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