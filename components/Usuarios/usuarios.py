class Usuarios:
    def __init__(self):
        self.usuarios = []  # En memoria, sin MongoDB
        # self.usuarios = list(_usuarios_col.find({}, {"_id": 0}))
        self.historial_medico = None
        self.tabla_cliente = None
        self._ultimo_id_usuario = max((u.get("id_usuario", 0) for u in self.usuarios), default=0)

    def enlazar_tablas(self, historial_medico, tabla_cliente):
        self.historial_medico = historial_medico
        self.tabla_cliente = tabla_cliente

    def actualizar_ingreso(self, id_usuario, fecha_ingreso):
        if self.tabla_cliente:
            self.tabla_cliente.actualizar_fecha_ingreso(id_usuario, fecha_ingreso)
        if self.historial_medico:
            self.historial_medico.actualizar_fecha_ingreso(id_usuario, fecha_ingreso)

    def crear_usuario(self):
        print("\nREGISTRO NUEVO USUARIO")
        self._ultimo_id_usuario += 1
        id_usuario = self._ultimo_id_usuario
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        fecha_nac = input("Fecha de nacimiento: ").strip()
        correo = input("Correo electrónico: ").strip()
        cedula = input("Cédula Ciudadana: ").strip()
        direccion = input("Dirección: ").strip()
        celular = input("Número celular: ").strip()
        objetivo_entreno = input("Objetivo de entreno: ").strip()
        print("\nHISTORIAL MEDICO")
        peso = input("Peso: ").strip() or "pendiente"
        estatura = input("Estatura: ").strip() or "pendiente"
        tipo_sangre = input("Tipo de sangre: ").strip() or "pendiente"
        lesiones = input("Lesiones: ").strip() or "ninguna"

        usuario = {
            "id_usuario": id_usuario,
            "nombre": nombre,
            "apellido": apellido,
            "fecha_nacimiento": fecha_nac,
            "correo_electronico": correo,
            "cedula": cedula,
            "direccion": direccion,
            "numero_celular": celular,
        }
        self.usuarios.append(usuario)
        # _usuarios_col.insert_one(usuario)  # Comentado: Sin MongoDB
        if self.tabla_cliente:
            self.tabla_cliente.crear_estado_usuario(id_usuario, objetivo_entreno)
        if self.historial_medico:
            self.historial_medico.crear_historial_usuario(
                id_usuario,
                peso,
                estatura,
                tipo_sangre,
                lesiones,
            )
        print(f"\nUsuario '{nombre} {apellido}' registrado correctamente.")

    def mostrar_usuarios(self):
        if not self.usuarios:
            print("\nNo hay usuarios registrados.")
            return
        columnas = [
            ("ID", 3),
            ("NOMBRE", 10),
            ("APELLIDO", 10),
            ("NACIMIENTO", 10),
            ("CORREO", 16),
            ("CEDULA", 10),
            ("DIRECCION", 14),
            ("CELULAR", 10),
        ]
        filas = [
            (
                u["id_usuario"],
                u["nombre"],
                u["apellido"],
                u["fecha_nacimiento"],
                u["correo_electronico"],
                u["cedula"],
                u["direccion"],
                u["numero_celular"],
            )
            for u in self.usuarios
        ]
        tabla("USUARIOS REGISTRADOS", columnas, filas)

    def buscar_id(self, id_usuario):
        id_usuario = str(id_usuario).strip()
        for u in self.usuarios:
            if str(u["id_usuario"]).strip() == id_usuario:
                return u
        return None

    def usuario_elegido(self):
        if not self.usuarios:
            print("\nNo hay usuarios registrados.")
            return None
        print("\nUSUARIOS DISPONIBLES")
        for i, u in enumerate(self.usuarios, start=1):
            print(f"{i}. {u['nombre']} {u['apellido']}")
        opcion = input("Seleccione usuario: ").strip()
        if not opcion.isdigit():
            print("Opción inválida.")
            return None
        indice = int(opcion)
        if indice < 1 or indice > len(self.usuarios):
            print("Opción fuera de rango.")
            return None
        return self.usuarios[indice - 1]
