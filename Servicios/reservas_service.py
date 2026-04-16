class ReservasService:
    """Servicio para gestionar reservas de clases"""
    
    def __init__(self):
        self.reservas = []
        self._ultimo_id = 0
    
    def crear_reserva(self, usuarios, tabla_clases):
        """Crea una nueva reserva"""
        print("\nREGISTRO DE RESERVA")
        usuario = usuarios.usuario_elegido()
        if not usuario:
            return
        id_usuario = usuario.id_usuario

        clase = tabla_clases.elegir_clase()
        if not clase:
            return
        disponible, cupos_libres = tabla_clases.hay_cupo_disponible(clase)
        if not disponible:
            print("La clase está llena. Regresando al menú principal...")
            return

        confirmacion = input("La clase está disponible. ¿Quieres entrar a la clase? (si/no): ").strip().lower()
        if confirmacion != "si":
            print("No se creó la reserva. Regresando al menú principal...")
            return

        fecha_reserva = input("Fecha reserva: ").strip()
        estado_reserva = "reservada"

        self._ultimo_id += 1
        id_reserva = self._ultimo_id
        reserva = {
            "id_reserva": id_reserva,
            "id_cliente": str(id_usuario).strip(),
            "id_clase": clase["id_clase"],
            "fecha_reserva": fecha_reserva,
            "estado_reserva": estado_reserva,
        }
        self.reservas.append(reserva)

        if clase.get("id_reserva") is None:
            clase["id_reserva"] = id_reserva

        print(f"Reserva registrada correctamente. Cupos restantes: {cupos_libres - 1}")
        return reserva
    
    def id_seleccionado(self, id_reserva):
        """Busca una reserva por su ID"""
        try:
            id_reserva = int(id_reserva)
        except (ValueError, TypeError):
            return None
        for r in self.reservas:
            if r["id_reserva"] == id_reserva:
                return r
        return None
    
    def elegir_reserva(self, usuarios):
        """Permite elegir una reserva"""
        if not self.reservas:
            print("\nNo hay reservas registradas.")
            return None
        print("\nRESERVAS DISPONIBLES")
        for i, r in enumerate(self.reservas, start=1):
            cliente = usuarios.buscar_id(r["id_cliente"])
            nombre = cliente.nombre if cliente else "Sin nombre"
            print(f"{i}. {nombre} - {r['fecha_reserva']} - {r['estado_reserva']}")
        opcion = input("Seleccione reserva: ").strip()
        if not opcion.isdigit():
            print("Opción inválida.")
            return None
        indice = int(opcion)
        if indice < 1 or indice > len(self.reservas):
            print("Opción fuera de rango.")
            return None
        return self.reservas[indice - 1]
