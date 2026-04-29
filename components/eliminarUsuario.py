from Servicios.eliminar_service import EliminarService


class EliminarUsuario:
    """Clase delegadora que utiliza EliminarService"""
    
    def __init__(self, usuarios):
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
