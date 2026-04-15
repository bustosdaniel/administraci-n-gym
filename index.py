from datetime import date
from components.Usuarios.usuarios import Usuarios
from components.Eliminar.eliminarUsuario import EliminarUsuario
##from pymongo import MongoClient


def _fmt_cell(valor, ancho):
    texto = "-" if valor is None else str(valor)
    if len(texto) > ancho:
        if ancho <= 3:
            return texto[:ancho]
        return (texto[: ancho - 3] + "...")
    return texto.ljust(ancho)


def tabla(titulo, columnas, filas):
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

class Cliente:
    def __init__(self, usuarios: Usuarios):
        self.registros_estado = []  # En memoria, sin MongoDB
        # self.registros_estado = list(_clientes_col.find({}, {"_id": 0}))
        self.usuarios = usuarios

    def crear_cliente(self):
        print("\nEste registro se crea al registrar un usuario para mantener la relacion por ID.")

    def crear_estado_usuario(self, id_usuario, objetivo_entreno):
        estado_membresia = "activa"
        objetivo = objetivo_entreno if objetivo_entreno else "acondicionamiento general"
        registro = {
            "id_usuario": str(id_usuario).strip(),
            "fecha_ingreso": "pendiente",
            "estado_membresia": estado_membresia,
            "objetivo": objetivo,
        }
        self.registros_estado.append(registro)
        # _clientes_col.insert_one(registro)  # Comentado: Sin MongoDB
        print("Registrado correctamente.")

    def actualizar_fecha_ingreso(self, id_usuario, fecha_ingreso):
        id_usuario = str(id_usuario).strip()
        for r in self.registros_estado:
            if str(r["id_usuario"]).strip() == id_usuario:
                r["fecha_ingreso"] = str(fecha_ingreso).strip()
        # _clientes_col.update_many(  # Comentado: Sin MongoDB
        #     {"id_usuario": id_usuario},
        #     {"$set": {"fecha_ingreso": str(fecha_ingreso).strip()}},
        # )

    def obtener_idusuario(self, id_usuario):
        id_usuario = str(id_usuario).strip()
        for r in reversed(self.registros_estado):
            if str(r["id_usuario"]).strip() == id_usuario:
                return r
        return None

    def mostrar_estados_clientes(self):
        if not self.registros_estado:
            print("\nNo hay estados de clientes registrados.")
            return
        columnas = [
            ("USUARIO", 16),
            ("INGRESO", 10),
            ("MEMBRESIA", 12),
            ("OBJETIVO", 22),
        ]
        filas = []
        for r in self.registros_estado:
            usuario = self.usuarios.buscar_id(r["id_usuario"])
            nombre_usuario = usuario["nombre"] if usuario else "Sin nombre"
            filas.append((nombre_usuario, r["fecha_ingreso"], r["estado_membresia"], r["objetivo"]))
        tabla("ESTADO DE CLIENTES", columnas, filas)

