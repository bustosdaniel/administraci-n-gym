import mysql.connector as mysql
from mysql.connector import Error 

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection 

connection = create_connection("localhost", "root", "root", "gym_db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM usuarios")
result = cursor.fetchall()
for row in result:
    print(row)    

def crear_usuario(connection, usuario):
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
    cursor.execute(query, values)
    connection.commit()