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


# Evolucion del proyecto: Usuarios, Dispositivos y Prestamos

El proyecto sigue creciendo, ahora se agregan los modelos de Dispositivo y Prestamo, junto con sus endpoints y relaciones. Para manejar los cambios en la base de datos se integra Alembic como herramienta de migraciones.

## Inicializacion de Alembic

Alembic se inicializa con alembic init para generar la carpeta de migraciones y el archivo alembic.ini con la configuracion base.


## Creacion de migracion

Con alembic revision --autogenerate Alembic detecta los cambios en los modelos y genera automaticamente el script de migracion correspondiente.

![alembic revision](img/alembic_autogenerate_captura.PNG)

## Aplicacion de migracion

Con alembic upgrade head se aplican los cambios pendientes a la base de datos.

![alembic upgrade head](img/alembic_upgrade_head_captura.PNG)

## Estructura de tablas generadas

Las tres tablas quedan creadas con sus columnas y relaciones correctamente reflejadas en la base de datos.

![estructura de tablas](img/tablas_alembic.PNG)

## Swagger UI

Se puede visualizar la totalidad de los endpoints disponibles directamente desde la interfaz de Swagger.


## Evidencia de creacion de registros

Se crea un dispositivo y un prestamo para verificar que los modelos funcionan correctamente y se relacionan entre si.

![creacion de dispositivo](img/peticiondevice.PNG)

![creacion de prestamo](img/peticionloan.PNG)

## Consultas con joins

Los endpoints de prestamos devuelven informacion combinada de las tablas relacionadas usando joins, evitando tener que hacer multiples peticiones.

![consulta con join](img/peticionloan2.PNG)


## Devolucion de dispositivo

Al registrar la devolucion de un dispositivo, el prestamo se actualiza y el dispositivo vuelve a estar disponible.

![devolucion](img/peticionloan3.PNG)

## Reflexion

Las migraciones con Alembic permiten evolucionar el esquema de la base de datos de forma controlada sin perder datos ni tener que recrear tablas manualmente. Las relaciones entre modelos y las consultas con joins son fundamentales para construir APIs que devuelvan informacion util y coherente sin multiplicar innecesariamente las peticiones al servidor.


# Evolucion del proyecto: Autenticacion y Seguridad

En esta fase se agrega autenticacion con JWT, control de acceso por roles, middleware de cabeceras, rate limiting con slowapi y configuracion de CORS.

## Estructura del proyecto

La estructura del proyecto se reorganiza para separar las responsabilidades de autenticacion del resto de los modulos.

![estructura del proyecto](img/auth1.png)

## Migracion Alembic aplicada

Se genera y aplica una nueva migracion para agregar los campos necesarios al modelo de usuario para soportar autenticacion.


## Registro de usuario

El endpoint POST /auth/register permite crear un usuario nuevo. La contrasena se almacena hasheada, nunca en texto plano.

![registro de usuario](img/auth2.png)

## Login y token generado

El endpoint POST /auth/login valida las credenciales y devuelve un token JWT que se debe usar en las siguientes peticiones.

![login y token](img/auth3.png)

## Endpoint /auth/me

Con el token valido en la cabecera Authorization, el endpoint GET /auth/me devuelve la informacion del usuario autenticado.

![auth me](img/auth4.png)

## Acceso sin token

Intentar acceder a un endpoint protegido sin token devuelve un error 401 Unauthorized.

![acceso sin token](img/auth5.png)

## Acceso con rol no permitido

Si el usuario autenticado no tiene el rol requerido para un endpoint, la API devuelve un error 403 Forbidden.

![rol no permitido](img/auth6.png)

## Swagger con OAuth2

Swagger UI muestra el boton de autorizacion para ingresar el token JWT y probar los endpoints protegidos directamente desde la interfaz.

![swagger oauth2](img/auth7.png)

## Cabeceras del middleware

El middleware agrega cabeceras personalizadas a cada respuesta. Esto se puede verificar en la seccion de headers de cualquier peticion.


## Rate limiting

slowapi limita la cantidad de peticiones que un cliente puede hacer en un periodo de tiempo. Al superar el limite la API devuelve un error 429 Too Many Requests.


## CORS configurado

CORS se configura en FastAPI usando CORSMiddleware, definiendo los origenes permitidos, los metodos HTTP aceptados y si se permiten credenciales. En este proyecto se configuro para aceptar peticiones desde cualquier origen durante el desarrollo, lo cual deberia restringirse a dominios especificos en un entorno de produccion.

## Reflexion final

La seguridad en una API REST no es opcional ni se agrega al final. JWT permite autenticar usuarios sin guardar estado en el servidor. El control de roles evita que usuarios accedan a recursos para los que no tienen permiso. El middleware y el rate limiting protegen la API de abusos y exponen informacion util por cabeceras. CORS controla que origenes pueden consumir la API desde el navegador. Cada una de estas capas tiene una responsabilidad distinta y todas son necesarias para que una API sea minimamente robusta en un entorno real.

