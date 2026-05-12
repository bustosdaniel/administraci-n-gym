const meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];

// ── Fecha topbar ──────────────────────────────────────
const _d = new Date();
const dias = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
document.getElementById('dateDisplay').textContent =
  `${dias[_d.getDay()]}, ${_d.getDate()} ${meses[_d.getMonth()]} ${_d.getFullYear()}`;

// ══════════════════════════════════════════════════════
// HELPERS
// ══════════════════════════════════════════════════════

function setText(id, valor) {
  const el = document.getElementById(id);
  if (el) el.textContent = (valor !== null && valor !== undefined && valor !== '') ? valor : '—';
}

function setHtml(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

function show(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = '';
}

function hide(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = 'none';
}

function formatFecha(fechaStr) {
  if (!fechaStr) return '—';
  const partes = fechaStr.split('-');
  if (partes.length !== 3) return fechaStr;
  const [y, m, day] = partes;
  return `${parseInt(day)} ${meses[parseInt(m) - 1]} ${y}`;
}

function getPrecio(plan) {
  const p = (plan || '').toLowerCase().trim();
  if (p === 'básico' || p === 'basico') return '$450 / mes';
  if (p === 'elite') return '$1,200 / mes';
  return '$850 / mes';
}

function getClasePlan(plan) {
  const p = (plan || '').toLowerCase().trim();
  if (p === 'básico' || p === 'basico') return 'basic';
  if (p === 'elite') return 'elite';
  return 'premium';
}

function aplicarTema(plan) {
  const root = document.documentElement;
  root.classList.remove('plan-basico', 'plan-premium', 'plan-elite');
  const p = (plan || '').toLowerCase().trim();
  if (p === 'básico' || p === 'basico') root.classList.add('plan-basico');
  else if (p === 'elite') root.classList.add('plan-elite');
  else root.classList.add('plan-premium');
}

// ══════════════════════════════════════════════════════
// CARGAR PERFIL
// ══════════════════════════════════════════════════════

async function cargarPerfil() {
  const token = sessionStorage.getItem('gym_token') || localStorage.getItem('gym_token');
  if (!token) {
    console.warn('No hay token de sesión');
    return;
  }

  try {
    const res = await fetch('/api/usuario/perfil', {
      headers: { 'Authorization': 'Bearer ' + token }
    });

    if (!res.ok) {
      console.error('Error al obtener perfil:', res.status);
      return;
    }

    const u = await res.json();
    console.log('Perfil cargado:', u); // para debug

    const nombre = u.nombre || '';
    const apellido = u.apellido || '';
    const iniciales = ((nombre[0] || '?') + (apellido[0] || '?')).toUpperCase();
    const nombreCompleto = `${nombre} ${apellido}`.trim().toUpperCase();
    const claseplan = getClasePlan(u.plan);
    const planTexto = u.plan || 'Premium';

    aplicarTema(u.plan);

    //Cambiar Vistas
    function cambiarVista(el, vista) { 
      setNav(el);
      const vistaPerfil = document.getElementById('vista-perfil');
      const vistaClases = document.getElementById('vista-clases');
      const vistaRutinas = document.getElementById('vista-rutinas');
      const vistaPagos = document.getElementById('vista-pagos');
      const vistaSalud = document.getElementById('vista-salud');
      const vistaEntrenadores = document.getElementById('vista-entrenadores');
      const vistaConfiguracion = document.getElementById('vista-configuracion');
      const pageTitle = document.getElementById('pageTitle');

      if (vista === 'perfil') {
        if (vistaPerfil) vistaPerfil.style.display = 'block';
        if (vistaClases) vistaClases.style.display = 'none';
        if (vistaRutinas) vistaRutinas.style.display = 'none';
        if (vistaPagos) vistaPagos.style.display = 'none';
        if (vistaSalud) vistaSalud.style.display = 'none';
        if (vistaEntrenadores) vistaEntrenadores.style.display = 'none';
      } else if (vista === 'clases') {
        if (vistaPerfil) vistaPerfil.style.display = 'none';
        if (vistaClases) vistaClases.style.display = 'block';
        if (vistaRutinas) vistaRutinas.style.display = 'none';
        if (vistaPagos) vistaPagos.style.display = 'none';
        if (vistaSalud) vistaSalud.style.display = 'none';
        if (vistaEntrenadores) vistaEntrenadores.style.display = 'none';
      } else if (vista === 'rutinas') {
        if (vistaPerfil) vistaPerfil.style.display = 'none';
        if (vistaClases) vistaClases.style.display = 'none';
        if (vistaRutinas) vistaRutinas.style.display = 'block';
        if (vistaPagos) vistaPagos.style.display = 'none';
        if (vistaSalud) vistaSalud.style.display = 'none';
        if (vistaEntrenadores) vistaEntrenadores.style.display = 'none';
      } else if (vista === 'pagos') {
        if (vistaPerfil) vistaPerfil.style.display = 'none';
        if (vistaClases) vistaClases.style.display = 'none';
        if (vistaRutinas) vistaRutinas.style.display = 'none';
        if (vistaPagos) vistaPagos.style.display = 'block';
        if (vistaSalud) vistaSalud.style.display = 'none';
        if (vistaEntrenadores) vistaEntrenadores.style.display = 'none';
      } else if (vista === 'salud') {
        if (vistaPerfil) vistaPerfil.style.display = 'none';
        if (vistaClases) vistaClases.style.display = 'none';
        if (vistaRutinas) vistaRutinas.style.display = 'none';
        if (vistaPagos) vistaPagos.style.display = 'none';
        if (vistaSalud) vistaSalud.style.display = 'block';
        if (vistaEntrenadores) vistaEntrenadores.style.display = 'none';
      } else if (vista === 'entrenadores') {
        if (vistaPerfil) vistaPerfil.style.display = 'none';
        if (vistaClases) vistaClases.style.display = 'none';
        if (vistaRutinas) vistaRutinas.style.display = 'none';
        if (vistaPagos) vistaPagos.style.display = 'none';
        if (vistaSalud) vistaSalud.style.display = 'none';
        if (vistaEntrenadores) vistaEntrenadores.style.display = 'block';
      } else if (vista === 'configuracion') {
        if (vistaPerfil) vistaPerfil.style.display = 'none';
        if (vistaClases) vistaClases.style.display = 'none';
        if (vistaRutinas) vistaRutinas.style.display = 'none';
        if (vistaPagos) vistaPagos.style.display = 'none';
        if (vistaSalud) vistaSalud.style.display = 'none';
        if (vistaEntrenadores) vistaEntrenadores.style.display = 'none';
        if (vistaConfiguracion) vistaConfiguracion.style.display = 'block';
      }

       // Actualizar título de la página
       if (pageTitle) {
         if (vista === 'perfil') pageTitle.textContent = 'Mi Perfil';
         else if (vista === 'clases') pageTitle.textContent = 'Mis Clases';
         else if (vista === 'rutinas') pageTitle.textContent = 'Mi Rutina';
         else if (vista === 'pagos') pageTitle.textContent = 'Mis Pagos';
         else if (vista === 'salud') pageTitle.textContent = 'Mi Salud';
         else if (vista === 'entrenadores') pageTitle.textContent = 'Mis Entrenadores';
         else if (vista === 'configuracion') pageTitle.textContent = 'Configuración';
       }
      
    }

    // ── Hero ─────────────────────────────────────────
    setText('heroAvatar', iniciales);
    setText('heroName', nombreCompleto);
    setText('heroId', '#' + String(u.id).padStart(4, '0'));
    setText('heroCedula', u.cedula);

    const heroPlan = document.getElementById('heroPlan');
    if (heroPlan) {
      heroPlan.textContent = planTexto.toUpperCase();
      heroPlan.className = `badge badge-${claseplan}`;
    }

    // ── Sidebar ───────────────────────────────────────
    setText('sideAvatar', iniciales);
    setText('sideName', `${nombre} ${apellido}`.trim());
    setText('sideRole', 'MIEMBRO #' + String(u.id).padStart(4, '0'));

    // ── Datos personales — SOLO LECTURA ───────────────
    setText('vNombre', nombre);
    setText('vApellido', apellido);
    setText('vCedula', u.cedula);
    setText('vFechaNac', formatFecha(u.fecha_nacimiento));

    // Peso y estatura: mostrar con unidad o '—'
    setText('vPeso', u.peso ? u.peso + ' kg' : '—');
    setText('vEstatura', u.estatura ? u.estatura + ' cm' : '—');
    setText('vTipoSangre', u.tipo_sangre || '—');
    setText('vLesiones', u.lesiones || 'Sin lesiones reportadas');

    // Pre-llenar input de peso para edición
    const fPeso = document.getElementById('fPeso');
    if (fPeso) fPeso.value = u.peso || '';

    // ── Campos EDITABLES: solo llenar el texto visible y el input ──
    // Correo
    setText('vCorreo', u.correo || '—');
    const fCorreo = document.getElementById('fCorreo');
    if (fCorreo) fCorreo.value = u.correo || '';

    // Teléfono
    setText('vTelefono', u.telefono || '—');
    const fTelefono = document.getElementById('fTelefono');
    if (fTelefono) fTelefono.value = u.telefono || '';

    // Dirección
    setText('vDireccion', u.direccion || '—');
    const fDireccion = document.getElementById('fDireccion');
    if (fDireccion) fDireccion.value = u.direccion || '';

    // Lesiones
    setText('vLesiones', u.lesiones || 'Sin lesiones reportadas');
    const fLesiones = document.getElementById('fLesiones');
    if (fLesiones) fLesiones.value = u.lesiones || ''; 

    // ── Panel Salud ───────────────────────────────────
    setHtml('saludPeso', (u.peso || '—') + '<span class="salud-unit"> kg</span>');
    setHtml('saludEstatura', (u.estatura || '—') + '<span class="salud-unit"> cm</span>');
    setText('saludSangre', u.tipo_sangre || '—');
    setText('saludLesiones', u.lesiones || 'Sin lesiones reportadas');

    // IMC calculado solo si hay peso y estatura
    if (u.peso && u.estatura) {
      const imc = (parseFloat(u.peso) / Math.pow(parseFloat(u.estatura) / 100, 2)).toFixed(1);
      setText('saludImc', imc);
    } else {
      setText('saludImc', '—');
    }

    // ── Membresía ─────────────────────────────────────
    setText('membPlan', planTexto);
    setText('membPrecio', getPrecio(u.plan));
    const membBadge = document.getElementById('membBadge');
    if (membBadge) {
      membBadge.textContent = planTexto.toUpperCase();
      membBadge.className = `badge badge-${claseplan}`;
    }

    // ── Alert bar ─────────────────────────────────────
    const alertMsg = document.getElementById('alertMsg');
    if (alertMsg) {
      alertMsg.innerHTML = `<strong>AVISO —</strong> Tu membresía <strong>${planTexto}</strong> vence en <strong>25 días</strong>. Renueva ahora para no perder acceso.`;
    }

    // ── Última edición ────────────────────────────────
    const hoy = `${_d.getDate()} ${meses[_d.getMonth()]} ${_d.getFullYear()}`;
    setText('ultimaEdicion', `Última edición: ${hoy}`);

  } catch (err) {
    console.error('Error cargando perfil:', err);
  }
}

// ══════════════════════════════════════════════════════
// EDICIÓN — solo correo, teléfono y dirección
// ══════════════════════════════════════════════════════

function toggleEdit() {
  // Mostrar inputs y labels de los campos editables
  hide('vCorreo'); show('fCorreo'); show('labelCorreo');
  hide('vTelefono'); show('fTelefono'); show('labelTelefono');
  hide('vDireccion'); show('fDireccion'); show('labelDireccion');
  hide('vPeso'); show('fPeso'); show('labelPeso');

  // Enfocar el primero
  const fCorreo = document.getElementById('fCorreo');
  if (fCorreo) fCorreo.focus();

  hide('editBtn');
  show('saveBtn');
}

async function saveProfile() {
  const correo = document.getElementById('fCorreo').value.trim();
  const telefono = document.getElementById('fTelefono').value.trim();
  const direccion = document.getElementById('fDireccion').value.trim();
  const pesoVal = document.getElementById('fPeso').value.trim();
  const peso = pesoVal !== '' ? pesoVal : null;

  // Volver al modo lectura
  setText('vCorreo', correo || '—');
  setText('vTelefono', telefono || '—');
  setText('vDireccion', direccion || '—');
  if (peso !== null) {
    setText('vPeso', peso + ' kg');
    // Actualizar también el panel salud
    setHtml('saludPeso', peso + '<span class="salud-unit"> kg</span>');
    // Recalcular IMC si hay estatura
    const estaturaEl = document.getElementById('vEstatura');
    if (estaturaEl) {
      const estStr = estaturaEl.textContent.replace(' cm', '').trim();
      const est = parseFloat(estStr);
      if (!isNaN(est) && est > 0) {
        const imc = (parseFloat(peso) / Math.pow(est / 100, 2)).toFixed(1);
        setText('saludImc', imc);
      }
    }
  }

  show('vCorreo'); hide('fCorreo'); hide('labelCorreo');
  show('vTelefono'); hide('fTelefono'); hide('labelTelefono');
  show('vDireccion'); hide('fDireccion'); hide('labelDireccion');
  show('vPeso'); hide('fPeso'); hide('labelPeso');

  show('editBtn');
  hide('saveBtn');

  // Enviar al backend
  const token = sessionStorage.getItem('gym_token') || localStorage.getItem('gym_token');
  if (!token) return;

  // Solo enviar campos que tengan valor (no sobreescribir con null si no cambiaron)
  const payload = { correo, telefono, direccion };
  if (peso !== null) payload.peso = peso;

  try {
    const res = await fetch('/api/usuario/perfil', {
      method: 'PUT',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      showToast('✓ Datos guardados correctamente');
    } else {
      const err = await res.json().catch(() => ({}));
      showToast('❌ Error: ' + (err.error || res.statusText));
    }
  } catch (err) {
    showToast('❌ Error de conexión: ' + err.message);
  }
}

// ── Toast ─────────────────────────────────────────────
function showToast(msg) {
  const t = document.getElementById('toast');
  document.getElementById('toastMsg').textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

// ── Arrancar al cargar ────────────────────────────────
window.addEventListener('load', cargarPerfil);