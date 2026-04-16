class Usuario:
    """Modelo de un usuario individual"""
    
    def __init__(self, id_usuario, nombre, apellido, fecha_nacimiento, 
                 correo_electronico, cedula, direccion, numero_celular,
                 peso=None, estatura=None, tipo_sangre=None, lesiones=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.correo_electronico = correo_electronico
        self.cedula = cedula
        self.direccion = direccion
        self.numero_celular = numero_celular
        self.peso = peso
        self.estatura = estatura
        self.tipo_sangre = tipo_sangre
        self.lesiones = lesiones

    def __repr__(self):
        return f"Usuario(id={self.id_usuario}, nombre={self.nombre} {self.apellido})"

    def get_datos(self):
        """Retorna los datos del usuario como diccionario"""
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_nacimiento": self.fecha_nacimiento,
            "correo_electronico": self.correo_electronico,
            "cedula": self.cedula,
            "direccion": self.direccion,
            "numero_celular": self.numero_celular,
            "peso": self.peso,
            "estatura": self.estatura,
            "tipo_sangre": self.tipo_sangre,
            "lesiones": self.lesiones
        }


class Usuarios:
    """Clase que gestiona la colección de usuarios"""
    
    def __init__(self):
        self.usuarios = []
        self._ultimo_id = 0
        self.service = None
        self.historial_medico = None
        self.tabla_cliente = None

    def enlazar_tablas(self, historial_medico, tabla_cliente):
        """Enlaza el servicio con historial médico y tabla de clientes"""
        self.historial_medico = historial_medico
        self.tabla_cliente = tabla_cliente

    def crear_usuario(self):
        """Crea un nuevo usuario mediante entrada interactiva"""
        print("\nREGISTRO DE USUARIO")
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()
        correo_electronico = input("Correo electrónico: ").strip()
        cedula = input("Cédula: ").strip()
        direccion = input("Dirección: ").strip()
        numero_celular = input("Número de celular: ").strip()
        objetivo_entreno = input("Objetivo de entreno: ").strip()

        # Validar que los campos requeridos no estén vacíos
        if not all([nombre, apellido, fecha_nacimiento, correo_electronico, cedula, direccion, numero_celular]):
            print("Error: Todos los campos son requeridos.")
            return None

        self._ultimo_id += 1
        id_usuario = self._ultimo_id

        usuario = Usuario(
            id_usuario=id_usuario,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            correo_electronico=correo_electronico,
            cedula=cedula,
            direccion=direccion,
            numero_celular=numero_celular
        )

        self.usuarios.append(usuario)

        # Crear estado de cliente asociado
        if self.tabla_cliente:
            self.tabla_cliente.crear_estado_usuario(id_usuario, objetivo_entreno)

        # Crear historial médico
        if self.historial_medico:
            peso = input("Peso (kg): ").strip()
            estatura = input("Estatura (cm): ").strip()
            tipo_sangre = input("Tipo de sangre: ").strip()
            lesiones = input("Lesiones: ").strip()
            self.historial_medico.crear_historial_usuario(id_usuario, peso, estatura, tipo_sangre, lesiones)

        print(f"Usuario '{nombre} {apellido}' registrado correctamente con ID: {id_usuario}")
        return usuario

    def buscar_id(self, id_usuario):
        """Busca un usuario por su ID"""
        try:
            id_usuario = int(id_usuario)
        except (ValueError, TypeError):
            id_usuario = str(id_usuario).strip()

        for usuario in self.usuarios:
            if usuario.id_usuario == id_usuario or str(usuario.id_usuario) == str(id_usuario):
                return usuario
        return None

    def usuario_elegido(self):
        """Muestra un menú para que el usuario seleccione uno de la lista"""
        if not self.usuarios:
            print("\nNo hay usuarios registrados.")
            return None

        print("\nUSUARIOS DISPONIBLES")
        for i, usuario in enumerate(self.usuarios, start=1):
            print(f"{i}. {usuario.nombre} {usuario.apellido} (ID: {usuario.id_usuario})")

        try:
            opcion = input("Seleccione un usuario por número: ").strip()
            indice = int(opcion) - 1
            if 0 <= indice < len(self.usuarios):
                return self.usuarios[indice]
            else:
                print("Opción inválida.")
                return None
        except (ValueError, IndexError):
            print("Opción inválida.")
            return None

    def actualizar_ingreso(self, id_usuario, fecha_ingreso):
        """Actualiza la fecha de ingreso de un usuario"""
        usuario = self.buscar_id(id_usuario)
        if usuario:
            # Actualizar en tabla de clientes si existe
            if self.tabla_cliente:
                self.tabla_cliente.actualizar_fecha_ingreso(id_usuario, fecha_ingreso)
            # Actualizar en historial médico si existe
            if self.historial_medico:
                self.historial_medico.actualizar_fecha_ingreso(id_usuario, fecha_ingreso)

    def mostrar_usuarios(self):
        """Muestra todos los usuarios registrados en formato tabla"""
        if not self.usuarios:
            print("\nNo hay usuarios registrados.")
            return

        print("\nLISTADO DE USUARIOS")
        print("=" * 100)
        print(f"{'ID':<5} {'NOMBRE':<15} {'APELLIDO':<15} {'CÉDULA':<12} {'CORREO':<25} {'CELULAR':<12}")
        print("-" * 100)

        for usuario in self.usuarios:
            print(
                f"{usuario.id_usuario:<5} {usuario.nombre:<15} {usuario.apellido:<15} "
                f"{usuario.cedula:<12} {usuario.correo_electronico:<25} {usuario.numero_celular:<12}"
            )
