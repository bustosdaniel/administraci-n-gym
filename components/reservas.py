from Servicios.reservas_service import ReservasService


class Reservas:
    """Clase delegadora que utiliza ReservasService"""
    
    def __init__(self, usuarios, tabla_clases):
        self.service = ReservasService()
        self.usuarios = usuarios
        self.tabla_clases = tabla_clases
    
    def crear_reserva(self):
        """Delega a ReservasService"""
        return self.service.crear_reserva(self.usuarios, self.tabla_clases)
    
    def id_seleccionado(self, id_reserva):
        """Delega a ReservasService"""
        return self.service.id_seleccionado(id_reserva)
    
    def elegir_reserva(self):
        """Delega a ReservasService"""
        return self.service.elegir_reserva(self.usuarios)
    
    def mostrar_reservas(self, tabla_func):
        """Muestra todas las reservas registradas"""
        if not self.service.reservas:
            print("\nNo hay reservas registradas.")
            return
        columnas = [
            ("ID_RES", 6),
            ("CLIENTE", 16),
            ("ID_CLASE", 7),
            ("FECHA_RESERVA", 12),
            ("ESTADO", 12),
        ]
        filas = []
        for r in self.service.reservas:
            cliente = self.usuarios.buscar_id(r["id_cliente"])
            nombre = cliente.nombre if cliente else "Sin nombre"
            filas.append((r["id_reserva"], nombre, r["id_clase"], r["fecha_reserva"], r["estado_reserva"]))
        tabla_func("RESERVAS", columnas, filas)
