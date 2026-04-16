class ClasesService:
    """Servicio para gestionar clases de entrenamiento"""
    
    def __init__(self):
        self.clases = []
        self.tabla_reservas = None
        self._ultimo_id = 0
    
    def enlazar_reservas(self, tabla_reservas):
        """Enlaza con la tabla de reservas"""
        self.tabla_reservas = tabla_reservas
    
    def crear_clase(self, tabla_entrenadores, tabla_sede):
        """Crea una nueva clase"""
        print("\nREGISTRO DE CLASE")
        entrenador = tabla_entrenadores.elegir_entrenador()
        if not entrenador:
            return
        sede = tabla_sede.elegir_sede()
        if not sede:
            return

        id_reserva_valor = None
        tipo_clase = input("Tipo de clase: ").strip()
        numero_clase = input("Numero de clase: ").strip()
        horario = input("Horario de la clase: ").strip()
        cupo_txt = input("Cupo total: ").strip()
        try:
            cupo_total = int(cupo_txt)
            if cupo_total < 1:
                print("El cupo debe ser mayor a 0.")
                return
        except ValueError:
            print("Cupo inválido. Debe ser numérico.")
            return

        self._ultimo_id += 1
        id_clase = self._ultimo_id
        clase_doc = {
            "id_clase": id_clase,
            "id_entrenador": entrenador["id_entrenador"],
            "id_sede": sede["id_sede"],
            "id_reserva": id_reserva_valor,
            "tipo_clase": tipo_clase,
            "numero_clase": numero_clase,
            "horario": horario,
            "cupo_total": cupo_total,
        }
        self.clases.append(clase_doc)
        print("Registrado correctamente.")
        return clase_doc
    
    def cupos_ocupados(self, id_clase):
        """Calcula cupos ocupados de una clase"""
        if not self.tabla_reservas:
            return 0
        return sum(
            1
            for r in self.tabla_reservas.service.reservas
            if r["id_clase"] == id_clase and r["estado_reserva"] == "reservada"
        )
    
    def hay_cupo_disponible(self, clase):
        """Verifica si hay cupo disponible"""
        cupo_total = int(clase.get("cupo_total", 0))
        cupos_libres = cupo_total - self.cupos_ocupados(clase["id_clase"])
        return cupos_libres > 0, cupos_libres
    
    def id_seleccionado(self, id_clase):
        """Busca una clase por su ID"""
        try:
            id_clase = int(id_clase)
        except (ValueError, TypeError):
            return None
        for c in self.clases:
            if c["id_clase"] == id_clase:
                return c
        return None
    
    def elegir_clase(self):
        """Permite elegir una clase"""
        if not self.clases:
            print("\nNo hay clases registradas.")
            return None
        print("\nCLASES DISPONIBLES")
        for i, c in enumerate(self.clases, start=1):
            disponible, cupos_libres = self.hay_cupo_disponible(c)
            estado = "disponible" if disponible else "lleno"
            print(
                f"{i}. Tipo: {c['tipo_clase']} | Horario: {c['horario']} | "
                f"Cupo: {cupos_libres}/{c['cupo_total']} | Estado: {estado}"
            )
        opcion = input("Seleccione clase: ").strip()
        if not opcion.isdigit():
            print("Opción inválida.")
            return None
        indice = int(opcion)
        if indice < 1 or indice > len(self.clases):
            print("Opción fuera de rango.")
            return None
        return self.clases[indice - 1]
