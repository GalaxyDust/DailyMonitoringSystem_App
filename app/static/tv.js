/* TV DMS — satu divisi per layar (R-80), absensi di awal (R-81), QR satu pintu (R-82).
   Panggung tetap 1600x900 lalu diskalakan agar tidak ada tumpang tindih di layar apa pun. */
const PAGES = ['absensi', 'she', 'quality', 'produksi', 'delivery', 'teknik', 'ringkasan'];
const HARI = ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab'];
const BLN = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
const SIKLUS = ['hadir', 'sakit', 'izin', 'alpa', 'terlambat', 'belum pasti'];
const LABEL = { 'belum pasti': 'belum pasti', 'dinas luar': 'dinas luar' };

let S = null, idx = 0, paused = false, timer = null;
const qs = new URLSearchParams(location.search);
const PLANT = qs.get('plant') || 'Snack', LINE = qs.get('line') || '*';

function el(t, c, txt) { const e = document.createElement(t); if (c) e.className = c; if (txt != null) e.textContent = txt; return e; }
function tglID(iso) { const d = new Date(iso + 'T00:00:00'); return `${HARI[d.getDay()]}, ${d.getDate()} ${BLN[d.getMonth()]} ${d.getFullYear()}`; }
function gridCols(w) { return w.map(x => x + 'fr').join(' '); }

function fit() {
  const s = Math.min(innerWidth / 1600, (innerHeight - 26) / 900);
  document.getElementById('stage').style.transform = `scale(${s})`;
}
addEventListener('resize', fit); fit();

async function load(keepPage) {
  const r = await fetch(`/api/state?plant=${encodeURIComponent(PLANT)}&line=${encodeURIComponent(LINE)}&demo=${qs.get('demo') ?? '1'}${qs.get('tanggal') ? '&tanggal=' + qs.get('tanggal') : ''}`);
  S = await r.json();
  if (!keepPage) idx = S.absensi.dikonfirmasi ? 1 : 0;
  render(); schedule();
}

function schedule() {
  clearTimeout(timer);
  if (paused || !S) return;
  if (!S.absensi.dikonfirmasi) { idx = 0; render(); return; }
  const key = PAGES[idx];
  const dur = (key === 'absensi' ? 5 : (S.durasi[key] || 25)) * 1000;
  timer = setTimeout(() => { idx = idx >= PAGES.length - 1 ? 1 : idx + 1; render(); schedule(); }, dur);
}

function head() {
  const key = PAGES[idx];
  const h = S.halaman.find(x => x.key === key);
  document.getElementById('h-plant').textContent = S.plant;
  document.getElementById('h-line').textContent = S.label_line || S.line;
  const badge = document.getElementById('h-badge');
  const sub = document.getElementById('h-sub');
  if (key === 'absensi') { badge.textContent = 'LANGKAH 1 · ABSENSI'; badge.style.background = '#2E868C'; sub.textContent = 'DIKERJAKAN SEBELUM DMS'; }
  else if (key === 'ringkasan') { badge.textContent = 'RINGKASAN LIMA DIVISI'; badge.style.background = '#1B2C57'; sub.textContent = 'AKHIR PUTARAN'; }
  else { badge.textContent = h.nama; badge.style.background = h.warna; badge.style.color = key === 'quality' ? '#2B2B28' : '#fff'; sub.textContent = 'SATU DIVISI PER LAYAR'; }
  if (key !== 'quality') badge.style.color = '#fff';
  document.getElementById('h-date').textContent = tglID(S.tanggal);
  document.getElementById('h-shift').textContent = `Shift ${S.sesi.shift} · PKI 08.30 · sesi ${S.sesi.status}`;
  const b = document.getElementById('banner');
  if (S.demo) { b.className = 'on'; b.textContent = `MODE DEMO · memutar ulang data ${tglID(S.tanggal)} dari reference/ — bukan data hari ini (${tglID(S.hari_ini)}). Angka dihitung dari log kasus asli.`; }
  else { b.className = ''; }
}

