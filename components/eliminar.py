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


class EliminarUsuario:
    """Clase delegadora que utiliza EliminarService"""
    
    def __init__(self, usuarios):
        from Servicios.eliminar_service import EliminarService
        self.service = EliminarService(usuarios.service)
        self.usuarios = usuarios

    @property
    def eliminaciones(self):
        """Propiedad que retorna las eliminaciones del service"""
        return self.service.eliminaciones

    def enlazar_service(self, usuarios_service):
        """Enlaza el servicio de usuarios"""
        self.service.usuarios_service = usuarios_service

    def eliminar_usuario(self):
        """Delega a EliminarService"""
        return self.service.eliminar_usuario()

    def mostrar_eliminaciones(self):
        """Delega a EliminarService"""
        return self.service.mostrar_eliminaciones()