class Entrenadores:
    def __init__(self, usuarios: Usuarios):
        entrenadores_base = [
            {
                "id_entrenador": 1,
                "id_usuario": "-",
                "nombre": "Carlos Rios",
                "especialidad": "Fuerza",
                "horario": "06:00-14:00",
                "experiencia": "5 anios",
                "ejercicios": ["Sentadilla", "Press de banca"],
            },
            {
                "id_entrenador": 2,
                "id_usuario": "-",
                "nombre": "Laura Mejia",
                "especialidad": "Cardio",
                "horario": "14:00-20:00",
                "experiencia": "7 anios",
                "ejercicios": ["Burpees", "Saltos de cuerda"],
            },
            {
                "id_entrenador": 3,
                "id_usuario": "-",
                "nombre": "Andres Salazar",
                "especialidad": "Funcional",
                "horario": "08:00-16:00",
                "experiencia": "4 anios",
                "ejercicios": ["Plancha", "Zancadas"],
            },
        ]
        if len(entrenadores_base) > 0:  # Sin MongoDB
            # if _entrenadores_col.count_documents({}) == 0:
            #     _entrenadores_col.insert_many(entrenadores_base)
            self.entrenadores = entrenadores_base
        # self.entrenadores = list(_entrenadores_col.find({}, {"_id": 0}))
        self.usuarios = usuarios
        self._ultimo_id_entrenador = len(self.entrenadores)

    def elegir_entrenador(self):
        print("\nENTRENADORES DISPONIBLES")
        for e in self.entrenadores:
            ejercicios = ", ".join(e.get("ejercicios", [])[:2])
            print(f"{e['id_entrenador']}. {e['nombre']} - {e['especialidad']} | ejercicios: {ejercicios}")
        opcion = input("Seleccione entrenador: ").strip()
        entrenador = self.id_seleccionado_entrenador(opcion)
        if not entrenador:
            print("Entrenador no válido.")
            return None
        return entrenador

    def id_seleccionado_entrenador(self, id_entrenador):
        try:
            id_entrenador = int(id_entrenador)
        except (ValueError, TypeError):
            return None

        for e in self.entrenadores:
            if e["id_entrenador"] == id_entrenador:
                return e
        return None

    def mostrar_entrenadores(self):
        if not self.entrenadores:
            print("\nNo hay entrenadores registrados.")
            return

        columnas = [
            ("ID_ENT", 6),
            ("NOMBRE", 14),
            ("ESPECIALIDAD", 12),
            ("HORARIO", 10),
            ("EXPERIENCIA", 8),
            ("EJERCICIOS", 22),
        ]
        filas = [
            (
                e["id_entrenador"],
                e["nombre"],
                e["especialidad"],
                e["horario"],
                e["experiencia"],
                ", ".join(e.get("ejercicios", [])[:2]),
            )
            for e in self.entrenadores
        ]
        tabla("ENTRENADORES", columnas, filas)


class Rutinas:
    def __init__(self, usuarios: Usuarios, tabla_cliente: Cliente, tabla_entrenadores: Entrenadores):
        self.rutinas = []  # En memoria, sin MongoDB
        # self.rutinas = list(_rutinas_col.find({}, {"_id": 0}))
        self.usuarios = usuarios
        self.tabla_cliente = tabla_cliente
        self.tabla_entrenadores = tabla_entrenadores
        self._ultimo_id_rutina = max((r.get("id_rutina", 0) for r in self.rutinas), default=0)

    def crear_rutina(self):
        print("\nREGISTRO DE RUTINA")
        cliente = self.usuarios.usuario_elegido()
        if not cliente:
            return
        id_cliente = cliente["id_usuario"]

        entrenador = self.tabla_entrenadores.elegir_entrenador()
        if not entrenador:
            return

        estado_cliente = self.tabla_cliente.obtener_idusuario(id_cliente)
        if not estado_cliente:
            print("El cliente no tiene objetivo registrado en la tabla de estado.")
            return

        self._ultimo_id_rutina += 1
        id_rutina = self._ultimo_id_rutina
        objetivo = estado_cliente["objetivo"]
        tiempo_entreno = input("Tiempo de entreno: ").strip()
        ejercicios_sugeridos = entrenador.get("ejercicios", [])[:2]
        if ejercicios_sugeridos:
            print("Ejercicios sugeridos por el entrenador:")
            for i, ejercicio in enumerate(ejercicios_sugeridos, start=1):
                print(f"{i}. {ejercicio}")

        rutina = {
            "id_rutina": id_rutina,
            "id_cliente": str(id_cliente).strip(),
            "id_entrenador": entrenador["id_entrenador"],
            "objetivo": objetivo,
            "tiempo_entreno": tiempo_entreno,
            "ejercicios": ", ".join(ejercicios_sugeridos),
        }
        self.rutinas.append(rutina)
        # _rutinas_col.insert_one(rutina)  # Comentado: Sin MongoDB
        print("Registrado correctamente.")

    def mostrar_rutinas(self):
        if not self.rutinas:
            print("\nNo hay rutinas registradas.")
            return

        columnas = [
            ("ID_RUT", 6),
            ("CLIENTE", 14),
            ("ENTRENADOR", 14),
            ("OBJETIVO", 18),
            ("TIEMPO", 10),
            ("EJERCICIOS", 24),
        ]
        filas = []
        for r in self.rutinas:
            cliente = self.usuarios.buscar_id(r["id_cliente"])
            nombre_cliente = cliente["nombre"] if cliente else "Sin nombre"
            entrenador = self.tabla_entrenadores.id_seleccionado_entrenador(r["id_entrenador"])
            nombre_entrenador = entrenador["nombre"] if entrenador else "Sin asignar"
            filas.append(
                (
                    r["id_rutina"],
                    nombre_cliente,
                    nombre_entrenador,
                    r["objetivo"],
                    r["tiempo_entreno"],
                    r["ejercicios"],
                )
            )
        tabla("RUTINAS", columnas, filas)

