
  // Fecha topbar
  const d = new Date();
  const dias = ['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'];
  const meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
  document.getElementById('dateDisplay').textContent =
  `${dias[d.getDay()]}, ${d.getDate()} ${meses[d.getMonth()]} ${d.getFullYear()}`;

  // Edición de perfil
  let editing = false;
  function toggleEdit() {
    editing = true;
  document.getElementById('panelDatos').classList.add('edit-mode');
  document.getElementById('editBtn').style.display = 'none';
  document.getElementById('saveBtn').style.display = '';
  }

  function saveProfile() {
    editing = false;
  // Actualizar valores mostrados
  const campos = [
  ['fNombre', 0], ['fApellido', 1], ['fCorreo', 2],
  ['fTelefono', 3], ['fFecha', 4], ['fDireccion', 5]
  ];
  const values = document.querySelectorAll('#panelDatos .field-value');
  const dates = {'1993-03-15': '15 Mar 1993' };
  const inputNombre = document.getElementById('fNombre').value;
  const inputApellido = document.getElementById('fApellido').value;

  values[0].textContent = inputNombre;
  values[1].textContent = inputApellido;
  values[2].textContent = document.getElementById('fCorreo').value;
  values[3].textContent = document.getElementById('fTelefono').value;
  const fd = document.getElementById('fFecha').value;
  if (fd) {
      const [y,m,day] = fd.split('-');
  values[4].textContent = `${day} ${meses[parseInt(m) - 1]} ${y}`;
    }
  values[5].textContent = document.getElementById('fDireccion').value;

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
