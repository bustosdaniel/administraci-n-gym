import mysql.connector as mysql

con = mysql.connect(
    host="62.169.20.169",
    user="patrones",
    password="patrones123",
    database="gym"
)
if con.is_connected():
    print("Conexión exitosa")
    cursor = con.cursor()
#port 3600
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