class Membresia:
    def __init__(self, usuarios: Usuarios):
        self.membresias = []  # En memoria, sin MongoDB
        # self.membresias = list(_membresias_col.find({}, {"_id": 0}))
        self.usuarios = usuarios
        self._ultimo_id = max((m.get("id_membresia", 0) for m in self.membresias), default=0)

    def crear_membresia(self):
        print("\nREGISTRO DE MEMBRESIA")
        usuario = self.usuarios.usuario_elegido()
        if not usuario:
            return
        id_usuario = usuario["id_usuario"]

        self._ultimo_id += 1
        id_membresia = self._ultimo_id
        fecha_inicio = input("Fecha inicio: ").strip()
        fecha_fin = "pendiente"
        estado = "activa"
        self.usuarios.actualizar_ingreso(id_usuario, fecha_inicio)
        membresia = {
            "id_membresia" : id_membresia,
            "id_cliente"   : str(id_usuario).strip(),
            "fecha_inicio" : fecha_inicio,
            "fecha_fin"    : fecha_fin,
            "estado"       : estado,
        }
        self.membresias.append(membresia)
        # _membresias_col.insert_one(membresia)  # Comentado: Sin MongoDB
        print("Registrado correctamente.")

    def id_seleccionado(self, id_membresia):
        try:
            id_membresia = int(id_membresia)
        except (ValueError, TypeError):
            return None
        for m in self.membresias:
            if m["id_membresia"] == id_membresia:
                return m
        return None

    def elegir_membresia(self):
        print("\nMEMBRESIAS DISPONIBLES")
        for i, m in enumerate(self.membresias, start=1):
            cliente = self.usuarios.buscar_id(m["id_cliente"])
            nombre = cliente["nombre"] if cliente else "Sin nombre"
            print(f"{i}. {nombre} | inicio: {m['fecha_inicio']} | estado: {m['estado']}")
        opcion = input("Seleccione membresia: ").strip()
        if not opcion.isdigit():
            print("Opción inválida.")
            return None
        indice = int(opcion)
        if indice < 1 or indice > len(self.membresias):
            print("Opción fuera de rango.")
            return None
        return self.membresias[indice - 1]

    def mostrar_membresias(self):
        if not self.membresias:
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
        for m in self.membresias:
            cliente = self.usuarios.buscar_id(m["id_cliente"])
            nombre = cliente["nombre"] if cliente else "Sin nombre"
            filas.append((m["id_membresia"], nombre, m["fecha_inicio"], m["fecha_fin"], m["estado"]))
        tabla("MEMBRESIAS", columnas, filas)

