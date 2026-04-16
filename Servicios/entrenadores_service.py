class EntrenadoresService:
    """Servicio para gestionar entrenadores"""
    
    def __init__(self):
        self.entrenadores = [
            {
                "id_entrenador": 1,
                "id_usuario": "-",
                "nombre": "Carlos Rios",
                "especialidad": "Fuerza",
                "horario": "06:00-14:00",
                "experiencia": "5 anios",
                "ejercicios": ["Sentadilla", "Press de banca"],
            },
            {
                "id_entrenador": 2,
                "id_usuario": "-",
                "nombre": "Laura Mejia",
                "especialidad": "Cardio",
                "horario": "14:00-20:00",
                "experiencia": "7 anios",
                "ejercicios": ["Burpees", "Saltos de cuerda"],
            },
            {
                "id_entrenador": 3,
                "id_usuario": "-",
                "nombre": "Andres Salazar",
                "especialidad": "Funcional",
                "horario": "08:00-16:00",
                "experiencia": "4 anios",
                "ejercicios": ["Plancha", "Zancadas"],
            },
        ]
        self._ultimo_id_entrenador = len(self.entrenadores)
    
    def elegir_entrenador(self):
        """Muestra menú de entrenadores disponibles y permite seleccionar"""
        print("\nENTRENADORES DISPONIBLES")
        for e in self.entrenadores:
            ejercicios = ", ".join(e.get("ejercicios", [])[:2])
            print(f"{e['id_entrenador']}. {e['nombre']} - {e['especialidad']} | ejercicios: {ejercicios}")
        opcion = input("Seleccione entrenador: ").strip()
        entrenador = self.id_seleccionado_entrenador(opcion)
        if not entrenador:
            print("Entrenador no válido.")
            return None
        return entrenador
    
    def id_seleccionado_entrenador(self, id_entrenador):
        """Busca un entrenador por su ID"""
        try:
            id_entrenador = int(id_entrenador)
        except (ValueError, TypeError):
            return None
        
        for e in self.entrenadores:
            if e["id_entrenador"] == id_entrenador:
                return e
        return None
