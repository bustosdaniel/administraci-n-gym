# Administración de Gimnasio

Sistema de gestión para administración de gimnasios desarrollado en Python puro con interfaz de consola.

## Descripción

Es una aplicación de escritorio que permite gestionar integralmente un gimnasio. El sistema maneja el ciclo completo de un miembro: desde su registro inicial, creación de historiales médicos, asignación de entrenadores y rutinas personalizadas, gestión de membresías y pagos, hasta el seguimiento de asistencia a clases. También administra las sedes del gimnasio, los entrenadores disponibles, las clases grupales programadas, y permite reservar lugares en clases específicas. Cada usuario tiene un historial médico que registra su peso, estatura, tipo de sangre, lesiones previas e IMC para un seguimiento personalizado del entrenamiento.

## Estructura del Proyecto

components/
- usuarios.py: Gestión de registro y búsqueda de miembros
- historial_medico.py: Datos médicos de cada usuario
- cliente.py: Estado de membresía y objetivo de entrenamiento
- entrenadores.py: Registro de entrenadores disponibles
- rutinas.py: Creación y asignación de rutinas personalizadas
- clases.py: Clases grupales programadas
- reservas.py: Sistema de reserva de lugares en clases
- asistencia.py: Registro de asistencia a clases
- membresia.py y tipo_membresia.py: Tipos y gestión de membresías
- pago.py: Registro de pagos y transacciones
- sede.py: Múltiples sedes del gimnasio
- eliminarUsuario.py: Eliminación de usuarios

Servicios/
- usuarios_service.py: Lógica de registro, búsqueda y gestión de miembros
- historial_medico_service.py: Creación y actualización de historiales médicos
- cliente_service.py: Gestión de estado de membresía y objetivos de entrenamiento
- entrenadores_service.py: Almacenamiento y asignación de entrenadores
- rutinas_service.py: Creación y asignación de rutinas personalizadas según objetivos
- clases_service.py: Gestión de clases grupales, horarios y capacidad
- reservas_service.py: Control de reservas y disponibilidad de lugares
- asistencia_service.py: Registro de asistencia de usuarios a clases
- membresia_service.py: Gestión de membresías activas por usuario
- tipo_membresia_service.py: Definición de tipos de membresía y beneficios
- pago_service.py: Registro de transacciones y seguimiento de pagos
- sede_service.py: Múltiples sedes del gimnasio con información de ubicación
- eliminar_service.py: Control de eliminación de usuarios y registro de bajas

## Funcionamiento

El programa inicia con un menú principal que ofrece 22 opciones. El usuario puede registrarse, crear su historial médico, seleccionar un entrenador, recibir una rutina personalizada, elegir un tipo de membresía, realizar pagos, reservarse en clases, y registrar su asistencia. Los datos se mantienen en memoria durante la ejecución.
