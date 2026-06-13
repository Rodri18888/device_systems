# Device systems 

## Descripcion

device systems es una app sencila de python + fastAPI donde se puede ejecutar un servidor y hacer a este peticiones GET y POST, usa un modelo de Usuario para hacer estas peticiones y esta pensado en expandirse con el pasar de las clases.

## Pasos antes de ejecutar el servidor

### Activacion entorno virtual

se debe crear un entorno virtual con python -m venv "nombre_entorno", activar el entorno segun el sistema operativo.

### Instalacion de dependencias

usando pip install -r requirements.txt dentro del entorno virtual vamos a instalar las dependencias necesarias para la app, en este caso fastapi, uvicorn y pydantic[email]

![instalacion de dependecias](img/dependencias_captura.png)

## Ejecucion del servidor

gracias a uvicorn podemos ejecutar el servidor de la app sin muchos problemas usando uvicorn app.main:app --reload, esto nos dara la direccion para entrar directamente o para utilizara en thunder client para hacer peticiones

![ejecucion del servidor](img/servidor_captura.png)

## Tabla de endpoints

esta app tiene 6 endpoints.
GET /users/ para ver todos los usuarios o filtrarlos segun el rol o si esta activo 
GET /users/{id} para filtrar el usuario segun la id
POST /users/ para enviar usuarios.
PUT /users/{id} para actualizar un usuario totalmente.
PATCH /users/{id} para actualizar un usuario parcialmente.
DELETE /users/{id} para eliminar un usuario.

## Peticiones en ThunderCLient

![inicio](img/peticion1_captura.png)

![peticion GET vacia](img/peticion2_captura.png)

![peticion POST](img/peticion3_captura.png)

![peticion GET con usuarios](img/peticion4_captura.png)

![peticion GET con id](img/peticion5_captura.png)

![peticion GET para visualizar cambios de las siguientes peticiones](img/peticion6_captura.PNG)

![peticion PUT donde se actualiza un usuario totalmente0](img/peticion7_captura.PNG)

![peticion PATCH donde solo se actualiza el nombre](img/peticion8_captura.PNG)

![peticion DELETE donde se elimina un usuario](img/peticion9_captura.PNG)

![peticion GET para comprobar que se elimino el usuario](img/peticion10_captura.PNG)


## Swagger UI

Swagger UI es una herramienta que genera una interfaz web interactiva para visualizar y probar APIs, se usara en este proyecto para hacer lo antes mencionado, podemos acceder a esta interfaz colocando /docs en una ruta

![swaggerui](img/swagger_captura.PNG)


# Evolucion del proyecto: SQLAlchemy

El proyecto ha tenido bastante evolucion, ahora se integrara sqlalchemy para la base de datos, esto requiere modificar/crear archivos, codigo, etc.

## Nueva estructura de proyecto

![nueva estructura](img/nueva_estructura.PNG)

## Base de datos generada

Ejemplo de la base de datos del proyecto con usuarios

![base de datos](img/base_de_datos.PNG)

## Prueba de endpoints

Se deben probar nuevamente los endpoints para comprobar que funcionen y esten conectados a la base de datos.

![GET](img/peticionswagger_1.PNG)

![POST](img/peticionswagger_2.PNG)

![GET CON ID](img/peticionswagger_3.PNG)

![PUT](img/peticionswagger_4.PNG)

![PATCH](img/peticionswagger_5.PNG)

![DELETE](img/peticionswagger_6.PNG)

Tambien se implementan 3 endpoints para buscar usuarios segun un valor en especifico del modelo.

![GET CON ROL](img/peticionswagger_7.PNG)

![GET CON ESTADO](img/peticionswagger_8.PNG)

![GET FECHA DE CREACION](img/peticionswagger_9.PNG)

## Validaciones

Usando los endpoints enviando datos erroneos podemos probar las validaciones

![validacion email duplicado](img/validacionswagger_1.PNG)

![validacion rol invalido](img/validacionswagger_2.PNG)

![validacion usuario inexistente](img/validacionswagger_3.PNG)

## Diferencia entre modelo sqlalchemy y schema pydantic

El modelo SQLAlchemy (ORM) define la estructura de las tablas, relaciones y tipos de datos directamente en la base de datos. El esquema Pydantic (DTO) se encarga de la validación, serialización y documentación de los datos que entran y salen de la API (solicitudes/respuestas).