
  // Date
  const d = new Date();
  const opts = { weekday:'long', year:'numeric', month:'long', day:'numeric' };
  document.getElementById('dateDisplay').textContent = d.toLocaleDateString('es-MX', opts).toUpperCase();

  // Nav
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
  const today = new Date().getDay(); // 0=Sun
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

  function saveNewMember() {
    closeModal();
    setTimeout(() => showToast('Miembro registrado correctamente'), 200);
  }

  // Animate ring on load
  window.addEventListener('load', () => {
    const ring = document.getElementById('ringCircle');
    const circumference = 264;
    const offset = circumference * (1 - 0.68);
    ring.style.strokeDashoffset = offset;
  });