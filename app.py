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

from auth import (
    inicializar_auth,
    login,
    logout,
    validar_token,
    registrar_credenciales_usuario,
)

import json
import os

app = Flask(__name__, static_folder='interfaz', static_url_path='')
CORS(app)

inicializar_auth()

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
            'lesiones': u.lesiones,
            'plan': getattr(u, 'plan', 'Premium')
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
                nuevo.plan = d.get('plan', 'Premium')
                usuarios.usuarios.append(nuevo)

def get_token_from_request():
    """Extrae el token del header Authorization o del query param ?token="""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    return request.args.get('token', '')

def requiere_auth(rol=None):
    """
    Decorador que protege una ruta.
    rol='admin'   → solo admins
    rol='usuario' → solo usuarios miembros
    rol=None      → cualquier sesión válida
    """
    def decorator(fn):
        from functools import wraps
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token  = get_token_from_request()
            sesion = validar_token(token)
            if not sesion:
                return jsonify({'error': 'No autenticado'}), 401
            if rol and sesion['rol'] != rol:
                return jsonify({'error': 'Sin permisos'}), 403
            request.sesion = sesion
            return fn(*args, **kwargs)
        return wrapper
    return decorator

cargar_usuarios()

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
        nuevo.plan = "Premium"
        usuarios.usuarios.append(nuevo)
        registrar_credenciales_usuario(nuevo.id_usuario, correo, "password123")
    
    guardar_usuarios()

@app.route('/')
def index():
    return send_from_directory('interfaz/login', 'login.html')

@app.route('/<filename>')
def static_files(filename):
    return send_from_directory('interfaz/login', filename)

@app.route('/admin/admin.html')
def admin_page():
    return send_from_directory('interfaz/admin', 'admin.html')

@app.route('/admin/<filename>')
def admin_static(filename):
    return send_from_directory('interfaz/admin', filename)

@app.route('/usuario/perfil.html')
def user_page():
    return send_from_directory('interfaz/usuario', 'perfil.html')

@app.route('/usuario/<filename>')
def user_static(filename):
    return send_from_directory('interfaz/usuario', filename)

# rutas de autenticación

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Cuerpo vacío'}), 400
    correo   = data.get('correo', '').strip()
    password = data.get('password', '').strip()
    if not correo or not password:
        return jsonify({'error': 'Correo y contraseña requeridos'}), 400
    resultado = login(correo, password)
    if resultado:
        return jsonify(resultado), 200
    return jsonify({'error': 'Credenciales incorrectas'}), 401

@app.route('/api/logout', methods=['POST'])
def api_logout():
    token = get_token_from_request()
    logout(token)
    return jsonify({'ok': True})

@app.route('/api/me', methods=['GET'])
@requiere_auth()
def api_me():
    return jsonify(request.sesion)

# Stats para dashboard
@app.route('/api/dashboard/stats', methods=['GET'])
@requiere_auth(rol='admin')  # ── NUEVO
def get_stats():
    return jsonify({
        'miembros_activos': len(usuarios.usuarios),
        'ingresos_mes': 84300,
        'clases_hoy': 14,
        'ocupacion_actual': 68
    })

# Listar miembros (primeros 10)
@app.route('/api/miembros', methods=['GET'])
@requiere_auth(rol='admin')  # ── NUEVO
def get_miembros():
    miembros = []
    for u in usuarios.usuarios[:10]:
        miembros.append({
            'id': u.id_usuario,
            'nombre': f"{u.nombre} {u.apellido}",
            'plan': getattr(u, 'plan', 'Premium'),
            'vence': '2026-08-15',
            'estado': 'Activo'
        })
    return jsonify(miembros)

# Listar TODOS los miembros
@app.route('/api/miembros-todos', methods=['GET'])
@requiere_auth(rol='admin')  # ── NUEVO
def get_miembros_todos():
    miembros = []
    for u in usuarios.usuarios:
        miembros.append({
            'id': u.id_usuario,
            'nombre': f"{u.nombre} {u.apellido}",
            'correo': u.correo_electronico,
            'telefono': u.numero_celular,
            'plan': getattr(u, 'plan', 'Premium'),
            'vence': '2026-08-15',
            'estado': 'Activo'
        })
    return jsonify(miembros)

