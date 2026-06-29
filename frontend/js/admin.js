const API_BASE = localStorage.getItem('apiBase') || 'http://127.0.0.1:5000';
const resources = {
  courses: ['department_id', 'name', 'degree', 'duration', 'eligibility', 'description', 'is_active'],
  departments: ['name', 'short_name', 'description', 'level', 'is_active'],
  fees: ['course_id', 'category', 'amount', 'notes'],
  admission: ['title', 'process_steps', 'eligibility', 'required_documents', 'important_dates'],
  placements: ['title', 'details', 'companies', 'training_support'],
  hostel: ['title', 'facilities', 'transport_details'],
  scholarships: ['name', 'eligibility', 'details'],
  contact: ['college_name', 'address', 'phone', 'email', 'website'],
  faculty: ['department_id', 'name', 'designation', 'qualification', 'specialization'],
  faqs: ['question', 'answer', 'category', 'is_active']
};

let token = localStorage.getItem('adminToken') || '';
let currentResource = 'courses';
let editingId = null;

const nav = document.getElementById('resourceNav');
const loginForm = document.getElementById('loginForm');
const crudArea = document.getElementById('crudArea');
const crudForm = document.getElementById('crudForm');
const records = document.getElementById('records');
const resourceTitle = document.getElementById('resourceTitle');
const logoutBtn = document.getElementById('logoutBtn');

function titleCase(text) {
  return text.replace(/_/g, ' ').replace(/w/g, (char) => char.toUpperCase());
}

function authHeaders() {
  return { 'Content-Type': 'application/json', Authorization: 'Bearer ' + token };
}

function renderNav() {
  nav.innerHTML = '';
  Object.keys(resources).forEach((resource) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = titleCase(resource);
    button.addEventListener('click', () => loadResource(resource));
    nav.appendChild(button);
  });
}

function renderForm(values = {}) {
  crudForm.innerHTML = '';
  resources[currentResource].forEach((field) => {
    const input = ['description', 'eligibility', 'details', 'notes', 'process_steps', 'required_documents', 'important_dates', 'facilities', 'transport_details', 'training_support', 'answer'].includes(field)
      ? document.createElement('textarea')
      : document.createElement('input');
    input.name = field;
    input.placeholder = titleCase(field);
    input.value = values[field] ?? '';
    if (field.startsWith('is_')) input.placeholder += ' (1 or 0)';
    crudForm.appendChild(input);
  });
  const button = document.createElement('button');
  button.type = 'submit';
  button.textContent = editingId ? 'Update Record' : 'Add Record';
  crudForm.appendChild(button);
}

function recordSummary(row) {
  return row.name || row.title || row.question || row.college_name || row.category || 'Record #' + row.id;
}

function renderRecords(rows) {
  records.innerHTML = '';
  rows.forEach((row) => {
    const card = document.createElement('article');
    card.className = 'record';
    const heading = document.createElement('h3');
    heading.textContent = recordSummary(row);
    const text = document.createElement('p');
    text.textContent = Object.entries(row).filter(([key]) => key !== 'id').map(([key, value]) => titleCase(key) + ': ' + (value ?? '')).join(' | ');
    const actions = document.createElement('div');
    actions.className = 'record-actions';
    const edit = document.createElement('button');
    edit.type = 'button';
    edit.textContent = 'Edit';
    edit.addEventListener('click', () => { editingId = row.id; renderForm(row); window.scrollTo({ top: 0, behavior: 'smooth' }); });
    const del = document.createElement('button');
    del.type = 'button';
    del.textContent = 'Delete';
    del.addEventListener('click', () => deleteRecord(row.id));
    actions.append(edit, del);
    card.append(heading, text, actions);
    records.appendChild(card);
  });
}

async function loadResource(resource) {
  currentResource = resource;
  editingId = null;
  resourceTitle.textContent = titleCase(resource);
  renderForm();
  const response = await fetch(API_BASE + '/admin/' + resource, { headers: authHeaders() });
  const data = await response.json();
  if (!response.ok) throw new Error(data.message || 'Failed to load records');
  renderRecords(data.data || []);
}

async function deleteRecord(id) {
  if (!confirm('Delete this record?')) return;
  await fetch(API_BASE + '/admin/' + currentResource + '/' + id, { method: 'DELETE', headers: authHeaders() });
  loadResource(currentResource);
}

loginForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const payload = { email: document.getElementById('adminEmail').value, password: document.getElementById('adminPassword').value };
  const response = await fetch(API_BASE + '/admin/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  const data = await response.json();
  if (!response.ok) return alert(data.message || 'Login failed');
  token = data.data.token;
  localStorage.setItem('adminToken', token);
  loginForm.classList.add('hidden');
  crudArea.classList.remove('hidden');
  loadResource(currentResource);
});

crudForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(crudForm).entries());
  Object.keys(payload).forEach((key) => { if (payload[key] === '') delete payload[key]; });
  const url = API_BASE + '/admin/' + currentResource + (editingId ? '/' + editingId : '');
  const response = await fetch(url, { method: editingId ? 'PUT' : 'POST', headers: authHeaders(), body: JSON.stringify(payload) });
  const data = await response.json();
  if (!response.ok) return alert(data.message || 'Save failed');
  editingId = null;
  renderForm();
  loadResource(currentResource);
});

logoutBtn.addEventListener('click', () => {
  localStorage.removeItem('adminToken');
  token = '';
  loginForm.classList.remove('hidden');
  crudArea.classList.add('hidden');
  resourceTitle.textContent = 'Login';
});

renderNav();
if (token) {
  loginForm.classList.add('hidden');
  crudArea.classList.remove('hidden');
  loadResource(currentResource).catch(() => logoutBtn.click());
}
