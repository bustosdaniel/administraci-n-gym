from Servicios.asistencia_service import AsistenciaService


class Asistencia:
    """Clase delegadora que utiliza AsistenciaService"""
    
    def __init__(self, tabla_reservas):
        self.service = AsistenciaService()
        self.tabla_reservas = tabla_reservas
    
    def crear_asistencia(self):
        """Delega a AsistenciaService"""
        return self.service.crear_asistencia(self.tabla_reservas)
    
    def mostrar_asistencias(self, tabla_func):
        """Muestra todas las asistencias registradas"""
        if not self.service.asistencias:
            print("\nNo hay asistencias registradas.")
            return
        columnas = [
            ("ID_ASIS", 7),
            ("ID_RES", 6),
            ("FECHA", 10),
            ("ESTADO", 10),
            ("HORA_ENTRADA", 11),
            ("HORA_SALIDA", 10),
        ]
        filas = [
            (
                a["id_asistencia"],
                a["id_reserva"],
                a["fecha_asistencia"],
                a["estado_asistencia"],
                a["hora_entrada"],
                a["horas_salida"],
            )
            for a in self.service.asistencias
        ]
        tabla_func("ASISTENCIAS", columnas, filas)
