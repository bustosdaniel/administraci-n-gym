import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Servicios.historial_medico_service import HistorialMedicoService


class HistorialMedicoManager:
    """Clase delegadora que utiliza HistorialMedicoService"""
    
    def __init__(self, usuarios):
        self.service = HistorialMedicoService(usuarios.service)
        self.usuarios = usuarios

    @property
    def historiales(self):
        """Propiedad que retorna los historiales del service"""
        return self.service.historiales

    def crear_historial_usuario(self, id_cliente, peso, estatura, tipo_sangre, lesiones):
        """Delega a HistorialMedicoService"""
        return self.service.crear_historial_usuario(id_cliente, peso, estatura, tipo_sangre, lesiones)

    def actualizar_fecha_ingreso(self, id_cliente, fecha_ingreso):
        """Delega a HistorialMedicoService"""
        return self.service.actualizar_fecha_ingreso(id_cliente, fecha_ingreso)

    def id_seleccionado_cliente(self, id_cliente):
        """Delega a HistorialMedicoService"""
        return self.service.id_seleccionado_cliente(id_cliente)

    def mostrar_historiales(self):
        """Delega a HistorialMedicoService"""
        return self.service.mostrar_historiales()
