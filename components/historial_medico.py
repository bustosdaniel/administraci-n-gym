import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class HistorialMedico:
    """Modelo de un historial médico de un usuario"""
    
    def __init__(self, id_historial_med, id_cliente, peso, estatura, 
                 tipo_sangre, lesiones, fecha_ingreso="pendiente", imc="pendiente"):
        self.id_historial_med = id_historial_med
        self.id_cliente = str(id_cliente).strip()
        self.fecha_ingreso = fecha_ingreso
        self.peso = peso
        self.estatura = estatura
        self.tipo_sangre = tipo_sangre
        self.lesiones = lesiones
        self.imc = imc

    def __repr__(self):
        return f"HistorialMedico(id={self.id_historial_med}, cliente={self.id_cliente})"

    def get_datos(self):
        """Retorna los datos del historial como diccionario"""
        return {
            "id_historial_med": self.id_historial_med,
            "id_cliente": self.id_cliente,
            "fecha_ingreso": self.fecha_ingreso,
            "peso": self.peso,
            "estatura": self.estatura,
            "tipo_sangre": self.tipo_sangre,
            "lesiones": self.lesiones,
            "imc": self.imc
        }

    def actualizar_fecha_ingreso(self, fecha_ingreso):
        """Actualiza la fecha de ingreso del historial"""
        self.fecha_ingreso = str(fecha_ingreso).strip()


class HistorialMedicoManager:
    """Clase delegadora que utiliza HistorialMedicoService"""
    
    def __init__(self, usuarios):
        from Servicios.historial_medico_service import HistorialMedicoService
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
