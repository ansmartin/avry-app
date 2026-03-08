# App Liga Rushdown
Aplicación para gestión de torneos de videojuegos de Pokémon.

Desarrollo de la parte del back-end con Python, gestión de la base de datos con SQLite y creación de una API REST.


## Iniciar aplicación

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

4. Inicia servidor API Rest en localhost puerto 8080:
   
   ```
   python -m api_server
   ```

## Lista de recursos disponibles de la API

### - User 
Endpoint:
`
/user/{username}
`

Métodos: 
- 'GET': Obtener usuario.
- 'POST': Crear usuario.
- 'DELETE': Eliminar usuario.

Ejemplo de crear nuevo usuario:

<img width="709" height="347" alt="Captura_user" src="https://github.com/user-attachments/assets/c8f70840-eb16-463a-bb7d-c7dc922ea517" />


### - Game 
Endpoint:
`
/user/{username}/game/{gamename}
`

Métodos: 
- 'GET': Obtener partida.
- 'POST': Crear partida.
- 'DELETE': Eliminar partida.

Ejemplo de crear nueva partida con las opciones por defecto:

<img width="711" height="869" alt="Captura_game" src="https://github.com/user-attachments/assets/17a5f7de-8569-4f23-a394-ad72cac4a626" />


### - Roll 
Endpoint:
`
/user/{username}/game/{gamename}/roll
`

(Opcional) Añadir argumento {type} para gastar un ticket de tipo y obtener un Pokémon del tipo especificado.

Endpoint:
`
/user/{username}/game/{gamename}/roll?{type}
`

Métodos: 
- 'GET': Realizar tirada para obtener un Pokémon aleatorio.

Ejemplo:

<img width="714" height="684" alt="Captura_roll" src="https://github.com/user-attachments/assets/550b0531-9490-415f-ae2c-6411fec868e4" />


### - Card 
Endpoint:
`
/user/{username}/game/{gamename}/card/{card_tag}
`

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
