# App Liga Rushdown
Aplicación para gestión de torneos de videojuegos de Pokémon.

Desarrollo de la parte del back-end con Python, gestión de la base de datos con SQLite y creación de una API REST.


## Preparación

1. Crear entorno virtual (recomendado)

	```
	python -m venv venv
	```

2. Activar entorno virtual (recomendado)

	```
	.\venv\Scripts\activate
	```

3. Instalar dependencias:

   ```
   python -m pip install -r requirements.txt
   ```

## Iniciar aplicación

1. Activar entorno virtual (recomendado) si no lo has activado ya antes 

	```
	.\venv\Scripts\activate
	```

2. Iniciar aplicación (inicia API Rest en localhost)
   
   ```
   python -m api_server
   ```

## Lista de recursos disponibles de la API

### - User (endpoint)
```
/user/{username}
```

Métodos: 
- 'GET': Obtener usuario.
- 'POST': Añadir usuario.
- 'DELETE': Eliminar usuario.

### - Game (endpoint)
```
/user/{username}/game/{gamename}
```

Métodos: 
- 'GET': Obtener partida.
- 'POST': Añadir partida.
- 'DELETE': Eliminar partida.

### - Roll (endpoint)
```
/user/{username}/game/{gamename}/roll
```

(Opcional) Añadir argumento {type} para gastar un ticket de tipo y obtener un Pokémon del tipo especificado.
```
/user/{username}/game/{gamename}/roll?{type}
```

Métodos: 
- 'GET': Realizar tirada para obtener un Pokémon aleatorio.

### - Card (endpoint)
```
/user/{username}/game/{gamename}/card/{card_tag}
```

Cartas de ventaja disponibles:

- tag = 'mega'

	nombre = ESPABILA, MEGAEVOLUCIONA

	descripción = REALIZA UNA TIRADA DONDE SÓLO PUEDEN APARECER POKÉMON CON MEGA-EVOLUCIÓN.

	precio = 6000 monedas

	Métodos: 
	- 'GET': Obtiene un Pokémon con mega-evolución.

- tag = 'fusion'

	nombre = FUSIÓN ALEATORIA

	descripción = ELIGE 2 POKÉMON, ELIMINALOS PARA REALIZAR UNA TIRADA ALEATORIA.

	precio = 400 monedas

	Métodos: 
	- 'POST': Envía los ids de los Pokémon a fusionar dentro del Body de la petición. Obtiene un nuevo Pokémon aleatorio.

			pokemon_id1 : {id}
			pokemon_id2 : {id}

- tag = 'intercambio'

	name = INTERCAMBIO PRODIGIOSO

	descripción = ELIGE 1 POKÉMON DE TUS 20, INTERCAMBIALO POR OTRO AL AZAR.

	precio = 600 monedas

	Métodos: 
	- 'POST': Envía el id del Pokémon a intercambiar dentro del Body de la petición. Obtiene un nuevo Pokémon aleatorio.

			pokemon_id : {id}

- tag = 'preevo'

	nombre = LA PRE-EVO ES MEJOR

	descripción = PUEDES CAMBIAR UNO DE TUS POKÉMON POR SU PRE-EVOLUCIÓN.

	precio = 1500 monedas

	Métodos: 
	- 'POST': Envía el id del Pokémon a cambiar dentro del Body de la petición. Obtiene el Pokémon pre-evolucionado.

			pokemon_id : {id}

- tag = 'comienzo'

	nombre = NUEVO COMIENZO

	descripción = ANTES DE GASTAR TU TIRADA Nº18, REINICIA TODAS TUS TIRADAS.

	precio = 3200 monedas

	Limitada a 1 uso.

- tag = '2_powerhouse'

	nombre = 2 ES MEJOR QUE 1

	descripción = PODRÁS UTILIZAR 2 POKÉMON DE LA CATEGORÍA \"PESOS PESADOS\" EN EL EQUIPO EN LUGAR DE 1.

	precio = 7000 monedas

	Limitada a 1 uso.

- tag = 'ticket_tipo'

	nombre = TIQUET ELEMENTAL

	descripción = OBTIENES UN TICKET ADICIONAL PARA FORZAR EL TIPO DEL POKÉMON.

	precio = 400 monedas

- tag = 'adicional_1'

	nombre = TIRADA ADICIONAL 1

	descripción = OBTIENES UNA TIRADA ADICIONAL.

	precio = 800 monedas

	Limitada a 1 uso.

- tag = 'adicional_2'

	nombre = TIRADA ADICIONAL 2

	descripción = OBTIENES DOS TIRADAS ADICIONALES.

	precio = 1400 monedas

	Limitada a 1 uso.

- tag = 'adicional_3'

	nombre = TIRADA ADICIONAL 3

	descripción = OBTIENES TRES TIRADAS ADICIONALES.

	precio = 2000 monedas

	Limitada a 1 uso.

- tag = 'selectiva'

	nombre = TIRADA SELECTIVA

	descripción = HAZ UNA TIRADA DE 6 POKÉMON, PUEDES DESECHAR HASTA 5 SIN GASTAR TIRADAS.

	precio = 3000 monedas

	Limitada a 1 uso.

	Métodos: 
	- 'GET': Obtienes la lista de Pokémon disponibles para elegir.
	- 'POST': Envía los ids de los Pokémon seleccionados dentro del Body de la petición (como claves).

			{id1}
			{id2}
			...
