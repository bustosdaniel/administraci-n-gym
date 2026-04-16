class SedeService:
    """Servicio para gestionar sedes del gimnasio"""
    
    def __init__(self):
        sedes_base = [
            {
                "id_sede": 1,
                "nombre_sede": "GYM FORTE Centro",
                "direccion": "Calle 10 #15-20",
                "telefono": "3001112233",
                "horario": "05:00-22:00",
            },
            {
                "id_sede": 2,
                "nombre_sede": "GYM FORTE Norte",
                "direccion": "Av 45 #80-12",
                "telefono": "3004445566",
                "horario": "06:00-21:00",
            },
            {
                "id_sede": 3,
                "nombre_sede": "GYM FORTE Sur",
                "direccion": "Cra 30 #12-05",
                "telefono": "3007778899",
                "horario": "05:30-21:30",
            },
        ]
        self.sedes = sedes_base
    
    def elegir_sede(self):
        """Permite elegir una sede"""
        print("\nSEDES DISPONIBLES")
        for s in self.sedes:
            print(f"{s['id_sede']}. {s['nombre_sede']} - {s['direccion']}")
        opcion = input("Seleccione sede: ").strip()
        sede = self.id_seleccionado(opcion)
        if not sede:
            print("Sede no válida.")
            return None
        return sede
    
    def id_seleccionado(self, id_sede):
        """Busca una sede por su ID"""
        try:
            id_sede = int(id_sede)
        except (ValueError, TypeError):
            return None
        for s in self.sedes:
            if s["id_sede"] == id_sede:
                return s
        return None
