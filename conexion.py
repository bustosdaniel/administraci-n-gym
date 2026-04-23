import mysql.connector as mysql
from mysql.connector import Error 

# CONFIGURACIÓN PARA XAMPP (credenciales por defecto)
DB_CONFIG = {
    'host': '62.169.20.169',
    'user': 'patrones',
    'password': 'patrones123', 
    'database': 'gym'
}
if con.is_connected():
    print("✓ Conexión a MySQL exitosa")

def create_connection(host_name, user_name, user_password, db_name):
    """Crea una conexión a la base de datos MySQL"""
    connection = None
    try:
        connection = mysql.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("✓ Conexión a MySQL exitosa")
    except Error as e:
        print(f"✗ Error de conexión: {e}")
    return connection 

def create_database_if_not_exists(host_name, user_name, user_password, db_name):
    """Crea la base de datos si no existe"""
    try:
        connection = mysql.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        # Crear tabla usuarios
        create_table_query = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100),
            apellido VARCHAR(100),
            fecha_nacimiento DATE,
            correo_electronico VARCHAR(100),
            cedula VARCHAR(20),
            direccion VARCHAR(255),
            numero_celular VARCHAR(20)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("✓ Base de datos y tablas creadas")
        cursor.close()
        connection.close()
    except Error as e:
        print(f"✗ Error al crear base de datos: {e}")

# Crear base de datos y tablas al importar el módulo
try:
    create_database_if_not_exists(
        DB_CONFIG['host'],
        DB_CONFIG['user'],
        DB_CONFIG['password'],
        DB_CONFIG['database']
    )
except Exception as e:
    print(f"✗ Error: {e}")

# Conectar a la base de datos
connection = create_connection(
    DB_CONFIG['host'],
    DB_CONFIG['user'],
    DB_CONFIG['password'],
    DB_CONFIG['database']
)

def crear_usuario(connection, usuario):
    """Inserta un nuevo usuario en la base de datos"""
    cursor = connection.cursor()
    query = """
    INSERT INTO usuarios (id_usuario, nombre, apellido, fecha_nacimiento, correo_electronico, cedula, direccion, numero_celular)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        usuario["id_usuario"],
        usuario["nombre"],
        usuario["apellido"],
        usuario["fecha_nacimiento"],
        usuario["correo_electronico"],
        usuario["cedula"],
        usuario["direccion"],
        usuario["numero_celular"]
    )
    try:
        cursor.execute(query, values)
        connection.commit()
        print(f"✓ Usuario '{usuario['nombre']}' registrado correctamente")
    except Error as e:
        print(f"✗ Error al registrar usuario: {e}")
        connection.rollback()