class TipoMembresia:
    TIPOS_VALIDOS = ["basica", "platinum", "premium", "vip"]

    def __init__(self, tabla_membresia: Membresia):
        self.tipos = []  # En memoria, sin MongoDB
        # self.tipos = list(_tipos_col.find({}, {"_id": 0}))
        self.tabla_membresia = tabla_membresia
        self._ultimo_id = max((t.get("id_tipo", 0) for t in self.tipos), default=0)

    def crear_tipo(self):
        print("\nREGISTRO DE TIPO DE MEMBRESIA")
        membresia = self.tabla_membresia.elegir_membresia()
        if not membresia:
            return

        print("Tipos disponibles: basica | platinum | premium | vip")
        tipo = input("Tipo: ").strip().lower()
        if tipo not in self.TIPOS_VALIDOS:
            print(f"Tipo invalido. Debe ser uno de: {', '.join(self.TIPOS_VALIDOS)}")
            return

        self._ultimo_id += 1
        id_tipo = self._ultimo_id
        tipo_doc = {
            "id_tipo": id_tipo,
            "id_membresia": membresia["id_membresia"],
            "tipo": tipo,
        }
        self.tipos.append(tipo_doc)
        # _tipos_col.insert_one(tipo_doc)  # Comentado: Sin MongoDB
        print("Registrado correctamente.")

    def id_seleccionado(self, id_tipo):
        try:
            id_tipo = int(id_tipo)
        except (ValueError, TypeError):
            return None
        for t in self.tipos:
            if t["id_tipo"] == id_tipo:
                return t
        return None

    def elegir_tipo(self):
        if not self.tipos:
            print("\nNo hay tipos de membresia registrados.")
            return None
        print("\nTIPOS DE MEMBRESIA DISPONIBLES")
        for i, t in enumerate(self.tipos, start=1):
            print(f"{i}. {t['tipo']}")
        opcion = input("Seleccione tipo de membresia: ").strip()
        if not opcion.isdigit():
            print("Opción inválida.")
            return None
        indice = int(opcion)
        if indice < 1 or indice > len(self.tipos):
            print("Opción fuera de rango.")
            return None
        return self.tipos[indice - 1]

    def mostrar_tipos(self):
        if not self.tipos:
            print("\nNo hay tipos de membresia registrados.")
            return
        columnas = [("ID_TIPO", 7), ("ID_MEM", 7), ("CLIENTE", 16), ("TIPO", 10)]
        filas = []
        for t in self.tipos:
            membresia = self.tabla_membresia.id_seleccionado(t["id_membresia"])
            cliente = self.tabla_membresia.usuarios.buscar_id(membresia["id_cliente"]) if membresia else None
            nombre = cliente["nombre"] if cliente else "Sin nombre"
            filas.append((t["id_tipo"], t["id_membresia"], nombre, t["tipo"]))
        tabla("TIPOS DE MEMBRESIA", columnas, filas)

class Pago:
    def __init__(self, usuarios: Usuarios, tabla_tipo_membresia: TipoMembresia):
        self.pagos = []  # En memoria, sin MongoDB
        # self.pagos = list(_pagos_col.find({}, {"_id": 0}))
        self.usuarios = usuarios
        self.tabla_tipo_membresia = tabla_tipo_membresia
        self._ultimo_id = max((p.get("id_pago", 0) for p in self.pagos), default=0)

    def crear_pago(self):
        print("\nREGISTRO DE PAGO")
        cliente = self.usuarios.usuario_elegido()
        if not cliente:
            return
        id_cliente = cliente["id_usuario"]

        tipo = self.tabla_tipo_membresia.elegir_tipo()
        if not tipo:
            return
        self._ultimo_id += 1
        id_pago = self._ultimo_id
        monto = input("Monto / Valor a pagar: ").strip()
        fecha_pago = str(date.today())
        metodo_pago  = input("Metodo de pago: ").strip()
        estado_cuenta = "pagado"

        pago_doc = {
            "id_pago": id_pago,
            "id_cliente": str(id_cliente).strip(),
            "id_tipo_membresia": tipo["id_tipo"],
            "monto": monto,
            "fecha_pago": fecha_pago,
            "metodo_pago": metodo_pago,
            "estado_cuenta": estado_cuenta,
        }
        self.pagos.append(pago_doc)
        # _pagos_col.insert_one(pago_doc)  # Comentado: Sin MongoDB
        print("Registrado correctamente.")

    def mostrar_pagos(self):
        if not self.pagos:
            print("\nNo hay pagos registrados.")
            return
        columnas = [
            ("ID_PAGO", 7),
            ("CLIENTE", 14),
            ("TIPO_MEM", 9),
            ("MONTO", 9),
            ("FECHA", 10),
            ("METODO", 10),
            ("ESTADO", 10),
        ]
        filas = []
        for p in self.pagos:
            cliente = self.usuarios.buscar_id(p["id_cliente"])
            nombre = cliente["nombre"] if cliente else "Sin nombre"
            tipo = self.tabla_tipo_membresia.id_seleccionado(p["id_tipo_membresia"])
            tipo_txt = tipo["tipo"] if tipo else "-"
            filas.append(
                (
                    p["id_pago"],
                    nombre,
                    tipo_txt,
                    p["monto"],
                    p["fecha_pago"],
                    p["metodo_pago"],
                    p["estado_cuenta"],
                )
            )
        tabla("PAGOS", columnas, filas)


