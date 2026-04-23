from datetime import date


class Eliminar:
    """Modelo de un registro de eliminación de usuario"""
    
    def __init__(self, id_usuario, nombre, apellido, fecha_baja=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_baja = fecha_baja or str(date.today())

    def __repr__(self):
        return f"Eliminar(id={self.id_usuario}, nombre={self.nombre} {self.apellido})"

    def get_datos(self):
        """Retorna los datos del registro de eliminación como diccionario"""
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_baja": self.fecha_baja
        }
