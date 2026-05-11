"""
auth.py — Módulo de autenticación para GYM FORTE
Maneja login de administradores y usuarios miembros.
Coloca este archivo en la raíz del proyecto (junto a app.py).
"""

import json
import hashlib
import os
from datetime import datetime, timedelta
import secrets

# ─────────────────────────────────────────────
# Archivo donde se guardan las credenciales
# ─────────────────────────────────────────────
CREDENCIALES_FILE = 'credenciales.json'

# ─────────────────────────────────────────────
# Sesiones en memoria  { token: { user_id, rol, expires } }
# ─────────────────────────────────────────────
sesiones_activas = {}


# ══════════════════════════════════════════════
# UTILIDADES
# ══════════════════════════════════════════════

def _hash_password(password: str) -> str:
    """SHA-256 simple. Para producción usa bcrypt."""
    return hashlib.sha256(password.encode()).hexdigest()


def _generar_token() -> str:
    return secrets.token_hex(32)


def _cargar_credenciales() -> dict:
    if not os.path.exists(CREDENCIALES_FILE):
        return {"admins": [], "usuarios": []}
    with open(CREDENCIALES_FILE, 'r') as f:
        return json.load(f)


def _guardar_credenciales(datos: dict):
    with open(CREDENCIALES_FILE, 'w') as f:
        json.dump(datos, f, indent=2)


# ══════════════════════════════════════════════
# INICIALIZACIÓN — crea admin por defecto
# ══════════════════════════════════════════════

def inicializar_auth():
    """
    Crea credenciales.json con el admin por defecto si no existe.
    Admin por defecto:  correo: admin@gymforte.com  |  clave: admin123
    """
    if os.path.exists(CREDENCIALES_FILE):
        return  # ya existe, no sobreescribir

    datos = {
        "admins": [
            {
                "id": 0,
                "nombre": "Admin",
                "correo": "admin@gymforte.com",
                "password_hash": _hash_password("admin123"),
                "rol": "admin"
            }
        ],
        "usuarios": []   # se populan al registrar/crear miembros
    }
    _guardar_credenciales(datos)
    print("[AUTH] credenciales.json creado con admin por defecto.")


# ══════════════════════════════════════════════
# REGISTRO de credenciales para un miembro nuevo
# ══════════════════════════════════════════════

def registrar_credenciales_usuario(user_id: int, correo: str, password: str) -> bool:
    """
    Llamado desde app.py al crear un usuario nuevo.
    Devuelve False si el correo ya existe.
    """
    datos = _cargar_credenciales()

    # Verificar que no exista
    for u in datos["usuarios"]:
        if u["correo"].lower() == correo.lower():
            return False

    datos["usuarios"].append({
        "id": user_id,
        "correo": correo.lower(),
        "password_hash": _hash_password(password),
        "rol": "usuario"
    })
    _guardar_credenciales(datos)
    return True


def actualizar_password_usuario(correo: str, nueva_password: str) -> bool:
    """Actualiza la contraseña de un usuario existente."""
    datos = _cargar_credenciales()
    for u in datos["usuarios"]:
        if u["correo"].lower() == correo.lower():
            u["password_hash"] = _hash_password(nueva_password)
            _guardar_credenciales(datos)
            return True
    return False


# ══════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════

def login(correo: str, password: str):
    """
    Intenta autenticar por correo + contraseña.
    Busca primero en admins, luego en usuarios.

    Retorna:
        { "token": str, "rol": "admin"|"usuario", "user_id": int, "nombre": str }
        o None si falla.
    """
    datos = _cargar_credenciales()
    pw_hash = _hash_password(password)
    correo = correo.strip().lower()

    # ── 1. Buscar en admins
    for a in datos["admins"]:
        if a["correo"].lower() == correo and a["password_hash"] == pw_hash:
            token = _generar_token()
            sesiones_activas[token] = {
                "user_id": a["id"],
                "rol": "admin",
                "nombre": a["nombre"],
                "expires": (datetime.utcnow() + timedelta(hours=8)).isoformat()
            }
            return {"token": token, "rol": "admin", "user_id": a["id"], "nombre": a["nombre"]}

    # ── 2. Buscar en usuarios miembros
    for u in datos["usuarios"]:
        if u["correo"].lower() == correo and u["password_hash"] == pw_hash:
            token = _generar_token()
            sesiones_activas[token] = {
                "user_id": u["id"],
                "rol": "usuario",
                "nombre": u.get("nombre", correo),
                "expires": (datetime.utcnow() + timedelta(hours=8)).isoformat()
            }
            return {"token": token, "rol": "usuario", "user_id": u["id"], "nombre": u.get("nombre", correo)}

    return None


# ══════════════════════════════════════════════
# VALIDACIÓN DE SESIÓN
# ══════════════════════════════════════════════

def validar_token(token: str):
    """
    Devuelve la sesión si el token es válido y no expiró, o None.
    """
    if not token or token not in sesiones_activas:
        return None
    sesion = sesiones_activas[token]
    if datetime.utcnow() > datetime.fromisoformat(sesion["expires"]):
        del sesiones_activas[token]
        return None
    return sesion


def logout(token: str):
    """Elimina el token de sesión."""
    sesiones_activas.pop(token, None)