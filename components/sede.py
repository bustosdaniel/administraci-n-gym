from Servicios.sede_service import SedeService


class Sede:
    """Clase delegadora que utiliza SedeService"""
    
    def __init__(self):
        self.service = SedeService()
    
    def elegir_sede(self):
        """Delega a SedeService"""
        return self.service.elegir_sede()
    
    def id_seleccionado(self, id_sede):
        """Delega a SedeService"""
        return self.service.id_seleccionado(id_sede)
    
    def mostrar_sedes(self, tabla_func):
        """Muestra todas las sedes disponibles"""
        if not self.service.sedes:
            print("\nNo hay sedes registradas.")
            return
        columnas = [
            ("ID_SEDE", 7),
            ("NOMBRE", 20),
            ("DIRECCION", 20),
            ("TELEFONO", 10),
            ("HORARIO", 10),
        ]
        filas = [
            (s["id_sede"], s["nombre_sede"], s["direccion"], s["telefono"], s["horario"])
            for s in self.service.sedes
        ]
        tabla_func("SEDES", columnas, filas)
