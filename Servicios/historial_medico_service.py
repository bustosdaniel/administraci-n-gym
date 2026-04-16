from components.historial_medico import HistorialMedico

class HistorialMedicoService:
    """Servicio para gestionar historiales médicos de usuarios"""
    
    def __init__(self, usuarios_service):
        self.historiales = []
        self.usuarios_service = usuarios_service
        self._ultimo_id_historial = 0

    def crear_historial_usuario(self, id_cliente, peso, estatura, tipo_sangre, lesiones):
        """Crea un nuevo historial médico para un usuario"""
        self._ultimo_id_historial += 1
        id_historial_med = self._ultimo_id_historial
        imc = "pendiente"
        
        historial = HistorialMedico(
            id_historial_med=id_historial_med,
            id_cliente=id_cliente,
            peso=peso,
            estatura=estatura,
            tipo_sangre=tipo_sangre,
            lesiones=lesiones,
            fecha_ingreso="pendiente",
            imc=imc
        )
        
        self.historiales.append(historial)
        print("Registrado correctamente.")

    def actualizar_fecha_ingreso(self, id_cliente, fecha_ingreso):
        """Actualiza la fecha de ingreso en todos los historiales del cliente"""
        id_cliente = str(id_cliente).strip()
        for h in self.historiales:
            if str(h.id_cliente).strip() == id_cliente:
                h.actualizar_fecha_ingreso(fecha_ingreso)

    def id_seleccionado_cliente(self, id_cliente):
        """Retorna el historial más reciente de un cliente"""
        id_cliente = str(id_cliente).strip()
        for h in reversed(self.historiales):
            if str(h.id_cliente).strip() == id_cliente:
                return h
        return None

    def mostrar_historiales(self):
        """Muestra todos los historiales en formato tabla"""
        if not self.historiales:
            print("\nNo hay historiales médicos registrados.")
            return
        
        from Servicios.usuarios_service import tabla
        
        columnas = [
            ("ID_HIST", 6),
            ("USUARIO", 14),
            ("INGRESO", 10),
            ("PESO", 6),
            ("ESTATURA", 8),
            ("SANGRE", 8),
            ("LESIONES", 12),
            ("IMC", 6),
        ]
        filas = []
        for h in self.historiales:
            cliente = self.usuarios_service.buscar_id(h.id_cliente)
            nombre_usuario = cliente.nombre if cliente else "Sin nombre"
            filas.append(
                (
                    h.id_historial_med,
                    nombre_usuario,
                    h.fecha_ingreso,
                    h.peso,
                    h.estatura,
                    h.tipo_sangre,
                    h.lesiones,
                    h.imc,
                )
            )
        tabla("HISTORIALES MEDICOS", columnas, filas)
