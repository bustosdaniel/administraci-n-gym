class ClienteService:
    """Servicio para gestionar estados de clientes"""
    
    def __init__(self, usuarios_service=None):
        self.registros_estado = []
        self.usuarios_service = usuarios_service
    
    def crear_estado_usuario(self, id_usuario, objetivo_entreno):
        """Crea un nuevo estado de cliente"""
        estado_membresia = "activa"
        objetivo = objetivo_entreno if objetivo_entreno else "acondicionamiento general"
        registro = {
            "id_usuario": str(id_usuario).strip(),
            "fecha_ingreso": "pendiente",
            "estado_membresia": estado_membresia,
            "objetivo": objetivo,
        }
        self.registros_estado.append(registro)
        print("Registrado correctamente.")
        return registro
    
    def actualizar_fecha_ingreso(self, id_usuario, fecha_ingreso):
        """Actualiza la fecha de ingreso de un cliente"""
        id_usuario = str(id_usuario).strip()
        for r in self.registros_estado:
            if str(r["id_usuario"]).strip() == id_usuario:
                r["fecha_ingreso"] = str(fecha_ingreso).strip()
    
    def obtener_idusuario(self, id_usuario):
        """Obtiene el estado de un cliente por su ID"""
        id_usuario = str(id_usuario).strip()
        for r in reversed(self.registros_estado):
            if str(r["id_usuario"]).strip() == id_usuario:
                return r
        return None