function foot() {
  const key = PAGES[idx];
  const h = S.halaman.find(x => x.key === key);
  const syncs = S.halaman.map(x => x.sinkron_terakhir).filter(Boolean).sort();
  const last = syncs.length ? syncs[syncs.length - 1].slice(11, 16).replace(':', '.') : '—';
  document.getElementById('f-sync').textContent = `Sinkron Excel ${last}`;
  document.getElementById('f-src').textContent = 'SUMBER: EXCEL';
  const a = S.absensi.hitung;
  let extra = `·  Hadir ${a.hadir || 0}/${S.absensi.total}`;
  if (h && h.status !== 'tersinkron') extra += `  ·  ${h.status.replace(/_/g, ' ')}`;
  if (!S.absensi.dikonfirmasi) extra += '  ·  absensi belum dikonfirmasi';
  document.getElementById('f-extra').textContent = extra;
  document.getElementById('f-page').textContent = `Halaman ${idx + 1}/${PAGES.length}`;
  const dots = document.getElementById('f-dots'); dots.innerHTML = '';
  PAGES.forEach((_, i) => { const d = el('i'); if (i === idx) d.className = 'on'; dots.appendChild(d); });
  document.body.className = paused ? 'paused' : '';
}

function kpiBlock(h) {
  const wrap = el('div', 'kpi');
  const periods = ['Target', 'S1', 'S2', 'S3', 'Harian', 'Minggu', 'Bulan'];
  const cols = '1fr ' + periods.map(() => '96px').join(' ');
  const hd = el('div', 'kpi-head'); hd.style.gridTemplateColumns = cols; hd.style.background = h.warna;
  hd.appendChild(el('div', null, 'KPI · dihitung dari log kasus Excel'));
  periods.forEach(p => hd.appendChild(el('div', null, p)));
  if (h.key === 'quality') hd.style.color = '#2B2B28';
  wrap.appendChild(hd);
  h.kpi.forEach(k => {
    const row = el('div', 'kpi-row'); row.style.gridTemplateColumns = cols;
    row.appendChild(el('div', 'item', k.item));
    row.appendChild(el('div', 'tgt', k.target));
    k.vals.forEach((v, i) => {
      const c = el('div', 'val s' + v.st + (i === 3 ? ' now' : ''));
      c.appendChild(el('span', null, v.v)); row.appendChild(c);
    });
    wrap.appendChild(row);
  });
  return wrap;
}

function tableBlock(h) {
  const t = el('div', 'tbl');
  const title = el('div', 'tbl-title');
  const sheets = [...new Set(h.berkas.map(b => b.sheet).filter(Boolean))].join(', ');
  title.appendChild(el('span', null, `KASUS · sheet ${sheets || '—'} · ${h.jumlah} baris pada tanggal ini`));
  title.appendChild(el('small', null, 'kolom mengikuti Excel (R-83) · angka tidak diubah dari TV'));
  t.appendChild(title);
  const cols = gridCols(h.kolom.map(c => c.bobot));
  const hd = el('div', 'tbl-head'); hd.style.gridTemplateColumns = cols;
  h.kolom.forEach(c => hd.appendChild(el('div', null, c.nama)));
  t.appendChild(hd);
  const body = el('div', 'tbl-body');
  const rows = h.baris.slice(0, 6);
  const rh = rows.length ? Math.max(38, Math.floor(300 / rows.length)) : 44;
  rows.forEach(r => {
    const row = el('div', 'tbl-row'); row.style.gridTemplateColumns = cols; row.style.height = rh + 'px';
    h.kolom.forEach((c, i) => {
      let cls = '';
      if (c.nama === 'Status') cls = 'st-' + r.status;
      else if (['Tgl', 'Tanggal', 'Date', 'Shift', 'LBN', 'PIC', 'Due', 'PO', 'Mesin'].includes(c.nama)) cls = 'blue';
      else if (['Prioritas', 'Umur', 'DT (min)', 'O / R'].includes(c.nama) && !['—', '0', 'Rendah'].includes(r.sel[i])) cls = 'red';
      const cell = el('div', cls, r.sel[i]);
      cell.title = r.sel[i] + (r.flag ? '  ⚠ ' + r.flag : '');
      if (r.flag && c.nama === 'PIC') cell.className += ' flagged';
      row.appendChild(cell);
    });
    body.appendChild(row);
  });
  t.appendChild(body);
  return t;
}

