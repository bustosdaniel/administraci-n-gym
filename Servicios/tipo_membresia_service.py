class TipoMembresiasService:
    """Servicio para gestionar tipos de membresias"""
    
    TIPOS_VALIDOS = ["basica", "platinum", "premium", "vip"]
    
    def __init__(self):
        self.tipos = []
        self._ultimo_id = 0
    
    def crear_tipo(self, tabla_membresia):
        """Crea un nuevo tipo de membresia"""
        print("\nREGISTRO DE TIPO DE MEMBRESIA")
        membresia = tabla_membresia.elegir_membresia()
        if not membresia:
            return

        print("Tipos disponibles: basica | platinum | premium | vip")
        tipo = input("Tipo: ").strip().lower()
        if tipo not in self.TIPOS_VALIDOS:
            print(f"Tipo invalido. Debe ser uno de: {', '.join(self.TIPOS_VALIDOS)}")
            return

        self._ultimo_id += 1
        id_tipo = self._ultimo_id
        tipo_doc = {
            "id_tipo": id_tipo,
            "id_membresia": membresia["id_membresia"],
            "tipo": tipo,
        }
        self.tipos.append(tipo_doc)
        print("Registrado correctamente.")
        return tipo_doc
    
    def id_seleccionado(self, id_tipo):
        """Busca un tipo por su ID"""
        try:
            id_tipo = int(id_tipo)
        except (ValueError, TypeError):
            return None
        for t in self.tipos:
            if t["id_tipo"] == id_tipo:
                return t
        return None
    
    def elegir_tipo(self):
        """Permite elegir un tipo de membresia"""
        if not self.tipos:
            print("\nNo hay tipos de membresia registrados.")
            return None
        print("\nTIPOS DE MEMBRESIA DISPONIBLES")
        for i, t in enumerate(self.tipos, start=1):
            print(f"{i}. {t['tipo']}")
        opcion = input("Seleccione tipo de membresia: ").strip()
        if not opcion.isdigit():
            print("Opción inválida.")
            return None
        indice = int(opcion)
        if indice < 1 or indice > len(self.tipos):
            print("Opción fuera de rango.")
            return None
        return self.tipos[indice - 1]