class Clases:
    def __init__(self, tabla_entrenadores: Entrenadores, tabla_sede):
        self.clases = []  # En memoria, sin MongoDB
        # self.clases = list(_clases_col.find({}, {"_id": 0}))
        self.tabla_entrenadores = tabla_entrenadores
        self.tabla_sede = tabla_sede
        self.tabla_reservas = None
        self._ultimo_id = max((c.get("id_clase", 0) for c in self.clases), default=0)

    def enlazar_reservas(self, tabla_reservas):
        self.tabla_reservas = tabla_reservas

    def crear_clase(self):
        print("\nREGISTRO DE CLASE")
        entrenador = self.tabla_entrenadores.elegir_entrenador()
        if not entrenador:
            return
        sede = self.tabla_sede.elegir_sede()
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
        # _clases_col.insert_one(clase_doc)  # Comentado: Sin MongoDB
        print("Registrado correctamente.")

    def cupos_ocupados(self, id_clase):
        if not self.tabla_reservas:
            return 0
        return sum(
            1
            for r in self.tabla_reservas.reservas
            if r["id_clase"] == id_clase and r["estado_reserva"] == "reservada"
        )

    def hay_cupo_disponible(self, clase):
        cupo_total = int(clase.get("cupo_total", 0))
        cupos_libres = cupo_total - self.cupos_ocupados(clase["id_clase"])
        return cupos_libres > 0, cupos_libres

    def id_seleccionado(self, id_clase):
        try:
            id_clase = int(id_clase)
        except (ValueError, TypeError):
            return None
        for c in self.clases:
            if c["id_clase"] == id_clase:
                return c
        return None

    def elegir_clase(self):
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

    def mostrar_clases(self):
        if not self.clases:
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
        for c in self.clases:
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
        tabla("CLASES", columnas, filas)


class Reservas:
    def __init__(self, usuarios: Usuarios, tabla_clases: Clases):
        self.reservas = []  # En memoria, sin MongoDB
        # self.reservas = list(_reservas_col.find({}, {"_id": 0}))
        self.usuarios = usuarios
        self.tabla_clases = tabla_clases
        self._ultimo_id = max((r.get("id_reserva", 0) for r in self.reservas), default=0)

    def crear_reserva(self):
        print("\nREGISTRO DE RESERVA")
        usuario = self.usuarios.usuario_elegido()
        if not usuario:
            return
        id_usuario = usuario["id_usuario"]

        clase = self.tabla_clases.elegir_clase()
        if not clase:
            return
        disponible, cupos_libres = self.tabla_clases.hay_cupo_disponible(clase)
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
        # _reservas_col.insert_one(reserva)  # Comentado: Sin MongoDB

        if clase.get("id_reserva") is None:
            clase["id_reserva"] = id_reserva
            # _clases_col.update_one(  # Comentado: Sin MongoDB
            #     {"id_clase": clase["id_clase"]},
            #     {"$set": {"id_reserva": id_reserva}},
            # )

        print(f"Reserva registrada correctamente. Cupos restantes: {cupos_libres - 1}")

    def id_seleccionado(self, id_reserva):
        try:
            id_reserva = int(id_reserva)
        except (ValueError, TypeError):
            return None
        for r in self.reservas:
            if r["id_reserva"] == id_reserva:
                return r
        return None

    def elegir_reserva(self):
        if not self.reservas:
            print("\nNo hay reservas registradas.")
            return None
        print("\nRESERVAS DISPONIBLES")
        for i, r in enumerate(self.reservas, start=1):
            cliente = self.usuarios.buscar_id(r["id_cliente"])
            nombre = cliente["nombre"] if cliente else "Sin nombre"
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

    def mostrar_reservas(self):
        if not self.reservas:
            print("\nNo hay reservas registradas.")
            return
        columnas = [
            ("ID_RES", 6),
            ("CLIENTE", 16),
            ("ID_CLASE", 7),
            ("FECHA_RESERVA", 12),
            ("ESTADO", 12),
        ]
        filas = []
        for r in self.reservas:
            cliente = self.usuarios.buscar_id(r["id_cliente"])
            nombre = cliente["nombre"] if cliente else "Sin nombre"
            filas.append((r["id_reserva"], nombre, r["id_clase"], r["fecha_reserva"], r["estado_reserva"]))
        tabla("RESERVAS", columnas, filas)


