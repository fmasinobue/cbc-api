import os 
# pip install mysql-connector-python
import mysql.connector  # Importa el conector MySQL para conectar con la base de datos
from flask import g  # Importa g de Flask para almacenar datos durante la petición
# pip install python-dotenv
from dotenv import load_dotenv  

d = os.path.dirname(__file__)
os.chdir(d)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la base de datos usando variables de entorno
# DATABASE_CONFIG = {
#     'user': os.getenv('DB_USERNAME'),  
#     'password': os.getenv('DB_PASSWORD'),  
#     'host': os.getenv('DB_HOST'),  
#     'database': os.getenv('DB_NAME'),  
#     'port': os.getenv('DB_PORT', 3306)  # Puerto del servidor de la base de datos, por defecto es 3306 si no se especifica
# }

DATABASE_CONFIG = {
    'user':"sql5717349",  
    'password': "MdLkB6FKQs",  
    'host': "sql5.freemysqlhosting.net",  
    'database': "sql5717349",  
    'port': 3306  # Puerto del servidor de la base de datos, por defecto es 3306 si no se especifica
}


# Función para obtener la conexión de la base de datos
def get_db():
    # Si no hay una conexión a la base de datos en g, la creamos
    # g, que es un objeto de Flask que se usa para almacenar datos durante la vida útil de una solicitud.
    if 'db' not in g:
        print("···· Abriendo conexion a DB ····",DATABASE_CONFIG['database']," ---- ",DATABASE_CONFIG['user'])
        g.db = mysql.connector.connect(**DATABASE_CONFIG)
    # Retorna la conexión a la base de datos
    return g.db

# Función para cerrar la conexión a la base de datos
def close_db(e=None):
    # Intenta obtener la conexión de la base de datos desde g
    db = g.pop('db', None)
    # Si hay una conexión, la cerramos
    if db is not None:
        print("···· Cerrando conexion a DB ····")
        db.close()
# Función para inicializar la base de datos
def init_db():
    db = get_db()
    cursor = db.cursor()

    # Crear tablas si no existen con todas las claves e índices incluidos
    sql_commands = [
    """CREATE TABLE IF NOT EXISTS `socios` (
        `id_socio` INT NOT NULL AUTO_INCREMENT,
        `nombre` VARCHAR(100) NOT NULL,
        `apellido` VARCHAR(100) NOT NULL,
        `federado` BOOLEAN NOT NULL DEFAULT FALSE,
        `edad` INT,
        PRIMARY KEY (`id_socio`)
    ) ;""",
     """CREATE TABLE IF NOT EXISTS `deportes` (
        `id_deporte` INT NOT NULL AUTO_INCREMENT,
        `nombre` VARCHAR(100) NOT NULL,
        PRIMARY KEY (`id_deporte`),
        UNIQUE KEY `nombre_UNIQUE` (`nombre`)
    ) ;""",
    
    """CREATE TABLE IF NOT EXISTS `socios_deportes` (
        `id_socio_deporte` INT NOT NULL AUTO_INCREMENT,
        `id_socio` INT NOT NULL,
        `id_deporte` INT NOT NULL,
        PRIMARY KEY (`id_socio_deporte`),
        KEY `FK_socio_idx` (`id_socio`),
        KEY `FK_deporte_idx` (`id_deporte`),
        CONSTRAINT `FK_socio` FOREIGN KEY (`id_socio`) REFERENCES `socios` (`id_socio`) ON DELETE CASCADE,
        CONSTRAINT `FK_deporte` FOREIGN KEY (`id_deporte`) REFERENCES `deportes` (`id_deporte`) ON DELETE CASCADE
    ) ;"""
    
   
]

    for command in sql_commands:
        cursor.execute(command)

    db.commit()

    # Inserciones de deportes si no existen
    cursor.execute("""
        INSERT INTO deportes (nombre) VALUES
            ('Futbol'), ('Remo'), ('Canotaje'), ('SUP'), ('Basquet'),
            ('Voley')
        ON DUPLICATE KEY UPDATE nombre=nombre;
    """)

    db.commit()
    cursor.close()

# Función para inicializar la aplicación con el cierre automático de la conexión a la base de datos
def init_app(app):
    # Registrar la función close_db para que se llame automáticamente
    # cuando el contexto de la aplicación se destruye
    app.teardown_appcontext(close_db)
