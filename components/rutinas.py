from Servicios.rutinas_service import RutinasService


class Rutinas:
    """Clase delegadora que utiliza RutinasService"""
    
    def __init__(self, usuarios, tabla_cliente, tabla_entrenadores):
        self.service = RutinasService()
        self.usuarios = usuarios
        self.tabla_cliente = tabla_cliente
        self.tabla_entrenadores = tabla_entrenadores
    
    def crear_rutina(self):
        """Delega a RutinasService"""
        return self.service.crear_rutina(self.usuarios, self.tabla_cliente, self.tabla_entrenadores)
    
    def mostrar_rutinas(self, tabla_func):
        """Delega a RutinasService"""
        return self.service.mostrar_rutinas(self.usuarios, self.tabla_entrenadores, tabla_func)
