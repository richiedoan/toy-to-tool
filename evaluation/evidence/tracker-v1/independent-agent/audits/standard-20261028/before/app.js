const KEY = 'task-tracker-v1';
const feedback = document.querySelector('#feedback');
const form = document.querySelector('#add-form');
let tasks = [];
const delay = () => new Promise(resolve => setTimeout(resolve, 200));

function render() {
  const list = document.querySelector('#tasks');
  list.replaceChildren();
  document.querySelector('#empty').hidden = tasks.length > 0;
  for (const task of tasks) {
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
    save.addEventListener('click', async () => {
      feedback.textContent = 'Saving…';
      await delay();
      feedback.textContent = 'Changes saved.';
    });
    item.append(heading, label, note, doneLabel, save);
    list.append(item);
  }
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  const title = form.elements.title.value.trim();
  if (!title || title.length > 80) {
    feedback.textContent = 'Enter a title of 1-80 characters.';
    return;
  }
  feedback.textContent = 'Adding…';
  await delay();
  const next = [...tasks, { id: crypto.randomUUID(), title, note: '', done: false }];
  try {
    localStorage.setItem(KEY, JSON.stringify(next));
    tasks = next;
    form.reset();
    render();
    feedback.textContent = 'Task added.';
  } catch {
    feedback.textContent = 'Could not save. Your existing tasks are unchanged. Try again.';
  }
});
render();
