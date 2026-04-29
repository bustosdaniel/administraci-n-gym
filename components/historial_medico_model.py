class HistorialMedico:
    """Modelo de un historial médico de un usuario"""
    
    def __init__(self, id_historial_med, id_cliente, peso, estatura, 
                 tipo_sangre, lesiones, fecha_ingreso="pendiente", imc="pendiente"):
        self.id_historial_med = id_historial_med
        self.id_cliente = str(id_cliente).strip()
        self.fecha_ingreso = fecha_ingreso
        self.peso = peso
        self.estatura = estatura
        self.tipo_sangre = tipo_sangre
        self.lesiones = lesiones
        self.imc = imc

    def __repr__(self):
        return f"HistorialMedico(id={self.id_historial_med}, cliente={self.id_cliente})"

    def get_datos(self):
        """Retorna los datos del historial como diccionario"""
        return {
            "id_historial_med": self.id_historial_med,
            "id_cliente": self.id_cliente,
            "fecha_ingreso": self.fecha_ingreso,
            "peso": self.peso,
            "estatura": self.estatura,
            "tipo_sangre": self.tipo_sangre,
            "lesiones": self.lesiones,
            "imc": self.imc
        }

    def actualizar_fecha_ingreso(self, fecha_ingreso):
        """Actualiza la fecha de ingreso del historial"""
        self.fecha_ingreso = str(fecha_ingreso).strip()
