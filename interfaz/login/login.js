  /* TABS */
  function switchTab(t) {
    const isL = t === 'login';
  document.getElementById('pLogin').classList.toggle('active', isL);
  document.getElementById('pRegister').classList.toggle('active', !isL);
  document.getElementById('tabL').classList.toggle('active', isL);
  document.getElementById('tabR').classList.toggle('active', !isL);
  document.getElementById('tabBar').classList.toggle('right', !isL);
  if (!isL) {currentStep = 1; showStep(1); }
  }

  /* PASSWORD TOGGLE */
  function toggleVer(id, btn) {
    const inp = document.getElementById(id);
  const show = inp.type === 'password';
  inp.type = show ? 'text' : 'password';
  btn.textContent = show ? 'OCULTAR' : 'MOSTRAR';
  }

  /* STRENGTH */
  function checkStr(v) {
    let sc = 0;
    if (v.length >= 8) sc++;
  if (/[A-Z]/.test(v)) sc++;
  if (/[0-9]/.test(v)) sc++;
  if (/[^A-Za-z0-9]/.test(v)) sc++;
  const cols = ['#ef4444','#f97316','#eab308','#22c55e'];
  const lbls = ['MUY DÉBIL','DÉBIL','MEDIA','FUERTE'];
  for (let i = 0; i < 4; i++) {
    document.getElementById('ss' + i).style.background =
    i < sc ? cols[sc - 1] : 'var(--border2)';
    }
  const lbl = document.getElementById('strLbl');
  lbl.textContent = v.length === 0 ? 'INGRESA UNA CONTRASEÑA' : (lbls[sc-1] || 'MUY DÉBIL');
  lbl.style.color = v.length === 0 ? 'var(--muted)' : cols[sc-1];
  }

  /* STEPS */
  let currentStep = 1;

  function showStep(n) {
    [1, 2, 3].forEach(i => {
      document.getElementById('r' + i).style.display = i === n ? '' : 'none';
      const seg = document.getElementById('s' + (i - 1));
      seg.className = 'step-seg' + (i < n ? ' done' : i === n ? ' active' : '');
    });
  currentStep = n;
  }

  function goStep(n) {
    if (n > currentStep) {
      if (currentStep === 1 && !validateStep1()) return;
  if (currentStep === 2 && !validateStep2()) return;
    }
  showStep(n);
  }

  /* VALIDACIONES */
  function setErr(inputId, errId, show) {
    document.getElementById(inputId).classList.toggle('error', show);
  const e = document.getElementById(errId);
  if (e) e.classList.toggle('show', show);
  return show;
  }

  function validateStep1() {
    let ok = true;
  if (!document.getElementById('rNombre').value.trim())  {setErr('rNombre', 'rNombreErr', true);   ok=false; } else setErr('rNombre','rNombreErr',false);
  if (!document.getElementById('rApellido').value.trim()){setErr('rApellido', 'rApellidoErr', true); ok=false; } else setErr('rApellido','rApellidoErr',false);
  const c = document.getElementById('rCorreo').value;
  if (!c || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(c))       {setErr('rCorreo', 'rCorreoErr', true);    ok=false; } else setErr('rCorreo','rCorreoErr',false);
  if (!document.getElementById('rCedula').value.trim())  {setErr('rCedula', 'rCedulaErr', true);    ok=false; } else setErr('rCedula','rCedulaErr',false);
  return ok;
  }

  function validateStep2() {
    let ok = true;
  const p1 = document.getElementById('rPass').value;
  const p2 = document.getElementById('rPass2').value;
  if (p1.length < 8) {setErr('rPass', 'rPassErr', true); ok=false; }   else setErr('rPass','rPassErr',false);
  if (!p2 || p1!==p2){setErr('rPass2', 'rPass2Err', true); ok=false; } else setErr('rPass2','rPass2Err',false);
  return ok;
  }

  /* LOGIN */
  function doLogin() {
    const email = document.getElementById('lEmail').value;
  const pass  = document.getElementById('lPass').value;
  let ok = true;
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {setErr('lEmail', 'lEmailErr', true); ok=false; } else setErr('lEmail','lEmailErr',false);
  if (!pass) {setErr('lPass', 'lPassErr', true); ok=false; } else setErr('lPass','lPassErr',false);
  if (!ok) return;

  const btn = document.getElementById('btnLogin');
  btn.textContent = 'VERIFICANDO...';
  btn.disabled = true;
  setTimeout(() => {
    btn.textContent = 'INGRESAR';
    btn.disabled = false;
    toast('✓', '¡Bienvenido! Redirigiendo...', false);
    setTimeout(() => {
      window.location.href = "../usuario/perfil.html";
    }, 1000);
  }, 1400);
  }

  /* REGISTRO */
  function doRegister() {
    if (!document.getElementById('terminos').checked) {
    toast('!', 'Debes aceptar los términos', true); return;
    }
  const btn = document.getElementById('btnRegister');
  btn.textContent = 'CREANDO CUENTA...'; btn.disabled = true;
    setTimeout(() => {
    btn.textContent = 'CREAR CUENTA'; btn.disabled = false;
  toast('✓', '¡Cuenta creada! Ya puedes ingresar.', false);
      setTimeout(() => switchTab('login'), 2000);
    }, 1800);
  }

  function toast(icon, msg, isErr) {
    const t = document.getElementById('toast');
  document.getElementById('tIcon').textContent = icon;
  document.getElementById('tMsg').textContent = msg;
  t.classList.toggle('err', isErr);
  t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3000);
  }