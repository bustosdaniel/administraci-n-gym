
  const API = 'http://localhost:5000/api';

  async function cargarDatos() {
    // Cargar estadísticas
    const stats = await fetch(`${API}/dashboard/stats`).then(r => r.json()).catch(e => null);
    if (stats) {
      document.querySelectorAll('.stat-value')[0].textContent = stats.miembros_activos;
      document.querySelectorAll('.stat-value')[1].textContent = '$' + stats.ingresos_mes.toLocaleString();
      document.querySelectorAll('.stat-value')[2].textContent = stats.clases_hoy;
      document.querySelectorAll('.stat-value')[3].textContent = stats.ocupacion_actual + '%';
    }

    // Cargar miembros
    const miembros = await fetch(`${API}/miembros`).then(r => r.json()).catch(e => []);
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
          <td><span class="badge badge-premium">${m.plan}</span></td>
          <td><span style="font-family:var(--mono);font-size:.7rem">${m.vence}</span></td>
          <td><span class="badge badge-active">${m.estado}</span></td>
        </tr>
      `).join('');
    }
  }

  function setNav(el) {
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    el.classList.add('active');
  }

  // Chart
  const data = [
    { day:'LUN', val:68 },
    { day:'MAR', val:82 },
    { day:'MIÉ', val:74 },
    { day:'JUE', val:91 },
    { day:'VIE', val:88 },
    { day:'SÁB', val:95 },
    { day:'DOM', val:45 },
  ];
  const maxVal = Math.max(...data.map(d => d.val));
  const barsEl = document.getElementById('chartBars');
  const labelsEl = document.getElementById('chartLabels');
  const today = new Date().getDay();
  const dayMap = [6,0,1,2,3,4,5];
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

  // Modal
  function openModal() {
    document.getElementById('modalOverlay').classList.add('open');
  }
  function closeModal() {
    document.getElementById('modalOverlay').classList.remove('open');
  }
  function closeModalOutside(e) {
    if (e.target === document.getElementById('modalOverlay')) closeModal();
  }

  // Toast
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

    // Validar obligatorios
    if (!nombre || !apellido || !correo || !cedula || !telefono || !direccion || !fecha_nac) {
      showToast('❌ Rellena todos los campos (*) requeridos');
      return;
    }

    const res = await fetch(`${API}/usuarios`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        nombre,
        apellido,
        correo_electronico: correo,
        cedula,
        numero_celular: telefono,
        fecha_nacimiento: fecha_nac,
        direccion,
        peso: document.getElementById('inputPeso').value || null,
        estatura: document.getElementById('inputEstatura').value || null,
        tipo_sangre: document.getElementById('inputTipoSangre').value || null,
        lesiones: document.getElementById('inputLesiones').value || null
      })
    }).catch(e => null);

    if (res && res.ok) {
      closeModal();
      showToast('✓ Miembro registrado');
      document.querySelectorAll('.modal-body input, .modal-body select').forEach(i => i.value = '');
      setTimeout(() => cargarDatos(), 300);
    } else {
      showToast('❌ Error al guardar. Intenta de nuevo');
    }
  }

  window.addEventListener('load', () => {
    // Fecha
    const d = new Date();
    const opts = { weekday:'long', year:'numeric', month:'long', day:'numeric' };
    document.getElementById('dateDisplay').textContent = d.toLocaleDateString('es-MX', opts).toUpperCase();

    // Ring
    const ring = document.getElementById('ringCircle');
    if (ring) {
      const circumference = 264;
      const offset = circumference * (1 - 0.68);
      ring.style.strokeDashoffset = offset;
    }

    cargarDatos();
  });