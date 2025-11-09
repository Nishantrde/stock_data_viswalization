// static/js/app.js
async function loadCompanies() {
  const res = await fetch('/companies');
  const data = await res.json();
  const list = document.getElementById('company-list');
  data.companies.forEach(sym => {
    const li = document.createElement('li');
    const btn = document.createElement('button');
    btn.textContent = sym;
    btn.onclick = () => loadSymbol(sym);
    li.appendChild(btn);
    list.appendChild(li);
  });
}

let chart = null;
async function loadSymbol(sym) {
  const res = await fetch(`/data/${encodeURIComponent(sym)}?days=90`);
  if (!res.ok) { alert('error fetching data'); return; }
  const payload = await res.json();
  const rows = payload.data;
  const labels = rows.map(r => r.Date);
  const closes = rows.map(r => r.Close);
  if (chart) chart.destroy();
  const ctx = document.getElementById('priceChart').getContext('2d');
  chart = new Chart(ctx, {
    type: 'line',
    data: { labels, datasets: [{ label: sym + ' Close', data: closes, fill:false }] },
    options: {}
  });
}

loadCompanies();
