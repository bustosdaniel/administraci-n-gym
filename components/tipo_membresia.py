from Servicios.tipo_membresia_service import TipoMembresiasService


class TipoMembresia:
    """Clase delegadora que utiliza TipoMembresiasService"""
    
    def __init__(self, tabla_membresia):
        self.service = TipoMembresiasService()
        self.tabla_membresia = tabla_membresia
    
    def crear_tipo(self):
        """Delega a TipoMembresiasService"""
        return self.service.crear_tipo(self.tabla_membresia)
    
    def id_seleccionado(self, id_tipo):
        """Delega a TipoMembresiasService"""
        return self.service.id_seleccionado(id_tipo)
    
    def elegir_tipo(self):
        """Delega a TipoMembresiasService"""
        return self.service.elegir_tipo()
    
    def mostrar_tipos(self, tabla_func):
        """Muestra todos los tipos de membresia"""
        if not self.service.tipos:
            print("\nNo hay tipos de membresia registrados.")
            return
        columnas = [("ID_TIPO", 7), ("ID_MEM", 7), ("CLIENTE", 16), ("TIPO", 10)]
        filas = []
        for t in self.service.tipos:
            membresia = self.tabla_membresia.id_seleccionado(t["id_membresia"])
            cliente = self.tabla_membresia.usuarios.buscar_id(membresia["id_cliente"]) if membresia else None
            nombre = cliente.nombre if cliente else "Sin nombre"
            filas.append((t["id_tipo"], t["id_membresia"], nombre, t["tipo"]))
        tabla_func("TIPOS DE MEMBRESIA", columnas, filas)
