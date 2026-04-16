from Servicios.entrenadores_service import EntrenadoresService


class Entrenadores:
    """Clase delegadora que utiliza EntrenadoresService"""
    
    def __init__(self, usuarios=None):
        self.service = EntrenadoresService()
        self.usuarios = usuarios
    
    def elegir_entrenador(self):
        """Delega a EntrenadoresService"""
        return self.service.elegir_entrenador()
    
    def id_seleccionado_entrenador(self, id_entrenador):
        """Delega a EntrenadoresService"""
        return self.service.id_seleccionado_entrenador(id_entrenador)
    
    def mostrar_entrenadores(self):
        """Muestra todos los entrenadores en formato tabla"""
        if not self.service.entrenadores:
            print("\nNo hay entrenadores registrados.")
            return
        
        from index import tabla
        
        columnas = [
            ("ID_ENT", 6),
            ("NOMBRE", 14),
            ("ESPECIALIDAD", 12),
            ("HORARIO", 10),
            ("EXPERIENCIA", 8),
            ("EJERCICIOS", 22),
        ]
        filas = [
            (
                e["id_entrenador"],
                e["nombre"],
                e["especialidad"],
                e["horario"],
                e["experiencia"],
                ", ".join(e.get("ejercicios", [])[:2]),
            )
            for e in self.service.entrenadores
        ]
        tabla("ENTRENADORES", columnas, filas)