# perfil del usuario autenticado

@app.route('/api/usuario/perfil', methods=['GET'])
@requiere_auth(rol='usuario')
def get_mi_perfil():
    user_id = request.sesion['user_id']
    for u in usuarios.usuarios:
        if u.id_usuario == user_id:
            return jsonify({
                'id':               u.id_usuario,
                'nombre':           u.nombre,
                'apellido':         u.apellido,
                'correo':           u.correo_electronico,
                'cedula':           u.cedula,
                'telefono':         u.numero_celular,
                'fecha_nacimiento': u.fecha_nacimiento,
                'direccion':        u.direccion,
                'peso':             u.peso,
                'estatura':         u.estatura,
                'tipo_sangre':      u.tipo_sangre,
                'lesiones':         u.lesiones,
                'plan':             getattr(u, 'plan', 'Premium'),
            })
    return jsonify({'error': 'Usuario no encontrado'}), 404

@app.route('/api/usuario/perfil', methods=['PUT'])
@requiere_auth(rol='usuario')
def actualizar_mi_perfil():
    """Actualizar solo los campos editables del perfil del usuario actual.
    Campos NO editables: nombre, apellido, cedula, tipo_sangre, plan, estatura.
    """
    user_id = request.sesion['user_id']
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Sin datos'}), 400

    for u in usuarios.usuarios:
        if u.id_usuario == user_id:
            # Solo actualizar campos permitidos que vengan en el payload
            if 'correo' in data and data['correo']:
                correo = data['correo'].strip()
                correo = correo.replace('@gmail.cm','@gmail.com').replace('@hotmail.cm','@hotmail.com')
                u.correo_electronico = correo
                # Actualizar también en credenciales.json
                from auth import _cargar_credenciales, _guardar_credenciales
                creds = _cargar_credenciales()
                for cu in creds['usuarios']:
                    if cu['id'] == user_id:
                        cu['correo'] = correo.lower()
                        break
                _guardar_credenciales(creds)
            if 'telefono' in data and data['telefono']:
                u.numero_celular = data['telefono']
            if 'direccion' in data and data['direccion']:
                u.direccion = data['direccion']
            if 'peso' in data and data['peso'] is not None and data['peso'] != '':
                u.peso = data['peso']
            # lesiones puede ser string vacío (borrar)
            if 'lesiones' in data:
                u.lesiones = data['lesiones']

            guardar_usuarios()
            return jsonify({'ok': True, 'mensaje': 'Perfil actualizado correctamente'}), 200

    return jsonify({'error': 'Usuario no encontrado'}), 404

# Crear usuario
@app.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    usuarios._ultimo_id += 1
    
    nuevo = type('Usuario', (), {})()
    nuevo.id_usuario = usuarios._ultimo_id
    nuevo.nombre = data.get('nombre', '')
    nuevo.apellido = data.get('apellido', '')
    correo_raw = data.get('correo_electronico', '').strip()
    # Corregir dominios mal escritos comunes
    correo_raw = correo_raw.replace('@gmail.cm', '@gmail.com').replace('@hotmail.cm', '@hotmail.com').replace('@yahoo.cm', '@yahoo.com')
    nuevo.correo_electronico = correo_raw
    nuevo.cedula = data.get('cedula', '')
    nuevo.numero_celular = data.get('numero_celular', '')
    nuevo.fecha_nacimiento = data.get('fecha_nacimiento', '')
    nuevo.direccion = data.get('direccion', '')
    nuevo.peso = data.get('peso')
    nuevo.estatura = data.get('estatura')
    nuevo.tipo_sangre = data.get('tipo_sangre')
    nuevo.lesiones = data.get('lesiones')
    nuevo.plan = data.get('plan', 'Premium')

    usuarios.usuarios.append(nuevo)
    guardar_usuarios()

    # guardar credenciales
    password = data.get('password', 'gym123') # Contraseña por defecto si no se proporciona o sea creada desde admin
    registrar_credenciales_usuario(
        nuevo.id_usuario,
        nuevo.correo_electronico,
        password
    )

    return jsonify({'success': True, 'id': nuevo.id_usuario}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)