function picaBlock(h) {
  const p = el('div', 'pica');
  const cols = '0.9fr 1.5fr 1.5fr 0.5fr 0.4fr 0.5fr';
  const hd = el('div', 'pica-head'); hd.style.gridTemplateColumns = cols;
  ['PICA TERBUKA', 'Problem', 'Rootcause', 'Action', 'PIC', 'Due', 'Status'].forEach(x => hd.appendChild(el('div', null, x)));
  p.appendChild(hd);
  const open = h.baris.filter(b => b.status !== 'CLOSE').slice(0, 2);
  const gi = n => h.kolom.findIndex(c => c.nama === n);
  open.forEach(b => {
    const row = el('div', 'pica-row'); row.style.gridTemplateColumns = cols;
    const pick = names => { for (const n of names) { const i = gi(n); if (i >= 0) return b.sel[i]; } return '—'; };
    row.appendChild(el('div', null, pick(['Problem Statement', 'Problem'])));
    row.appendChild(el('div', null, pick(['RootCause', 'Root Cause'])));
    row.appendChild(el('div', null, pick(['Action Plan', 'Corrective / Preventive'])));
    row.appendChild(el('div', 'b', pick(['PIC'])));
    row.appendChild(el('div', 'b', pick(['Due'])));
    row.appendChild(el('div', 'r', b.status));
    p.appendChild(row);
  });
  if (!open.length) { const row = el('div', 'pica-row'); row.style.gridTemplateColumns = '1fr'; row.appendChild(el('div', null, 'Tidak ada PICA terbuka pada tanggal ini.')); p.appendChild(row); }
  return p;
}

function emptyBlock(h) {
  const e = el('div', 'empty');
  const tag = el('div', 'tag tag-' + h.status, h.status.replace(/_/g, ' ').toUpperCase());
  e.appendChild(tag);
  const judul = { menunggu_berkas: 'Menunggu berkas divisi', belum_diisi: 'Belum ada isian tanggal ini', belum_tersinkron: 'Belum tersinkron' };
  e.appendChild(el('h2', null, judul[h.status] || h.status));
  e.appendChild(el('p', null, h.pesan + '. Halaman ini tetap tampil dan tidak dilewati (R-84) — supaya jelas siapa yang belum mengisi, bukan layar mati.'));
  if (h.berkas.length) e.appendChild(el('div', 'files', h.berkas.map(b => `${b.id} · ${b.path} · ${b.sheet || '?'} · ${b.status}`).join('\n')));
  else e.appendChild(el('div', 'files', 'Daftarkan berkasnya di app/registry.json — tidak perlu membuat form baru (R-86).'));
  return e;
}

function pageDivisi(h) {
  const f = document.createDocumentFragment();
  if (h.status !== 'tersinkron') { f.appendChild(emptyBlock(h)); return f; }
  f.appendChild(kpiBlock(h));
  f.appendChild(tableBlock(h));
  f.appendChild(picaBlock(h));
  return f;
}

function pageAbsensi() {
  const a = S.absensi, hit = a.hitung;
  const w = el('div', 'abs-wrap');
  const left = el('div', 'abs-left');
  const sum = el('div', 'abs-sum');
  sum.appendChild(el('div', 'big', String(hit.hadir || 0)));
  const txt = el('div');
  txt.appendChild(el('div', 'lbl', `hadir dari ${a.total} orang`));
  txt.appendChild(el('div', 'det', `${hit.sakit || 0} sakit · ${hit.izin || 0} izin · ${hit.alpa || 0} alpa · ${hit['belum pasti'] || 0} belum pasti`));
  sum.appendChild(txt);
  const bar = el('div', 'bar'); const fill = el('i'); fill.style.width = (100 * (hit.hadir || 0) / a.total) + '%'; bar.appendChild(fill);
  sum.appendChild(bar);
  left.appendChild(sum);
  const g = el('div', 'abs-grid');
  a.nama.forEach(n => {
    const cls = n.status === 'hadir' ? '' : (n.status === 'sakit' ? 'sakit' : (n.status === 'belum pasti' ? 'belum' : 'izin'));
    const c = el('div', 'chip ' + cls);
    c.appendChild(el('div', 'av', n.nama.slice(0, 2).toUpperCase()));
    const box = el('div');
    box.appendChild(el('div', 'nm', n.nama));
    box.appendChild(el('div', 'stt', LABEL[n.status] || n.status));
    c.appendChild(box);
    c.onclick = async () => {
      if (S.absensi.dikonfirmasi) return;
      const next = SIKLUS[(SIKLUS.indexOf(n.status) + 1) % SIKLUS.length];
      await fetch('/api/absensi', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ nama: n.nama, status: next, plant: PLANT, line: LINE, perangkat: 'tv' }) });
      await load(true);
    };
    g.appendChild(c);
  });
  left.appendChild(g);
  w.appendChild(left);

  const right = el('div', 'abs-right');
  right.appendChild(el('div', 'hd', 'SATU PINTU · QR SESI'));
  const inside = el('div', 'in');
  const img = el('img'); img.src = `/qr/${S.sesi.token}.png`; img.alt = 'QR sesi DMS';
  inside.appendChild(img);
  inside.appendChild(el('div', 'u', 'Pindai untuk absen & masuk DMS'));
  inside.appendChild(el('div', 'v', `berlaku Shift ${S.sesi.shift} · ${S.label_line || S.line} · token berputar tiap shift`));
  const steps = el('div', 'steps');
  [['1', 'Absensi', S.absensi.dikonfirmasi ? 'SELESAI' : 'AKTIF · wajib dulu', true],
   ['2', 'Data divisi', S.absensi.dikonfirmasi ? 'TERBUKA' : 'terkunci', S.absensi.dikonfirmasi],
   ['3', 'Review & kunci', 'otomatis', false]].forEach(([n, l, t, on]) => {
    const s = el('div', 'step' + (on ? ' on' : ''));
    s.appendChild(el('div', 'n', n)); s.appendChild(el('div', null, l)); s.appendChild(el('div', 'tag', t));
    steps.appendChild(s);
  });
  inside.appendChild(steps);
  const btn = el('button', 'go', S.absensi.dikonfirmasi ? 'KEHADIRAN TERKONFIRMASI' : 'KONFIRMASI KEHADIRAN');
  btn.disabled = S.absensi.dikonfirmasi;
  btn.onclick = async () => {
    await fetch('/api/konfirmasi', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ plant: PLANT, line: LINE, pelaku: 'leader' }) });
    await load(false); idx = 1; render(); schedule();
  };
  inside.appendChild(btn);
  inside.appendChild(el('div', 'note', 'Data divisi sudah masuk dari Excel masing-masing — tidak perlu isi ulang (R-88). Isian divisi terbuka setelah kehadiran dikonfirmasi (R-81). Supervisor/DH dapat membuka ulang dengan alasan tercatat.'));
  right.appendChild(inside);
  w.appendChild(right);
  return w;
}

