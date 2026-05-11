const meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];

// ── Fecha topbar 
const d = new Date();
const dias = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
document.getElementById('dateDisplay').textContent =
  `${dias[d.getDay()]}, ${d.getDate()} ${meses[d.getMonth()]} ${d.getFullYear()}`;

// ── Cargar perfil desde la API con el token 
async function cargarPerfil() {
  const token = localStorage.getItem('gym_token') || sessionStorage.getItem('gym_token');
  if (!token) return;

  try {
    const res = await fetch('/api/usuario/perfil', {
      headers: { 'Authorization': 'Bearer ' + token }
    });
    if (!res.ok) return;
    const u = await res.json();

    // Nombre completo
    const nombreCompleto = `${u.nombre} ${u.apellido}`.toUpperCase();
    const iniciales = (u.nombre.substring(0, 1) + u.apellido.substring(0, 1)).toUpperCase();

    // Hero
    const heroAvatar = document.querySelector('.hero-avatar');
    const heroName = document.querySelector('.hero-name');
    if (heroAvatar) heroAvatar.textContent = iniciales;
    if (heroName) heroName.textContent = nombreCompleto;

    // Badges de plan en hero
    const badgePlan = document.querySelector('.badge-premium');
    if (badgePlan) badgePlan.textContent = (u.plan || 'Premium').toUpperCase();

    // ID en hero
    const heroTags = document.querySelectorAll('.hero-tag span');
    if (heroTags[1]) heroTags[1].textContent = '#' + String(u.id).padStart(4, '0');
    if (heroTags[2]) heroTags[2].textContent = u.cedula || '—';

    // Sidebar avatar y nombre
    const sideAvatar = document.querySelector('.sidebar-footer .avatar');
    const sideName = document.querySelector('.sidebar-footer .user-name');
    const sideRole = document.querySelector('.sidebar-footer .user-role');
    if (sideAvatar) sideAvatar.textContent = iniciales;
    if (sideName) sideName.textContent = `${u.nombre} ${u.apellido}`;
    if (sideRole) sideRole.textContent = 'MIEMBRO #' + String(u.id).padStart(4, '0');

    // ── Campos del panel Datos Personales ─────────────
    const values = document.querySelectorAll('#panelDatos .field-value');
    if (values[0]) values[0].textContent = u.nombre || '—';
    if (values[1]) values[1].textContent = u.apellido || '—';
    if (values[2]) values[2].textContent = u.correo || '—';
    if (values[3]) values[3].textContent = u.telefono || '—';
    if (values[4]) {
      if (u.fecha_nacimiento) {
        const [y, m, day] = u.fecha_nacimiento.split('-');
        values[4].textContent = `${day} ${meses[parseInt(m) - 1]} ${y}`;
      } else {
        values[4].textContent = '—';
      }
    }
    if (values[5]) values[5].textContent = u.direccion || '—';

    // ── Inputs de edición 
    const fNombre = document.getElementById('fNombre');
    const fApellido = document.getElementById('fApellido');
    const fCorreo = document.getElementById('fCorreo');
    const fTelefono = document.getElementById('fTelefono');
    const fFecha = document.getElementById('fFecha');
    const fDireccion = document.getElementById('fDireccion');
    if (fNombre) fNombre.value = u.nombre || '';
    if (fApellido) fApellido.value = u.apellido || '';
    if (fCorreo) fCorreo.value = u.correo || '';
    if (fTelefono) fTelefono.value = u.telefono || '';
    if (fFecha) fFecha.value = u.fecha_nacimiento || '';
    if (fDireccion) fDireccion.value = u.direccion || '';

    // ── Panel Salud 
    const saludVals = document.querySelectorAll('.salud-val');
    if (saludVals[0]) saludVals[0].innerHTML = (u.peso || '—') + '<span class="salud-unit"> kg</span>';
    if (saludVals[1]) saludVals[1].innerHTML = (u.estatura || '—') + '<span class="salud-unit"> cm</span>';
    if (saludVals[3]) saludVals[3].textContent = u.tipo_sangre || '—';

    // IMC
    if (u.peso && u.estatura && saludVals[2]) {
      const imc = (parseFloat(u.peso) / Math.pow(parseFloat(u.estatura) / 100, 2)).toFixed(1);
      saludVals[2].textContent = imc;
    }

    // Lesiones
    const lesionEl = document.querySelector('.salud-item:last-child div:last-child');
    if (lesionEl) lesionEl.textContent = u.lesiones || 'Sin lesiones reportadas';

    // Plan membresía
    const membVal = document.querySelectorAll('.memb-val');
    if (membVal[0]) membVal[0].textContent = u.plan || 'Premium';

  } catch (err) {
    console.error('Error cargando perfil:', err);
  }
}

// ── Edición de perfil 
let editing = false;

function toggleEdit() {
  editing = true;
  document.getElementById('panelDatos').classList.add('edit-mode');
  document.getElementById('editBtn').style.display = 'none';
  document.getElementById('saveBtn').style.display = '';
}

function saveProfile() {
  editing = false;
  const values = document.querySelectorAll('#panelDatos .field-value');
  const inputNombre = document.getElementById('fNombre').value;
  const inputApellido = document.getElementById('fApellido').value;

  values[0].textContent = inputNombre;
  values[1].textContent = inputApellido;
  values[2].textContent = document.getElementById('fCorreo').value;
  values[3].textContent = document.getElementById('fTelefono').value;

  const fd = document.getElementById('fFecha').value;
  if (fd) {
    const [y, m, day] = fd.split('-');
    values[4].textContent = `${day} ${meses[parseInt(m) - 1]} ${y}`;
  }
  values[5].textContent = document.getElementById('fDireccion').value;

  // Actualizar también el hero
  const heroName = document.querySelector('.hero-name');
  if (heroName) heroName.textContent = `${inputNombre} ${inputApellido}`.toUpperCase();
  const heroAvatar = document.querySelector('.hero-avatar');
  if (heroAvatar) heroAvatar.textContent = (inputNombre[0] + inputApellido[0]).toUpperCase();
  const sideName = document.querySelector('.sidebar-footer .user-name');
  if (sideName) sideName.textContent = `${inputNombre} ${inputApellido}`;
  const sideAvatar = document.querySelector('.sidebar-footer .avatar');
  if (sideAvatar) sideAvatar.textContent = (inputNombre[0] + inputApellido[0]).toUpperCase();

  document.getElementById('panelDatos').classList.remove('edit-mode');
  document.getElementById('editBtn').style.display = '';
  document.getElementById('saveBtn').style.display = 'none';

  showToast(`Perfil actualizado: ${inputNombre} ${inputApellido}`);
}

function showToast(msg) {
  const t = document.getElementById('toast');
  document.getElementById('toastMsg').textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

// ── Iniciar al cargar la página ────────────────────────
window.addEventListener('load', cargarPerfil);