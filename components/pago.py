from Servicios.pago_service import PagoService


class Pago:
    """Clase delegadora que utiliza PagoService"""
    
    def __init__(self, usuarios, tabla_tipo_membresia):
        self.service = PagoService()
        self.usuarios = usuarios
        self.tabla_tipo_membresia = tabla_tipo_membresia
    
    def crear_pago(self):
        """Delega a PagoService"""
        return self.service.crear_pago(self.usuarios, self.tabla_tipo_membresia)
    
    def mostrar_pagos(self, tabla_func):
        """Delega a PagoService"""
        return self.service.mostrar_pagos(self.usuarios, self.tabla_tipo_membresia, tabla_func)
