from datetime import date
from components.Usuarios.usuarios import Usuarios

class EliminarUsuario:
    def __init__(self, usuarios: Usuarios):
        self.eliminaciones = []  # En memoria, sin MongoDB
        # self.eliminaciones = list(_eliminaciones_col.find({}, {"_id": 0}))
        self.usuarios = usuarios
    def eliminar_usuario(self):
        print("\nELIMINAR USUARIO")
        usuario = self.usuarios.usuario_elegido()
        if not usuario:
            return
        confirmacion = input(
            f"¿Seguro que desea eliminar a '{usuario['nombre']} {usuario['apellido']}'? (si/no): "
        ).strip().lower()
        if confirmacion == "no":
            print("Operación cancelada. Regresando al menú principal...")
            return
        if confirmacion != "si":
            print("Respuesta inválida. Regresando al menú principal...")
            return
        registro = {
            "id_usuario" : usuario["id_usuario"],
            "nombre" : usuario["nombre"],
            "apellido" : usuario["apellido"],
            "fecha_baja": str(date.today()),
        }
        self.eliminaciones.append(registro)
        # _eliminaciones_col.insert_one(registro)  # Comentado: Sin MongoDB
        self.usuarios.usuarios.remove(usuario)
        # _usuarios_col.delete_one({"id_usuario": usuario["id_usuario"]})  # Comentado: Sin MongoDB
        print(f"\nUsuario '{usuario['nombre']} {usuario['apellido']}' eliminado correctamente.")

    def mostrar_eliminaciones(self):
        if not self.eliminaciones:
            print("\nNo hay registros de eliminaciones.")
            return
        print("\nHISTORIAL DE BAJAS DE USUARIOS")
        for e in self.eliminaciones:
            print(f"[{e['id_usuario']}] {e['nombre']} {e['apellido']}|"
                  f"Fecha baja: {e['fecha_baja']}")