function pageRingkasan() {
  const f = document.createDocumentFragment();
  const g = el('div', 'ring');
  S.ringkasan.forEach(r => {
    const c = el('div', 'rcard');
    const h = el('div', 'rh', r.nama.split(' / ')[0]); h.style.background = r.warna;
    if (r.key === 'quality') h.style.color = '#2B2B28';
    c.appendChild(h);
    const b = el('div', 'rb');
    b.appendChild(el('div', 'num', r.status === 'tersinkron' ? String(r.jumlah) : '—'));
    b.appendChild(el('div', 'cap', 'kasus tanggal ini'));
    [['Open', r.open], ['Completion', r.completion], ['Lewat tenggat', r.lewat]].forEach(([k, v]) => {
      const kv = el('div', 'kv'); kv.appendChild(el('span', null, k)); kv.appendChild(el('b', null, v)); b.appendChild(kv);
    });
    c.appendChild(b);
    const st = el('div', 'stt', r.status.replace(/_/g, ' '));
    st.style.color = r.status === 'tersinkron' ? '#1E6B3A' : (r.status === 'belum_tersinkron' ? '#B02F2F' : '#8A6C10');
    c.appendChild(st);
    g.appendChild(c);
  });
  f.appendChild(g);
  const note = el('div', 'rfoot');
  note.textContent = `Semua angka dihitung dari log kasus pada berkas Excel tiap divisi — aplikasi tidak menulis ke workbook (R-85) dan tidak meminta petugas mengunggah apa pun (R-88).Kolom milik Excel baca-saja; koreksi dilakukan di Excel lalu layar ini menyusul otomatis (R-89). Pengawas folder aktif: putaran ${S.pengawas.putaran}, perubahan terakhir ${S.pengawas.terakhir || 'belum ada'}.`;
  f.appendChild(note);
  return f;
}

function render() {
  if (!S) return;
  head();
  const body = document.getElementById('body');
  body.innerHTML = '';
  const key = PAGES[idx];
  if (key === 'absensi') body.appendChild(pageAbsensi());
  else if (key === 'ringkasan') body.appendChild(pageRingkasan());
  else body.appendChild(pageDivisi(S.halaman.find(x => x.key === key)));
  foot();
}

addEventListener('keydown', async e => {
  if (e.key === 'ArrowRight') { idx = (idx + 1) % PAGES.length; render(); schedule(); }
  if (e.key === 'ArrowLeft') { idx = (idx - 1 + PAGES.length) % PAGES.length; render(); schedule(); }
  if (e.key === ' ') { e.preventDefault(); paused = !paused; render(); schedule(); }
  if (e.key.toLowerCase() === 'a') { idx = 0; render(); schedule(); }
  if (e.key.toLowerCase() === 's') { await fetch('/api/sync', { method: 'POST' }); await load(true); }
});

load(false);
setInterval(() => load(true), 15000);