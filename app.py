from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from components.usuarios import Usuarios
from components.entrenadores import Entrenadores
from components.clases import Clases
from components.reservas import Reservas
from components.asistencia import Asistencia
from components.clientes import Cliente
from components.rutinas import Rutinas
from components.sede import Sede
import json
import os

app = Flask(__name__, static_folder='interfaz', static_url_path='')
CORS(app)

# Inicializar
usuarios = Usuarios()
estado_cliente = Cliente(usuarios)
entrenadores = Entrenadores(usuarios)
sede = Sede()
clases_obj = Clases(entrenadores, sede)
reservas = Reservas(usuarios, clases_obj)
asistencia = Asistencia(reservas)

ARCHIVO_USUARIOS = 'usuarios_data.json'

def guardar_usuarios():
    """Guardar usuarios en JSON"""
    datos = []
    for u in usuarios.usuarios:
        datos.append({
            'id_usuario': u.id_usuario,
            'nombre': u.nombre,
            'apellido': u.apellido,
            'correo_electronico': u.correo_electronico,
            'cedula': u.cedula,
            'numero_celular': u.numero_celular,
            'fecha_nacimiento': u.fecha_nacimiento,
            'direccion': u.direccion,
            'peso': u.peso,
            'estatura': u.estatura,
            'tipo_sangre': u.tipo_sangre,
            'lesiones': u.lesiones
        })
    with open(ARCHIVO_USUARIOS, 'w') as f:
        json.dump(datos, f, indent=2)

def cargar_usuarios():
    """Cargar usuarios desde JSON si existe"""
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, 'r') as f:
            datos = json.load(f)
            for d in datos:
                usuarios._ultimo_id = max(usuarios._ultimo_id, d['id_usuario'])
                nuevo = type('Usuario', (), {})()
                nuevo.id_usuario = d['id_usuario']
                nuevo.nombre = d['nombre']
                nuevo.apellido = d['apellido']
                nuevo.correo_electronico = d['correo_electronico']
                nuevo.cedula = d['cedula']
                nuevo.numero_celular = d['numero_celular']
                nuevo.fecha_nacimiento = d['fecha_nacimiento']
                nuevo.direccion = d['direccion']
                nuevo.peso = d.get('peso')
                nuevo.estatura = d.get('estatura')
                nuevo.tipo_sangre = d.get('tipo_sangre')
                nuevo.lesiones = d.get('lesiones')
                usuarios.usuarios.append(nuevo)

# Cargar datos al iniciar
cargar_usuarios()

# Si no hay datos, crear demo
if len(usuarios.usuarios) == 0:
    datos_demo = [
        ("Marco", "Ruiz", "marco@gmail.com", "123456789", "+34666111111", "Calle 1, 10"),
        ("Sofía", "López", "sofia@gmail.com", "987654321", "+34666222222", "Calle 2, 20"),
        ("Diego", "Mora", "diego@gmail.com", "555666777", "+34666333333", "Calle 3, 30"),
        ("Ana", "Linares", "ana@gmail.com", "444333222", "+34666444444", "Calle 4, 40"),
    ]
    
    for nombre, apellido, correo, cedula, telefono, direccion in datos_demo:
        usuarios._ultimo_id += 1
        nuevo = type('Usuario', (), {})()
        nuevo.id_usuario = usuarios._ultimo_id
        nuevo.nombre = nombre
        nuevo.apellido = apellido
        nuevo.correo_electronico = correo
        nuevo.cedula = cedula
        nuevo.numero_celular = telefono
        nuevo.fecha_nacimiento = ""
        nuevo.direccion = direccion
        nuevo.peso = None
        nuevo.estatura = None
        nuevo.tipo_sangre = None
        nuevo.lesiones = None
        usuarios.usuarios.append(nuevo)
    
    guardar_usuarios()

# Servir HTML
@app.route('/')
def index():
    return send_from_directory('interfaz', 'index.html')

# Stats para dashboard
@app.route('/api/dashboard/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'miembros_activos': len(usuarios.usuarios),
        'ingresos_mes': 84300,
        'clases_hoy': 14,
        'ocupacion_actual': 68
    })

# Listar miembros
@app.route('/api/miembros', methods=['GET'])
def get_miembros():
    miembros = []
    for u in usuarios.usuarios[:10]:
        miembros.append({
            'id': u.id_usuario,
            'nombre': f"{u.nombre} {u.apellido}",
            'plan': 'Premium',
            'vence': '2026-08-15',
            'estado': 'Activo'
        })
    return jsonify(miembros)

# Crear usuario
@app.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    usuarios._ultimo_id += 1
    
    nuevo = type('Usuario', (), {})()
    nuevo.id_usuario = usuarios._ultimo_id
    nuevo.nombre = data.get('nombre', '')
    nuevo.apellido = data.get('apellido', '')
    nuevo.correo_electronico = data.get('correo_electronico', '')
    nuevo.cedula = data.get('cedula', '')
    nuevo.numero_celular = data.get('numero_celular', '')
    nuevo.fecha_nacimiento = data.get('fecha_nacimiento', '')
    nuevo.direccion = data.get('direccion', '')
    nuevo.peso = data.get('peso')
    nuevo.estatura = data.get('estatura')
    nuevo.tipo_sangre = data.get('tipo_sangre')
    nuevo.lesiones = data.get('lesiones')
    
    usuarios.usuarios.append(nuevo)
    guardar_usuarios()  # Guardar en JSON
    
    return jsonify({'success': True, 'id': nuevo.id_usuario}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
