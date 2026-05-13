const API = '/api';

// ── Normaliza el plan a su clase CSS de badge ──────────
function planClass(plan) {
  const p = (plan || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  if (p.includes('elite')) return 'badge-elite';
  if (p.includes('premium')) return 'badge-premium';
  return 'badge-basic';
}
function planLabel(plan) {
  const p = (plan || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  if (p.includes('elite')) return 'Elite';
  if (p.includes('premium')) return 'Premium';
  return 'Básico';
}

async function cargarDatos() {
  console.log('Cargando datos desde API...');

  try {
    const statsRes = await fetch(`${API}/dashboard/stats`);
    const stats = await statsRes.json();
    if (stats) {
      document.querySelectorAll('.stat-value')[0].textContent = stats.miembros_activos;
      document.querySelectorAll('.stat-value')[1].textContent = '$' + stats.ingresos_mes.toLocaleString();
      document.querySelectorAll('.stat-value')[2].textContent = stats.clases_hoy;
      document.querySelectorAll('.stat-value')[3].textContent = stats.ocupacion_actual + '%';
      const badge = document.getElementById('navBadgeMiembros');
      if (badge) badge.textContent = stats.miembros_activos;
    }
  } catch (e) { console.error('Error cargando stats:', e); }

  try {
    const miembrosRes = await fetch(`${API}/miembros`);
    const miembros = await miembrosRes.json();
    const tbody = document.querySelector('.table tbody');
    if (tbody && miembros.length > 0) {
      tbody.innerHTML = miembros.map(m => `
        <tr>
          <td>
            <div class="member-cell">
              <div class="member-avatar">${m.nombre.substring(0, 2).toUpperCase()}</div>
              <div>
                <div class="member-name">${m.nombre}</div>
                <div class="member-id">#${String(m.id).padStart(4, '0')}</div>
              </div>
            </div>
          </td>
          <td><span class="badge ${planClass(m.plan)}">${planLabel(m.plan)}</span></td>
          <td><span style="font-family:var(--mono);font-size:.7rem">${m.vence}</span></td>
          <td><span class="badge badge-active">${m.estado}</span></td>
        </tr>
      `).join('');
    }
  } catch (e) { console.error('Error cargando miembros:', e); }
}

function setNav(el) {
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  el.classList.add('active');
}

// ── Sistema de vistas ──────────────────────────────────
function cambiarVista(el, vista) {
  setNav(el);
  
  // Ocultar todas las vistas
  const vistas = [
    'vista-dashboard',
    'vista-miembros',
    'vista-clases',
    'vista-pagos',
    'vista-equipos',
    'vista-entrenadores',
    'vista-reportes',
    'vista-configuracion'
  ];
  
  vistas.forEach(id => {
    const elem = document.getElementById(id);
    if (elem) elem.style.display = 'none';
  });

  const pageTitle = document.getElementById('pageTitle');
  const verTodosBtn = document.getElementById('verTodosBtn');

  // Mostrar la vista seleccionada
  if (vista === 'dashboard') {
    const vistaDashboard = document.getElementById('vista-dashboard');
    if (vistaDashboard) vistaDashboard.style.display = 'block';
    if (pageTitle) pageTitle.textContent = 'GYM FORTE';
    if (verTodosBtn) verTodosBtn.style.display = '';
  } else if (vista === 'miembros') {
    const vistaMiembros = document.getElementById('vista-miembros');
    if (vistaMiembros) { 
      vistaMiembros.style.display = 'flex';
      vistaMiembros.style.flexDirection = 'column';
    }
    if (pageTitle) pageTitle.textContent = 'Miembros';
    if (verTodosBtn) verTodosBtn.style.display = 'none';
    cargarTodosMiembros();
  } else if (vista === 'clases') {
    const vistaClases = document.getElementById('vista-clases');
    if (vistaClases) vistaClases.style.display = 'block';
    if (pageTitle) pageTitle.textContent = 'Clases';
  } else if (vista === 'pagos') {
    const vistaPagos = document.getElementById('vista-pagos');
    if (vistaPagos) vistaPagos.style.display = 'block';
    if (pageTitle) pageTitle.textContent = 'Pagos';
  } else if (vista === 'equipos') {
    const vistaEquipos = document.getElementById('vista-equipos');
    if (vistaEquipos) vistaEquipos.style.display = 'block';
    if (pageTitle) pageTitle.textContent = 'Equipos';
  } else if (vista === 'entrenadores') {
    const vistaEntrenadores = document.getElementById('vista-entrenadores');
    if (vistaEntrenadores) vistaEntrenadores.style.display = 'block';
    if (pageTitle) pageTitle.textContent = 'Entrenadores';
  } else if (vista === 'reportes') {
    const vistaReportes = document.getElementById('vista-reportes');
    if (vistaReportes) vistaReportes.style.display = 'block';
    if (pageTitle) pageTitle.textContent = 'Reportes';
  } else if (vista === 'configuracion') {
    const vistaConfig = document.getElementById('vista-configuracion');
    if (vistaConfig) vistaConfig.style.display = 'block';
    if (pageTitle) pageTitle.textContent = 'Configuración del Sistema';
    cargarConfiguracion();
  }
}

// ── Cargar TODOS los miembros ──────────────────────────
async function cargarTodosMiembros() {
  console.log('Cargando todos los miembros...');
  try {
    const res = await fetch(`${API}/miembros-todos`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const miembros = await res.json();

    document.getElementById('totalMiembros').textContent = miembros.length;
    const badge = document.getElementById('navBadgeMiembros');
    if (badge) badge.textContent = miembros.length;
    const statCard = document.getElementById('statTotalMiembros');
    if (statCard) statCard.textContent = miembros.length;

    const tbody = document.getElementById('tablaMiembrosCompleta');
    if (!tbody) return;

    if (miembros.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:20px;color:var(--muted);">No hay miembros registrados</td></tr>';
      return;
    }

    const colors = ['#f97316', '#22c55e', '#3b82f6', '#a855f7', '#eab308', '#ef4444', '#06b6d4', '#f43f5e'];
    tbody.innerHTML = miembros.map((m, i) => `
      <tr>
        <td>
          <div class="member-cell">
            <div class="member-avatar" style="background:${colors[i % colors.length]}">${m.nombre.substring(0, 2).toUpperCase()}</div>
            <div>
              <div class="member-name">${m.nombre}</div>
              <div class="member-id">#${String(m.id).padStart(4, '0')}</div>
            </div>
          </div>
        </td>
        <td><span style="font-size:0.85rem">${m.correo || '-'}</span></td>
        <td><span style="font-size:0.85rem">${m.telefono || '-'}</span></td>
        <td><span class="badge ${planClass(m.plan)}">${planLabel(m.plan)}</span></td>
        <td><span style="font-family:var(--mono);font-size:.7rem">${m.vence}</span></td>
        <td><span class="badge badge-active">${m.estado}</span></td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Error cargando miembros:', err);
    const tbody = document.getElementById('tablaMiembrosCompleta');
    if (tbody) tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:20px;color:red;">Error: ${err.message}</td></tr>`;
  }
}

// ── Cargar opciones de configuración (lista de usuarios con opción eliminar)
function getAvatarColor(userId) {
  const colors = ['#f97316', '#22c55e', '#3b82f6', '#a855f7', '#eab308', '#ef4444', '#06b6d4', '#f43f5e'];
  const idNum = parseInt(userId, 10) || 0;
  return colors[idNum % colors.length];
}

async function cargarConfiguracion() {
  console.log('Cargando configuración...');
  const userDetailCard = document.getElementById('userDetailCard');
  if (userDetailCard) userDetailCard.style.display = 'none';
  try {
    const res = await fetch(`${API}/miembros-todos`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const miembros = await res.json();

    const tbody = document.getElementById('tablaConfigCompleta');
    if (!tbody) return;

    if (miembros.length === 0) {
      tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:20px;color:var(--muted);">No hay miembros registrados</td></tr>';
      return;
    }

    tbody.innerHTML = `<tr><th>Miembro</th><th>Correo</th><th>Aviso</th><th>Acciones</th></tr>` +
      miembros.map(m => {
        const avatarColor = getAvatarColor(m.id);
        return `
      <tr data-id="${m.id}">
        <td>
          <div style="display:flex;align-items:center;gap:12px">
            <div class="member-avatar" style="width:36px;height:36px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;background:${avatarColor};color:#fff;font-weight:700;">${m.nombre.substring(0,2).toUpperCase()}</div>
            <div>
              <div style="font-weight:600">${m.nombre}</div>
              <div style="font-family:var(--mono);font-size:.75rem;color:var(--muted)">#${String(m.id).padStart(4,'0')}</div>
            </div>
          </div>
        </td>
        <td style="font-size:0.9rem">${m.correo || '-'}</td>
        <td style="font-size:0.9rem">${membreHtml(m.id)}</td>
        <td style="width:220px">
          <button class="btn btn-ghost" onclick="mostrarUsuarioConfig(${m.id})">Ver</button>
          <button class="btn btn-danger" onclick="confirmDeleteUser(${m.id}, '${encodeURIComponent(m.nombre)}')">Eliminar</button>
        </td>
      </tr>
    `}).join('');

  } catch (err) {
    console.error('Error cargando configuración:', err);
    const tbody = document.getElementById('tablaConfigCompleta');
    if (tbody) tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;padding:20px;color:red;">Error: ${err.message}</td></tr>`;
  }
}

async function mostrarUsuarioConfig(id) {
  try {
    const res = await fetch(`${API}/usuarios/${id}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const u = await res.json();

    const avatarColor = getAvatarColor(u.id);
    const initials = `${(u.nombre || '?')[0] || '?'}${(u.apellido || '?')[0] || '?'}`.toUpperCase();
    const userDetailCard = document.getElementById('userDetailCard');
    if (userDetailCard) userDetailCard.style.display = 'block';
    const subtitle = document.getElementById('userDetailSubtitle');
    if (subtitle) subtitle.textContent = `ID #${String(u.id).padStart(4,'0')} · ${u.plan || 'Premium'}`;
    const avatar = document.getElementById('userDetailAvatar');
    if (avatar) {
      avatar.textContent = initials;
      avatar.style.backgroundColor = avatarColor;
      avatar.style.color = '#fff';
    }
    const nameEl = document.getElementById('userDetailName');
    if (nameEl) nameEl.textContent = `${u.nombre || ''} ${u.apellido || ''}`.trim();
    const planEl = document.getElementById('userDetailPlan');
    if (planEl) planEl.textContent = `Plan: ${u.plan || 'Premium'}`;
    const idEl = document.getElementById('userDetailId');
    if (idEl) idEl.textContent = `#${String(u.id).padStart(4,'0')}`;
    const cedulaEl = document.getElementById('userDetailCedula');
    if (cedulaEl) cedulaEl.textContent = u.cedula || '—';
    const correoEl = document.getElementById('userDetailCorreo');
    if (correoEl) correoEl.textContent = u.correo || '—';
    const telEl = document.getElementById('userDetailTelefono');
    if (telEl) telEl.textContent = u.telefono || '—';
    const dirEl = document.getElementById('userDetailDireccion');
    if (dirEl) dirEl.textContent = u.direccion || '—';
    const fechaEl = document.getElementById('userDetailFecha');
    if (fechaEl) fechaEl.textContent = u.fecha_nacimiento || '—';
    const pesoEl = document.getElementById('userDetailPeso');
    if (pesoEl) pesoEl.textContent = u.peso ? `${u.peso} kg` : '—';
    const estaturaEl = document.getElementById('userDetailEstatura');
    if (estaturaEl) estaturaEl.textContent = u.estatura ? `${u.estatura} cm` : '—';
    const sangreEl = document.getElementById('userDetailTipoSangre');
    if (sangreEl) sangreEl.textContent = u.tipo_sangre || '—';
    const lesionesEl = document.getElementById('userDetailLesiones');
    if (lesionesEl) lesionesEl.textContent = u.lesiones || 'Sin lesiones reportadas';

    const statusText = document.getElementById('userStatusText');
    if (statusText) {
      const estado = getRandomStatus();
      statusText.textContent = estado.label;
      statusText.className = `status-label ${estado.cls}`;
      statusText.title = estado.title;
    }
  } catch (err) {
    console.error('Error mostrando usuario:', err);
    showToast('No se pudo cargar el usuario.');
  }
}

function getRandomStatus() {
  const estados = [
    {label: 'Pago', cls: 'status-ok', title: 'Pago al día'},
    {label: 'Pendiente', cls: 'status-pending', title: 'Pago pendiente'},
    {label: 'No pago', cls: 'status-due', title: 'Pago vencido'}
  ];
  return estados[Math.floor(Math.random() * estados.length)];
}

function viewMember(id) {
  mostrarUsuarioConfig(id);
}

// Devuelve html de membresía con estado aleatorio
function membreHtml(id) {
  const estados = [
    {k: 'pago', label: 'Pago', cls: 'pay-ok', title: 'Pago al día'},
    {k: 'pendiente', label: 'Pendiente', cls: 'pay-pending', title: 'Pago pendiente'},
    {k: 'no_pago', label: 'No pago', cls: 'pay-due', title: 'Pago vencido'}
  ];
  const idx = Math.floor(Math.random() * estados.length);
  const e = estados[idx];
  return `<span class="pay-indicator ${e.cls}" title="${e.title}"></span>`;
}

function escapeHtml(str) {
  return (str || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// ── Modal eliminar
let _deleteTargetId = null;
function confirmDeleteUser(id, encodedNombre) {
  _deleteTargetId = id;
  const nombre = decodeURIComponent(encodedNombre || '');
  const modal = document.getElementById('modalDeleteOverlay');
  const text = document.getElementById('modalDeleteText');
  if (text) text.textContent = `¿Estás seguro de eliminar la cuenta de ${nombre} (ID #${String(id).padStart(4,'0')})? Esta acción no se puede deshacer.`;
  if (modal) modal.style.display = 'block';
  const btn = document.getElementById('confirmDeleteBtn');
  if (btn) {
    btn.onclick = () => deleteUserConfirmed();
  }
}

function closeDeleteModal() {
  const modal = document.getElementById('modalDeleteOverlay');
  if (modal) modal.style.display = 'none';
  _deleteTargetId = null;
}

function closeDeleteModalOutside(e) { if (e.target === document.getElementById('modalDeleteOverlay')) closeDeleteModal(); }

async function deleteUserConfirmed() {
  if (!_deleteTargetId) return;
  try {
    const res = await fetch(`${API}/usuarios/${_deleteTargetId}`, {
      method: 'DELETE'
    });
    if (res.ok) {
      showToast('Usuario eliminado');
      closeDeleteModal();
      // refrescar vistas
      cargarDatos();
      cargarTodosMiembros();
      cargarConfiguracion();
    } else {
      const body = await res.json().catch(() => ({}));
      showToast('Error: ' + (body.error || 'No se pudo eliminar'));
    }
  } catch (err) {
    showToast('Error de conexión: ' + err.message);
  }
}

function mostrarTodosMiembros(e) {
  if (e) e.preventDefault();
  const navItems = document.querySelectorAll('.nav-item');
  for (let item of navItems) {
    if (item.textContent.trim().startsWith('Miembros') || item.textContent.includes('👥')) {
      cambiarVista(item, 'miembros');
      break;
    }
  }
}

// ── Chart ──────────────────────────────────────────────
const data = [
  { day: 'LUN', val: 68 }, { day: 'MAR', val: 82 }, { day: 'MIÉ', val: 74 },
  { day: 'JUE', val: 91 }, { day: 'VIE', val: 88 }, { day: 'SÁB', val: 95 }, { day: 'DOM', val: 45 },
];
const maxVal = Math.max(...data.map(d => d.val));
const barsEl = document.getElementById('chartBars');
const labelsEl = document.getElementById('chartLabels');
const today = new Date().getDay();
const dayMap = [6, 0, 1, 2, 3, 4, 5];
const todayIdx = dayMap[today];

data.forEach((item, i) => {
  const pct = (item.val / maxVal) * 100;
  const isToday = i === todayIdx;
  const wrap = document.createElement('div');
  wrap.className = 'bar-wrap';
  wrap.innerHTML = `<div class="bar ${isToday ? 'active-bar' : ''}" style="height:${pct}%" title="$${item.val * 800}"></div>`;
  barsEl.appendChild(wrap);
  const label = document.createElement('div');
  label.className = 'bar-wrap';
  label.innerHTML = `<span class="bar-label" style="${isToday ? 'color:var(--accent)' : ''}">${item.day}</span>`;
  labelsEl.appendChild(label);
});

// ── Modal ──────────────────────────────────────────────
function openModal() { document.getElementById('modalOverlay').classList.add('open'); }
function closeModal() { document.getElementById('modalOverlay').classList.remove('open'); }
function closeModalOutside(e) { if (e.target === document.getElementById('modalOverlay')) closeModal(); }

// ── Toast ──────────────────────────────────────────────
function showToast(msg) {
  const t = document.getElementById('toast');
  document.getElementById('toastMsg').textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

async function saveNewMember() {
  const nombre = document.getElementById('inputNombre').value.trim();
  const apellido = document.getElementById('inputApellido').value.trim();
  const correo = document.getElementById('inputCorreo').value.trim();
  const cedula = document.getElementById('inputCedula').value.trim();
  const telefono = document.getElementById('inputTelefono').value.trim();
  const direccion = document.getElementById('inputDireccion').value.trim();
  const fecha_nac = document.getElementById('inputFechaNac').value.trim();
  const plan = document.getElementById('inputPlan').value.trim();

  if (!nombre || !apellido || !correo || !cedula || !telefono || !direccion || !fecha_nac || !plan) {
    showToast('❌ Rellena todos los campos (*) requeridos');
    return;
  }

  try {
    const res = await fetch(`${API}/usuarios`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nombre, apellido,
        correo_electronico: correo,
        cedula,
        numero_celular: telefono,
        fecha_nacimiento: fecha_nac,
        direccion, plan,
        peso: document.getElementById('inputPeso').value || null,
        estatura: document.getElementById('inputEstatura').value || null,
        tipo_sangre: document.getElementById('inputTipoSangre').value || null,
        lesiones: document.getElementById('inputLesiones').value || null
      })
    });

    if (res && res.ok) {
      closeModal();
      showToast('✓ Miembro registrado');
      document.querySelectorAll('.modal-body input, .modal-body select').forEach(i => i.value = '');
      setTimeout(() => cargarDatos(), 300);
    } else {
      showToast('❌ Error al guardar. Intenta de nuevo');
    }
  } catch (err) {
    showToast('❌ Error de conexión: ' + err.message);
  }
}

window.addEventListener('load', () => {
  const d = new Date();
  const opts = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  document.getElementById('dateDisplay').textContent = d.toLocaleDateString('es-MX', opts).toUpperCase();

  const ring = document.getElementById('ringCircle');
  if (ring) {
    const circumference = 264;
    ring.style.strokeDashoffset = circumference * (1 - 0.68);
  }

  cargarDatos();
});