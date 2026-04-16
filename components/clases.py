from Servicios.clases_service import ClasesService


class Clases:
    """Clase delegadora que utiliza ClasesService"""
    
    def __init__(self, tabla_entrenadores, tabla_sede):
        self.service = ClasesService()
        self.tabla_entrenadores = tabla_entrenadores
        self.tabla_sede = tabla_sede
    
    def enlazar_reservas(self, tabla_reservas):
        """Delega a ClasesService"""
        self.service.enlazar_reservas(tabla_reservas)
    
    def crear_clase(self):
        """Delega a ClasesService"""
        return self.service.crear_clase(self.tabla_entrenadores, self.tabla_sede)
    
    def cupos_ocupados(self, id_clase):
        """Delega a ClasesService"""
        return self.service.cupos_ocupados(id_clase)
    
    def hay_cupo_disponible(self, clase):
        """Delega a ClasesService"""
        return self.service.hay_cupo_disponible(clase)
    
    def id_seleccionado(self, id_clase):
        """Delega a ClasesService"""
        return self.service.id_seleccionado(id_clase)
    
    def elegir_clase(self):
        """Delega a ClasesService"""
        return self.service.elegir_clase()
    
    def mostrar_clases(self, tabla_func):
        """Muestra todas las clases registradas"""
        if not self.service.clases:
            print("\nNo hay clases registradas.")
            return
        columnas = [
            ("ID_CLASE", 7),
            ("ENTRENADOR", 14),
            ("SEDE", 12),
            ("ID_RES", 6),
            ("TIPO", 12),
            ("NUMERO", 7),
            ("HORARIO", 10),
            ("CUPO", 7),
        ]
        filas = []
        for c in self.service.clases:
            entrenador = self.tabla_entrenadores.id_seleccionado_entrenador(c["id_entrenador"])
            nombre_entrenador = entrenador["nombre"] if entrenador else "Sin nombre"
            sede = self.tabla_sede.id_seleccionado(c["id_sede"])
            nombre_sede = sede["nombre_sede"] if sede else "Sin sede"
            id_reserva_txt = c["id_reserva"] if c["id_reserva"] is not None else "-"
            _, cupos_libres = self.hay_cupo_disponible(c)
            cupo_txt = f"{cupos_libres}/{c['cupo_total']}"
            filas.append(
                (
                    c["id_clase"],
                    nombre_entrenador,
                    nombre_sede,
                    id_reserva_txt,
                    c["tipo_clase"],
                    c["numero_clase"],
                    c["horario"],
                    cupo_txt,
                )
            )
        tabla_func("CLASES", columnas, filas)
