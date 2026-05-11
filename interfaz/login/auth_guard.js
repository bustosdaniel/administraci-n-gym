/* ═══════════════════════════════════════════════════════
   auth_guard.js — GYM FORTE
   Incluye este script al inicio de admin.html y perfil.html
   para proteger las páginas de accesos no autenticados.

   Uso en admin.html:
     <script src="../login/auth_guard.js" data-rol="admin"></script>

   Uso en perfil.html:
     <script src="../login/auth_guard.js" data-rol="usuario"></script>
   ═══════════════════════════════════════════════════════ */

(function () {
  const API = '/api';

  /* ── Leer sesión del sessionStorage ── */
  const token = sessionStorage.getItem('gym_token');
  const rol = sessionStorage.getItem('gym_rol');
  const nombre = sessionStorage.getItem('gym_nombre');
  const user_id = sessionStorage.getItem('gym_user_id');

  /* ── Rol requerido por esta página ── */
  const scriptTag = document.currentScript;
  const rolRequerido = scriptTag ? scriptTag.getAttribute('data-rol') : null;

  /* ── Sin sesión → login ── */
  if (!token) {
    redirigirLogin();
    return;
  }

  /* ── Rol incorrecto → login ── */
  if (rolRequerido && rol !== rolRequerido) {
    redirigirLogin('Sin permisos para esta página.');
    return;
  }

  /* ── Verificar token contra el servidor (asíncrono) ── */
  fetch(`${API}/me`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
    .then(res => {
      if (!res.ok) {
        limpiarSesion();
        redirigirLogin('Tu sesión ha expirado. Inicia sesión de nuevo.');
      }
      // Si ok → no hacemos nada, la página carga normalmente
    })
    .catch(() => {
      // Sin conexión: dejamos pasar (funcionamiento offline básico)
      console.warn('[AuthGuard] No se pudo verificar la sesión con el servidor.');
    });

  /* ── Exponer datos de sesión globalmente ── */
  window.GYM_SESSION = { token, rol, nombre, user_id };

  /* ── Función de logout global ── */
  window.gymLogout = async function () {
    try {
      await fetch(`${API}/logout`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
    } catch (_) { }
    limpiarSesion();
    redirigirLogin();
  };

  /* ── Inyectar token en todas las peticiones fetch ──
     Monkey-patch de fetch para añadir el header automáticamente
     en llamadas a /api/* sin que tengas que cambiarlo en cada archivo.
  */
  const _originalFetch = window.fetch.bind(window);
  window.fetch = function (url, options = {}) {
    if (typeof url === 'string' && url.startsWith('/api')) {
      options.headers = Object.assign(
        { 'Authorization': `Bearer ${token}` },
        options.headers || {}
      );
    }
    return _originalFetch(url, options);
  };

  /* ── Helpers ── */
  function limpiarSesion() {
    ['gym_token', 'gym_rol', 'gym_user_id', 'gym_nombre'].forEach(k =>
      sessionStorage.removeItem(k)
    );
  }

  function redirigirLogin(msg) {
    if (msg) sessionStorage.setItem('gym_login_msg', msg);
    window.location.href = '../login/login.html';
  }
})();