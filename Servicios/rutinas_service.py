class RutinasService:
    """Servicio para gestionar rutinas de entrenamiento"""
    
    def __init__(self):
        self.rutinas = []
        self._ultimo_id_rutina = 0
    
    def crear_rutina(self, usuarios, tabla_cliente, tabla_entrenadores):
        """Crea una nueva rutina de entrenamiento"""
        print("\nREGISTRO DE RUTINA")
        cliente = usuarios.usuario_elegido()
        if not cliente:
            return
        id_cliente = cliente.id_usuario

        entrenador = tabla_entrenadores.elegir_entrenador()
        if not entrenador:
            return

        estado_cliente = tabla_cliente.obtener_idusuario(id_cliente)
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
        print("Registrado correctamente.")
        return rutina
    
    def mostrar_rutinas(self, usuarios, tabla_entrenadores, tabla_func):
        """Muestra todas las rutinas registradas"""
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
            cliente = usuarios.buscar_id(r["id_cliente"])
            nombre_cliente = cliente.nombre if cliente else "Sin nombre"
            entrenador = tabla_entrenadores.id_seleccionado_entrenador(r["id_entrenador"])
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
        tabla_func("RUTINAS", columnas, filas)
