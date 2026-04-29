from components.usuarios import Usuario

def tabla(titulo, columnas, filas):
    """Función auxiliar para mostrar tablas formateadas"""
    def _fmt_cell(valor, ancho):
        texto = "-" if valor is None else str(valor)
        if len(texto) > ancho:
            if ancho <= 3:
                return texto[:ancho]
            return (texto[: ancho - 3] + "...")
        return texto.ljust(ancho)
    
    ancho_total = sum(ancho for _, ancho in columnas) + (3 * (len(columnas) - 1))
    print(f"\n{titulo}")
    print("=" * ancho_total)
    encabezado = " | ".join(_fmt_cell(nombre, ancho) for nombre, ancho in columnas)
    print(encabezado)
    print("-" * ancho_total)

    if not filas:
        print("Sin registros.")
        return

    for fila in filas:
        celdas = []
        for i, (_, ancho) in enumerate(columnas):
            valor = fila[i] if i < len(fila) else "-"
            celdas.append(_fmt_cell(valor, ancho))
        print(" | ".join(celdas))

class UsuarioService:

    def __init__(self):
        self.usuarios = []
        self._ultimo_id_usuario = 0
        self.historial_medico = None
        self.tabla_cliente = None

    def crear_usuario(self):
        print("\nREGISTRO NUEVO USUARIO")

        self._ultimo_id_usuario += 1
        id_usuario = self._ultimo_id_usuario

        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        fecha_nac = input("Fecha de nacimiento: ").strip()
        correo = input("Correo electrónico: ").strip()
        cedula = input("Cédula: ").strip()
        direccion = input("Dirección: ").strip()
        celular = input("Celular: ").strip()

        print("\nHISTORIAL MEDICO")
        peso = input("Peso: ").strip() or "pendiente"
        estatura = input("Estatura: ").strip() or "pendiente"
        tipo_sangre = input("Tipo de sangre: ").strip() or "pendiente"
        lesiones = input("Lesiones: ").strip() or "ninguna"

        usuario = Usuario(
            id_usuario, nombre, apellido, fecha_nac,
            correo, cedula, direccion, celular,
            peso, estatura, tipo_sangre, lesiones
        )

        self.usuarios.append(usuario)

        return usuario

    def enlazar_tablas(self, historial_medico, tabla_cliente):
        """Enlaza el servicio con historial médico y tabla de clientes"""
        self.historial_medico = historial_medico
        self.tabla_cliente = tabla_cliente

    def actualizar_ingreso(self, id_usuario, fecha_ingreso):
        """Actualiza la fecha de ingreso en historial y tabla cliente"""
        if self.tabla_cliente:
            self.tabla_cliente.actualizar_fecha_ingreso(id_usuario, fecha_ingreso)
        if self.historial_medico:
            self.historial_medico.actualizar_fecha_ingreso(id_usuario, fecha_ingreso)

    def mostrar_usuarios(self):
        """Muestra todos los usuarios registrados en formato tabla"""
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
                u.id_usuario,
                u.nombre,
                u.apellido,
                u.fecha_nacimiento,
                u.correo_electronico,
                u.cedula,
                u.direccion,
                u.numero_celular,
            )
            for u in self.usuarios
        ]
        tabla("USUARIOS REGISTRADOS", columnas, filas)

    def buscar_id(self, id_usuario):
        """Busca un usuario por su ID"""
        id_usuario = str(id_usuario).strip()
        for u in self.usuarios:
            if str(u.id_usuario).strip() == id_usuario:
                return u
        return None

    def usuario_elegido(self):
        """Muestra menú para que el usuario seleccione un usuario"""
        if not self.usuarios:
            print("\nNo hay usuarios registrados.")
            return None
        print("\nUSUARIOS DISPONIBLES")
        for i, u in enumerate(self.usuarios, start=1):
            print(f"{i}. {u.nombre} {u.apellido}")
        opcion = input("Seleccione usuario: ").strip()
        if not opcion.isdigit():
            print("Opción inválida.")
            return None
        indice = int(opcion)
        if indice < 1 or indice > len(self.usuarios):
            print("Opción fuera de rango.")
            return None
        return self.usuarios[indice - 1]