class Asistencia:
    def __init__(self, tabla_reservas: Reservas):
        self.asistencias = []  # En memoria, sin MongoDB
        # self.asistencias = list(_asistencias_col.find({}, {"_id": 0}))
        self.tabla_reservas = tabla_reservas
        self._ultimo_id = max((a.get("id_asistencia", 0) for a in self.asistencias), default=0)

    def crear_asistencia(self):
        print("\nREGISTRO DE ASISTENCIA")
        usuario = self.tabla_reservas.usuarios.usuario_elegido()
        if not usuario:
            return

        reservas_usuario = [
            r for r in self.tabla_reservas.reservas if str(r["id_cliente"]) == str(usuario["id_usuario"])
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
        # _asistencias_col.insert_one(asistencia_doc)  # Comentado: Sin MongoDB
        reserva["estado_reserva"] = estado_asistencia
        # _reservas_col.update_one(  # Comentado: Sin MongoDB
        #     {"id_reserva": reserva["id_reserva"]},
        #     {"$set": {"estado_reserva": estado_asistencia}},
        # )
        print("Registrado correctamente.")

    def mostrar_asistencias(self):
        if not self.asistencias:
            print("\nNo hay asistencias registradas.")
            return
        columnas = [
            ("ID_ASIS", 7),
            ("ID_RES", 6),
            ("FECHA", 10),
            ("ESTADO", 10),
            ("HORA_ENTRADA", 11),
            ("HORA_SALIDA", 10),
        ]
        filas = [
            (
                a["id_asistencia"],
                a["id_reserva"],
                a["fecha_asistencia"],
                a["estado_asistencia"],
                a["hora_entrada"],
                a["horas_salida"],
            )
            for a in self.asistencias
        ]
        tabla("ASISTENCIAS", columnas, filas)

class Sede:
    def __init__(self):
        sedes_base = [
            {
                "id_sede": 1,
                "nombre_sede": "GYM FORTE Centro",
                "direccion": "Calle 10 #15-20",
                "telefono": "3001112233",
                "horario": "05:00-22:00",
            },
            {
                "id_sede": 2,
                "nombre_sede": "GYM FORTE Norte",
                "direccion": "Av 45 #80-12",
                "telefono": "3004445566",
                "horario": "06:00-21:00",
            },
            {
                "id_sede": 3,
                "nombre_sede": "GYM FORTE Sur",
                "direccion": "Cra 30 #12-05",
                "telefono": "3007778899",
                "horario": "05:30-21:30",
            },
        ]
        if len(sedes_base) > 0:  # Sin MongoDB
            # if _sedes_col.count_documents({}) == 0:
            #     _sedes_col.insert_many(sedes_base)
            self.sedes = sedes_base
        # self.sedes = list(_sedes_col.find({}, {"_id": 0}))

    def elegir_sede(self):
        print("\nSEDES DISPONIBLES")
        for s in self.sedes:
            print(f"{s['id_sede']}. {s['nombre_sede']} - {s['direccion']}")
        opcion = input("Seleccione sede: ").strip()
        sede = self.id_seleccionado(opcion)
        if not sede:
            print("Sede no válida.")
            return None
        return sede

    def id_seleccionado(self, id_sede):
        try:
            id_sede = int(id_sede)
        except (ValueError, TypeError):
            return None
        for s in self.sedes:
            if s["id_sede"] == id_sede:
                return s
        return None

    def mostrar_sedes(self):
        if not self.sedes:
            print("\nNo hay sedes registradas.")
            return
        columnas = [
            ("ID_SEDE", 6),
            ("NOMBRE_SEDE", 18),
            ("DIRECCION", 20),
            ("TELEFONO", 10),
            ("HORARIO", 10),
        ]
        filas = [
            (s["id_sede"], s["nombre_sede"], s["direccion"], s["telefono"], s["horario"])
            for s in self.sedes
        ]
        tabla("SEDES", columnas, filas)

if __name__ == "__main__":
    usuarios = Usuarios()
    eliminar_cliente = EliminarUsuario(usuarios)
    historial_medico = HistorialMedico(usuarios)
    estado_cliente = Cliente(usuarios)
    entrenadores = Entrenadores(usuarios)
    rutinas = Rutinas(usuarios, estado_cliente, entrenadores)
    membresia = Membresia(usuarios)
    tipo_membresia = TipoMembresia(membresia)
    pago = Pago(usuarios, tipo_membresia)
    sede = Sede()
    clases = Clases(entrenadores, sede)
    reservas = Reservas(usuarios, clases)
    clases.enlazar_reservas(reservas)
    asistencia = Asistencia(reservas)
    usuarios.enlazar_tablas(historial_medico, estado_cliente)

    while True:
        print("\nGYM FORTE")
        print("1. Registrar usuario")
        print("2. Registrar membresia")
        print("3. Registrar tipo de membresia")
        print("4. Registrar pago")
        print("5. Registrar clase")
        print("6. Registrar reserva")
        print("7. Registrar asistencia")
        print("8. Registrar rutina")
        print("9. Ver entrenadores disponibles")
        print("10. Ver sedes disponibles")
        print("11. Ver usuarios")
        print("12. Ver historiales medicos")
        print("13. Ver estados de clientes")
        print("14. Ver rutinas")
        print("15. Ver membresias")
        print("16. Ver tipos de membresia")
        print("17. Ver pagos")
        print("18. Ver clases")
        print("19. Ver reservas")
        print("20. Ver asistencias")
        print("21. Eliminar usuario")
        print("22. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            usuarios.crear_usuario()
        elif opcion == "2":
            membresia.crear_membresia()
        elif opcion == "3":
            tipo_membresia.crear_tipo()
        elif opcion == "4":
            pago.crear_pago()
        elif opcion == "5":
            clases.crear_clase()
        elif opcion == "6":
            reservas.crear_reserva()
        elif opcion == "7":
            asistencia.crear_asistencia()
        elif opcion == "8":
            rutinas.crear_rutina()
        elif opcion == "9":
            entrenadores.mostrar_entrenadores()
        elif opcion == "10":
            sede.mostrar_sedes()
        elif opcion == "11":
            usuarios.mostrar_usuarios()
        elif opcion == "12":
            historial_medico.mostrar_historiales()
        elif opcion == "13":
            estado_cliente.mostrar_estados_clientes()
        elif opcion == "14":
            rutinas.mostrar_rutinas()
        elif opcion == "15":
            membresia.mostrar_membresias()
        elif opcion == "16":
            tipo_membresia.mostrar_tipos()
        elif opcion == "17":
            pago.mostrar_pagos()
        elif opcion == "18":
            clases.mostrar_clases()
        elif opcion == "19":
            reservas.mostrar_reservas()
        elif opcion == "20":
            asistencia.mostrar_asistencias()
        elif opcion == "21":
            eliminar_cliente.eliminar_usuario()
        elif opcion == "22":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
