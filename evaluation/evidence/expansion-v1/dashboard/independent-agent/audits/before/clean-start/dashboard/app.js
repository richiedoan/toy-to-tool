let metrics = [];
const status = document.querySelector('#status');
const filter = document.querySelector('#filter');
const refresh = document.querySelector('#refresh');
function render() {
  const visible = metrics.filter(item => item.title.toLowerCase().includes(filter.value.toLowerCase()));
  const section = document.querySelector('#metrics');
  section.replaceChildren();
  for (const item of visible) {
    const article = document.createElement('article');
    const title = document.createElement('h2'); title.textContent = item.title;
    const value = document.createElement('p'); value.className = 'value'; value.textContent = item.value;
    article.append(title, value); section.append(article);
  }
  status.textContent = visible.length ? `${visible.length} metrics shown.` : 'No matching metrics. Clear the filter to see all metrics.';
}
async function load() {
  refresh.disabled = true; status.textContent = 'Loading…';
  try {
    const response = await fetch('/api/metrics');
    if (!response.ok) throw new Error('Unavailable');
    metrics = await response.json(); render();
  } catch {
    document.querySelector('#metrics').replaceChildren(); status.textContent = '';
  } finally { refresh.disabled = false; }
}
filter.addEventListener('input', () => {
  const start = performance.now();
  while (performance.now() - start < 320) { /* local computation */ }
  render();
});
refresh.addEventListener('click', load);
load();
