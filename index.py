import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date
from components.usuarios import Usuarios
from components.eliminarUsuario import EliminarUsuario
from components.historial_medico import HistorialMedicoManager
from components.cliente import Cliente
from components.entrenadores import Entrenadores
from components.rutinas import Rutinas
from components.membresia import Membresia
from components.tipo_membresia import TipoMembresia
from components.pago import Pago
from components.clases import Clases
from components.reservas import Reservas
from components.asistencia import Asistencia
from components.sede import Sede


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


if __name__ == "__main__":
    usuarios = Usuarios()
    eliminar_cliente = EliminarUsuario(usuarios)
    historial_medico = HistorialMedicoManager(usuarios)
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
        print("22. Ver eliminaciones")
        print("23. Salir")
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
            sede.mostrar_sedes(tabla)
        elif opcion == "11":
            usuarios.mostrar_usuarios()
        elif opcion == "12":
            historial_medico.mostrar_historiales()
        elif opcion == "13":
            estado_cliente.mostrar_estados_clientes()
        elif opcion == "14":
            rutinas.mostrar_rutinas(tabla)
        elif opcion == "15":
            membresia.mostrar_membresias(tabla)
        elif opcion == "16":
            tipo_membresia.mostrar_tipos(tabla)
        elif opcion == "17":
            pago.mostrar_pagos(tabla)
        elif opcion == "18":
            clases.mostrar_clases(tabla)
        elif opcion == "19":
            reservas.mostrar_reservas(tabla)
        elif opcion == "20":
            asistencia.mostrar_asistencias(tabla)
        elif opcion == "21":
            eliminar_cliente.eliminar_usuario()
        elif opcion == "22":
            eliminar_cliente.mostrar_eliminaciones()
        elif opcion == "23":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
