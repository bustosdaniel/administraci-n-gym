class MembresiasService:
    """Servicio para gestionar membresias de usuarios"""
    
    def __init__(self):
        self.membresias = []
        self._ultimo_id = 0
    
    def crear_membresia(self, usuarios):
        """Crea una nueva membresia para un usuario"""
        print("\nREGISTRO DE MEMBRESIA")
        usuario = usuarios.usuario_elegido()
        if not usuario:
            return
        id_usuario = usuario.id_usuario

        self._ultimo_id += 1
        id_membresia = self._ultimo_id
        fecha_inicio = input("Fecha inicio: ").strip()
        fecha_fin = "pendiente"
        estado = "activa"
        usuarios.actualizar_ingreso(id_usuario, fecha_inicio)
        membresia = {
            "id_membresia" : id_membresia,
            "id_cliente"   : str(id_usuario).strip(),
            "fecha_inicio" : fecha_inicio,
            "fecha_fin"    : fecha_fin,
            "estado"       : estado,
        }
        self.membresias.append(membresia)
        print("Registrado correctamente.")
        return membresia
    
    def id_seleccionado(self, id_membresia):
        """Busca una membresia por su ID"""
        try:
            id_membresia = int(id_membresia)
        except (ValueError, TypeError):
            return None
        for m in self.membresias:
            if m["id_membresia"] == id_membresia:
                return m
        return None
    
    def elegir_membresia(self, usuarios):
        """Permite elegir una membresia del listado disponible"""
        print("\nMEMBRESIAS DISPONIBLES")
        for i, m in enumerate(self.membresias, start=1):
            cliente = usuarios.buscar_id(m["id_cliente"])
            nombre = cliente.nombre if cliente else "Sin nombre"
            print(f"{i}. {nombre} | inicio: {m['fecha_inicio']} | estado: {m['estado']}")
        opcion = input("Seleccione membresia: ").strip()
        if not opcion.isdigit():
            print("Opción inválida.")
            return None
        indice = int(opcion)
        if indice < 1 or indice > len(self.membresias):
            print("Opción fuera de rango.")
            return None
        return self.membresias[indice - 1]
