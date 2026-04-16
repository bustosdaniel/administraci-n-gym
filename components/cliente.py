from Servicios.cliente_service import ClienteService


class Cliente:
    """Clase delegadora que utiliza ClienteService"""
    
    def __init__(self, usuarios):
        self.service = ClienteService()
        self.usuarios = usuarios
    
    def crear_cliente(self):
        """Crea un nuevo cliente"""
        print("\nEste registro se crea al registrar un usuario para mantener la relacion por ID.")
    
    def crear_estado_usuario(self, id_usuario, objetivo_entreno):
        """Delega a ClienteService"""
        return self.service.crear_estado_usuario(id_usuario, objetivo_entreno)
    
    def actualizar_fecha_ingreso(self, id_usuario, fecha_ingreso):
        """Delega a ClienteService"""
        return self.service.actualizar_fecha_ingreso(id_usuario, fecha_ingreso)
    
    def obtener_idusuario(self, id_usuario):
        """Delega a ClienteService"""
        return self.service.obtener_idusuario(id_usuario)
    
    def mostrar_estados_clientes(self):
        """Muestra todos los estados de clientes en formato tabla"""
        if not self.service.registros_estado:
            print("\nNo hay estados de clientes registrados.")
            return
        
        from index import tabla
        
        columnas = [
            ("USUARIO", 16),
            ("INGRESO", 10),
            ("MEMBRESIA", 12),
            ("OBJETIVO", 22),
        ]
        filas = []
        for r in self.service.registros_estado:
            usuario = self.usuarios.buscar_id(r["id_usuario"])
            nombre_usuario = usuario.nombre if usuario else "Sin nombre"
            filas.append((nombre_usuario, r["fecha_ingreso"], r["estado_membresia"], r["objetivo"]))
        tabla("ESTADO DE CLIENTES", columnas, filas)
