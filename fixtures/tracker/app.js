const KEY = 'task-tracker-v1';
const feedback = document.querySelector('#feedback');
const form = document.querySelector('#add-form');
let tasks = [];
let adding = false;
let storageReady = false;
const delay = () => new Promise(resolve => setTimeout(resolve, 200));

// Do not overwrite unreadable saved data with an empty list.
try {
  const saved = JSON.parse(localStorage.getItem(KEY) ?? '[]');
  if (!Array.isArray(saved) || saved.some(task => !task ||
    typeof task.id !== 'string' || typeof task.title !== 'string' ||
    typeof task.note !== 'string' || typeof task.done !== 'boolean') ||
    new Set(saved.map(task => task.id)).size !== saved.length) {
    throw new Error('Invalid saved tasks');
  }
  tasks = saved;
  storageReady = true;
} catch {
  feedback.textContent = 'Could not load saved tasks. Saved data has not been changed. Reload to try again.';
}

function render() {
  const list = document.querySelector('#tasks');
  // Adding a task must not replace another task's pending or failed-save draft.
  const renderedIds = new Set(Array.from(list.children, item => item.dataset.id));
  document.querySelector('#empty').hidden = tasks.length > 0;
  for (const task of tasks) {
    if (renderedIds.has(task.id)) continue;
    const item = document.createElement('li');
    item.dataset.id = task.id;
    const heading = document.createElement('h3');
    heading.textContent = task.title;
    const label = document.createElement('label');
    label.textContent = 'Working note';
    label.htmlFor = `note-${task.id}`;
    const note = document.createElement('textarea');
    note.id = label.htmlFor;
    note.maxLength = 500;
    note.value = task.note;
    const doneLabel = document.createElement('label');
    doneLabel.className = 'check';
    const done = document.createElement('input');
    done.type = 'checkbox';
    done.checked = task.done;
    doneLabel.append(done, 'Completed');
    const save = document.createElement('button');
    save.type = 'button';
    save.textContent = 'Save changes';
    let saving = false;
    save.addEventListener('click', async () => {
      if (saving) return;
      const nextNote = note.value;
      const nextDone = done.checked;
      if (nextNote.length > 500) {
        feedback.textContent = 'Enter a note of up to 500 characters.';
        return;
      }
      saving = true;
      save.disabled = true;
      feedback.textContent = 'Saving…';
      try {
        await delay();
        const next = tasks.map(current => current.id === task.id
          ? { ...current, note: nextNote, done: nextDone } : current);
        localStorage.setItem(KEY, JSON.stringify(next));
        tasks = next;
        feedback.textContent = 'Changes saved.';
      } catch {
        feedback.textContent = 'Could not save. Your existing tasks are unchanged. Try again.';
      } finally {
        saving = false;
        save.disabled = false;
      }
    });
    item.append(heading, label, note, doneLabel, save);
    list.append(item);
  }
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  if (adding || !storageReady) return;
  const title = form.elements.title.value.trim();
  if (!title || title.length > 80) {
    feedback.textContent = 'Enter a title of 1-80 characters.';
    return;
  }
  adding = true;
  document.querySelector('#add').disabled = true;
  feedback.textContent = 'Adding…';
  try {
    await delay();
    const next = [...tasks, { id: crypto.randomUUID(), title, note: '', done: false }];
    localStorage.setItem(KEY, JSON.stringify(next));
    tasks = next;
    form.reset();
    render();
    feedback.textContent = 'Task added.';
  } catch {
    feedback.textContent = 'Could not save. Your existing tasks are unchanged. Try again.';
  } finally {
    adding = false;
    document.querySelector('#add').disabled = false;
  }
});
render();
