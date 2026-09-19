CREATE TABLE users(
    user_id INTEGER PRIMARY KEY,
	username TEXT NOT NULL,
	UNIQUE (username)
);

CREATE TABLE games(
    game_id INTEGER PRIMARY KEY,
	user_id INTEGER NOT NULL,
	gamemode_id INTEGER NOT NULL,
	max_rolls INTEGER NOT NULL,
	rolls INTEGER NOT NULL,
	tickets INTEGER NOT NULL,
	money INTEGER NOT NULL,
	item_points INTEGER NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users(user_id),
	FOREIGN KEY (gamemode_id) REFERENCES gamemodes(gamemode_id),
	UNIQUE (user_id, gamemode_id)
);

CREATE TABLE gamemodes(
    gamemode_id INTEGER PRIMARY KEY,
    gamename TEXT NOT NULL,
	max_rolls INTEGER NOT NULL,
	max_tickets INTEGER NOT NULL,
	max_money INTEGER NOT NULL,
	max_item_points INTEGER NOT NULL,
	generation INTEGER NOT NULL,
	include_mythical BOOLEAN NOT NULL,
	include_legendary BOOLEAN NOT NULL,
	include_sublegendary BOOLEAN NOT NULL,
	include_powerhouse BOOLEAN NOT NULL,
	fully_evolved_only BOOLEAN NOT NULL,
	random_ability BOOLEAN NOT NULL,
	UNIQUE (gamename)
);

CREATE TABLE rolls(
    game_id INTEGER NOT NULL,
	pokemon_id INTEGER NOT NULL,
	ability_id INTEGER,
	FOREIGN KEY (game_id) REFERENCES games(game_id),
	FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
	FOREIGN KEY (ability_id) REFERENCES abilities(ability_id),
	CONSTRAINT roll_pk PRIMARY KEY (game_id, pokemon_id)
);

CREATE TABLE used_cards(
    game_id INTEGER NOT NULL,
	tag TEXT NOT NULL,
	uses INTEGER NOT NULL,
	FOREIGN KEY (game_id) REFERENCES games(game_id),
	CONSTRAINT used_card_pk PRIMARY KEY (game_id, tag)
);

CREATE TABLE pokemon(
	pokemon_id INTEGER PRIMARY KEY,
	pokemon_name TEXT NOT NULL,
	form_name TEXT,
	generation INTEGER NOT NULL,
	evolves_from_pokemon_id INTEGER,
	first_type TEXT NOT NULL,
	second_type TEXT,
	first_ability INTEGER NOT NULL,
	second_ability INTEGER, 
	hidden_ability INTEGER,
	is_mythical BOOLEAN NOT NULL, 
	is_legendary BOOLEAN NOT NULL, 
	is_sublegendary BOOLEAN NOT NULL, 
	is_powerhouse BOOLEAN NOT NULL, 
	is_fully_evolved BOOLEAN NOT NULL,
	has_mega BOOLEAN NOT NULL, 
	has_gmax BOOLEAN NOT NULL, 
	sprite INTEGER
);

CREATE TABLE abilities(
    ability_id INTEGER PRIMARY KEY,
    ability_name TEXT NOT NULL,
	generation INTEGER NOT NULL
);
