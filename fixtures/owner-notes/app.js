const status = document.querySelector('#status');
async function request(path, options = {}) {
  const response = await fetch(path, { ...options, headers: { 'Content-Type': 'application/json' } });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error);
  return data;
}
async function load() {
  const notes = await request('/api/notes');
  const list = document.querySelector('#notes');
  list.replaceChildren();
  for (const record of notes) {
    const item = document.createElement('li');
    const label = document.createElement('label');
    label.textContent = 'Working note'; label.htmlFor = record.id;
    const input = document.createElement('textarea');
    input.id = record.id; input.maxLength = 1000; input.value = record.text;
    const save = document.createElement('button'); save.textContent = 'Save note';
    save.addEventListener('click', async () => {
      save.disabled = true; status.textContent = 'Saving…';
      try { await request(`/api/notes/${record.id}`, { method: 'PATCH', body: JSON.stringify({ text: input.value }) }); status.textContent = 'Note saved.'; }
      catch (error) { status.textContent = error.message; }
      finally { save.disabled = false; }
    });
    item.append(label, input, save); list.append(item);
  }
}
document.querySelector('#login').addEventListener('submit', async event => {
  event.preventDefault();
  try {
    await request('/api/login', { method: 'POST', body: JSON.stringify({ username: document.querySelector('#username').value, password: document.querySelector('#password').value }) });
    document.querySelector('#password').value = '';
    await load(); document.querySelector('#login').hidden = true; document.querySelector('#workspace').hidden = false; status.textContent = 'Your notes are ready.';
  } catch (error) { status.textContent = error.message; }
});
document.querySelector('#logout').addEventListener('click', async () => {
  try { await request('/api/logout', { method: 'POST', body: '{}' }); document.querySelector('#workspace').hidden = true; document.querySelector('#notes').replaceChildren(); document.querySelector('#login').hidden = false; status.textContent = 'Signed out.'; }
  catch (error) { status.textContent = error.message; }
});
