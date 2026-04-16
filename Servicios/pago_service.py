from datetime import date

class PagoService:
    """Servicio para gestionar pagos"""
    
    def __init__(self):
        self.pagos = []
        self._ultimo_id = 0
    
    def crear_pago(self, usuarios, tabla_tipo_membresia):
        """Crea un nuevo registro de pago"""
        print("\nREGISTRO DE PAGO")
        cliente = usuarios.usuario_elegido()
        if not cliente:
            return
        id_cliente = cliente.id_usuario

        tipo = tabla_tipo_membresia.elegir_tipo()
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
        print("Registrado correctamente.")
        return pago_doc
    
    def mostrar_pagos(self, usuarios, tabla_tipo_membresia, tabla_func):
        """Muestra todos los pagos registrados"""
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
            cliente = usuarios.buscar_id(p["id_cliente"])
            nombre = cliente.nombre if cliente else "Sin nombre"
            tipo = tabla_tipo_membresia.id_seleccionado(p["id_tipo_membresia"])
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
        tabla_func("PAGOS", columnas, filas)
