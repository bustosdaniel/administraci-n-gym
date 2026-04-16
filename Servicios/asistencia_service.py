class AsistenciaService:
    """Servicio para gestionar asistencias a clases"""
    
    def __init__(self):
        self.asistencias = []
        self._ultimo_id = 0
    
    def crear_asistencia(self, tabla_reservas):
        """Crea un nuevo registro de asistencia"""
        print("\nREGISTRO DE ASISTENCIA")
        usuario = tabla_reservas.usuarios.usuario_elegido()
        if not usuario:
            return

        reservas_usuario = [
            r for r in tabla_reservas.service.reservas if str(r["id_cliente"]) == str(usuario.id_usuario)
        ]
        if not reservas_usuario:
            print("Este usuario no tiene reservas disponibles.")
            return

        print("\nRESERVAS DISPONIBLES DEL USUARIO")
        for i, r in enumerate(reservas_usuario, start=1):
            print(f"{i}. Reserva {r['id_reserva']} | Fecha: {r['fecha_reserva']} | Estado: {r['estado_reserva']}")

        opcion = input("Seleccione reserva: ").strip()
        if not opcion.isdigit():
            print("Opción inválida.")
            return
        indice = int(opcion)
        if indice < 1 or indice > len(reservas_usuario):
            print("Opción fuera de rango.")
            return
        reserva = reservas_usuario[indice - 1]

        fecha_asistencia = input("Fecha asistencia: ").strip()
        asistira = input("¿Asistirá a la clase? (si/no): ").strip().lower()
        estado_asistencia = "asistira" if asistira == "si" else "no asistira"
        hora_entrada = input("Hora entrada: ").strip() or "pendiente"
        horas_salida = input("Hora salida: ").strip() or "pendiente"

        self._ultimo_id += 1
        id_asistencia = self._ultimo_id
        asistencia_doc = {
            "id_asistencia": id_asistencia,
            "id_reserva": reserva["id_reserva"],
            "fecha_asistencia": fecha_asistencia,
            "estado_asistencia": estado_asistencia,
            "hora_entrada": hora_entrada,
            "horas_salida": horas_salida,
        }
        self.asistencias.append(asistencia_doc)
        reserva["estado_reserva"] = estado_asistencia
        print("Registrado correctamente.")
        return asistencia_doc
