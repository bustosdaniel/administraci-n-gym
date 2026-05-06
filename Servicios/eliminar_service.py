from datetime import date
from components.eliminar import Eliminar

class EliminarService:
    """Servicio para gestionar eliminación de usuarios"""
    
    def __init__(self, usuarios_service):
        self.eliminaciones = []
        self.usuarios_service = usuarios_service

    def eliminar_usuario(self):
        """Elimina un usuario después de confirmar"""
        print("\nELIMINAR USUARIO")
        usuario = self.usuarios_service.usuario_elegido()
        if not usuario:
            return
        
        confirmacion = input(
            f"¿Seguro que desea eliminar a '{usuario.nombre} {usuario.apellido}'? (si/no): "
        ).strip().lower()
        
        if confirmacion == "no":
            print("Operación cancelada. Regresando al menú principal...")
            return
        
        if confirmacion != "si":
            print("Respuesta inválida. Regresando al menú principal...")
            return
        
        # Crear registro de eliminación
        eliminar = Eliminar(
            id_usuario=usuario.id_usuario,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            fecha_baja=str(date.today())
        )
        
        self.eliminaciones.append(eliminar)
        
        # Remover usuario de la lista
        self.usuarios_service.usuarios.remove(usuario)
        
        print(f"\nUsuario '{usuario.nombre} {usuario.apellido}' eliminado correctamente.")

    def mostrar_eliminaciones(self):
        """Muestra el historial de eliminaciones"""
        if not self.eliminaciones:
            print("\nNo hay registros de eliminaciones.")
            return
        
        print("\nHISTORIAL DE BAJAS DE USUARIOS")
        for e in self.eliminaciones:
            print(f"[{e.id_usuario}] {e.nombre} {e.apellido} | "
                  f"Fecha baja: {e.fecha_baja}")
