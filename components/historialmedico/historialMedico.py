class HistorialMedico:
    def __init__(self, usuarios: Usuarios):
        self.historiales = []  # En memoria, sin MongoDB
        # self.historiales = list(_historiales_col.find({}, {"_id": 0}))
        self.usuarios = usuarios
        self._ultimo_id_historial = max((h.get("id_historial_med", 0) for h in self.historiales), default=0)

    def crear_historial_usuario(self, id_cliente, peso, estatura, tipo_sangre, lesiones):
        self._ultimo_id_historial += 1
        id_historial_med = self._ultimo_id_historial
        imc = "pendiente"
        historial = {
            "id_historial_med": id_historial_med,
            "id_cliente": str(id_cliente).strip(),
            "fecha_ingreso": "pendiente",
            "peso": peso,
            "estatura": estatura,
            "tipo_sangre": tipo_sangre,
            "lesiones": lesiones,
            "imc": imc,
        }
        self.historiales.append(historial)
        # _historiales_col.insert_one(historial)  # Comentado: Sin MongoDB
        print("Registrado correctamente.")

    def actualizar_fecha_ingreso(self, id_cliente, fecha_ingreso):
        id_cliente = str(id_cliente).strip()
        for h in self.historiales:
            if str(h["id_cliente"]).strip() == id_cliente:
                h["fecha_ingreso"] = str(fecha_ingreso).strip()
        # _historiales_col.update_many(  # Comentado: Sin MongoDB
        #     {"id_cliente": id_cliente},
        #     {"$set": {"fecha_ingreso": str(fecha_ingreso).strip()}},
        # )

    def id_seleccionado_cliente(self, id_cliente):
        id_cliente = str(id_cliente).strip()
        for h in reversed(self.historiales):
            if str(h["id_cliente"]).strip() == id_cliente:
                return h
        return None

    def mostrar_historiales(self):
        if not self.historiales:
            print("\nNo hay historiales médicos registrados.")
            return
        columnas = [
            ("ID_HIST", 6),
            ("USUARIO", 14),
            ("INGRESO", 10),
            ("PESO", 6),
            ("ESTATURA", 8),
            ("SANGRE", 8),
            ("LESIONES", 12),
            ("IMC", 6),
        ]
        filas = []
        for h in self.historiales:
            cliente = self.usuarios.buscar_id(h["id_cliente"])
            nombre_usuario = cliente["nombre"] if cliente else "Sin nombre"
            filas.append(
                (
                    h["id_historial_med"],
                    nombre_usuario,
                    h["fecha_ingreso"],
                    h["peso"],
                    h["estatura"],
                    h["tipo_sangre"],
                    h["lesiones"],
                    h["imc"],
                )
            )
        tabla("HISTORIALES MEDICOS", columnas, filas)
