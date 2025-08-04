# Kiko!
Kiko es un bot de moderacion orientado al minimalismo y la eficiencia. Utill para servidores de tema neutral o profesional.
## Como hostearlo?
### Paso 0: MongoDB
Kiko tiene un sistema de base de datos que usa MongoDB, asi que se necesita crear:
1. Crea una nueva base de datos llamada `kiko`.
2. Crea una nueva coleccion llamada `warns`.
3. Copia el archivo `.env_example` y renombralo como `.env` y abrelo en un editor de texto.
4. Elimina los valores dentro de `MONGO_URI` y pega el Token siguiendo las instrucciones.
### Paso 1: Preparando el Bot
1. Crea un nueva aplicacion usando el portal de Desarrolladores de Discord.
2. Abre el archivo `.env` y ahora pega el Token de tu Bot dentro de `CORE_TOKEN`.
3. Invita al Bot a tu servidor.
### Paso 2: Prende tu Bot
1. Puedes correr tu Bot de manera local, o hostearlo en algun servicio. Mi recomendacion es Railway
2. Usa el archivo `shot.py` para ejecutar todas las funciones del Bot.
### Paso 3: Local
Si estas usando editores de texto como Visual Studio Code, no esta mal pero te sugeriria que usaras algo mas sofisticado, como PyCharm, Jupyter etc.

Este codigo fue programado en Python, por lo que estas IDEs son justamante para Python. MI recomendacion personal es que uses PyCharm, corriendo el archivo `shot.py` y reiniciandolo cada que actualices algun archivo o comando.

### Quieres modificar el Bot?
Haz lo que quieras. Pero no olvides dar creditos al autor de este codigo.

Osko.
