from Servicios.membresia_service import MembresiasService


class Membresia:
    """Clase delegadora que utiliza MembresiasService"""
    
    def __init__(self, usuarios):
        self.service = MembresiasService()
        self.usuarios = usuarios
    
    def crear_membresia(self):
        """Delega a MembresiasService"""
        return self.service.crear_membresia(self.usuarios)
    
    def id_seleccionado(self, id_membresia):
        """Delega a MembresiasService"""
        return self.service.id_seleccionado(id_membresia)
    
    def elegir_membresia(self):
        """Delega a MembresiasService"""
        return self.service.elegir_membresia(self.usuarios)
    
    def mostrar_membresias(self, tabla_func):
        """Muestra todas las membresias registradas"""
        if not self.service.membresias:
            print("\nNo hay membresias registradas.")
            return
        columnas = [
            ("ID_MEM", 6),
            ("CLIENTE", 16),
            ("INICIO", 10),
            ("FIN", 10),
            ("ESTADO", 10),
        ]
        filas = []
        for m in self.service.membresias:
            cliente = self.usuarios.buscar_id(m["id_cliente"])
            nombre = cliente.nombre if cliente else "Sin nombre"
            filas.append((m["id_membresia"], nombre, m["fecha_inicio"], m["fecha_fin"], m["estado"]))
        tabla_func("MEMBRESIAS", columnas, filas)
