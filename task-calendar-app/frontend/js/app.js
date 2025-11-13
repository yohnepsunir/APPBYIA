const apiUrl = 'http://localhost:5000/api/tasks';

let currentTaskId = null;
let tasks = [];

// Elementos del DOM
const taskForm = document.getElementById('taskForm');
const tasksList = document.getElementById('tasksList');
const attachmentsList = document.getElementById('attachmentsList');
const btnNewTask = document.getElementById('btnNewTask');
const btnDelete = document.getElementById('btnDelete');
const btnClear = document.getElementById('btnClear');
const btnUpload = document.getElementById('btnUpload');
const fileInput = document.getElementById('fileInput');

// Inicializar aplicación
document.addEventListener('DOMContentLoaded', async () => {
    await loadTasks();
    setupEventListeners();
});

function setupEventListeners() {
    btnNewTask.addEventListener('click', newTask);
    taskForm.addEventListener('submit', saveTask);
    btnDelete.addEventListener('click', deleteTask);
    btnClear.addEventListener('click', clearForm);
    btnUpload.addEventListener('click', uploadFile);
}

async function loadTasks() {
    tasks = await TaskAPI.getTasks();
    renderTaskList();
}

function renderTaskList() {
    tasksList.innerHTML = '';
    tasks.forEach(task => {
        const taskEl = document.createElement('div');
        taskEl.className = `task-item priority-${task.priority} status-${task.status}`;
        taskEl.innerHTML = `
            <div class="task-header">
                <strong>${task.title}</strong>
                <span class="priority-badge">P${task.priority}</span>
            </div>
            <small>${task.category || 'Sin categoría'}</small>
            <p>${task.description ? task.description.substring(0, 50) + '...' : 'Sin descripción'}</p>
            <small>Vence: ${task.due_date || 'Sin fecha'}</small>
        `;
        taskEl.addEventListener('click', () => editTask(task.id));
        tasksList.appendChild(taskEl);
    });
}

function newTask() {
    clearForm();
    currentTaskId = null;
    document.getElementById('title').focus();
}

async function editTask(id) {
    currentTaskId = id;
    const task = await TaskAPI.getTask(id);
    if (task) {
        document.getElementById('taskId').value = task.id;
        document.getElementById('title').value = task.title;
        document.getElementById('description').value = task.description || '';
        document.getElementById('category').value = task.category || '';
        document.getElementById('priority').value = task.priority || 3;
        document.getElementById('due_date').value = task.due_date || '';
        document.getElementById('status').value = task.status || 'pending';
        btnDelete.style.display = 'inline-block';
        
        // Cargar adjuntos de esta tarea
        loadAttachments(id);
    }
}

async function saveTask(e) {
    e.preventDefault();
    
    const data = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        category: document.getElementById('category').value,
        priority: parseInt(document.getElementById('priority').value),
        due_date: document.getElementById('due_date').value,
        status: document.getElementById('status').value
    };

    if (!data.title.trim()) {
        alert('El título es requerido');
        return;
    }

    let result;
    if (currentTaskId) {
        result = await TaskAPI.updateTask(currentTaskId, data);
    } else {
        result = await TaskAPI.createTask(data);
        if (result) {
            currentTaskId = result.id;
        }
    }

    if (result) {
        await loadTasks();
        alert('Tarea guardada exitosamente');
    } else {
        alert('Error al guardar la tarea');
    }
}

async function deleteTask(e) {
    e.preventDefault();
    if (!currentTaskId) return;
    
    if (confirm('¿Estás seguro de que deseas eliminar esta tarea?')) {
        const result = await TaskAPI.deleteTask(currentTaskId);
        if (result) {
            await loadTasks();
            clearForm();
            alert('Tarea eliminada');
        }
    }
}

function clearForm() {
    taskForm.reset();
    currentTaskId = null;
    document.getElementById('taskId').value = '';
    btnDelete.style.display = 'none';
    attachmentsList.innerHTML = '';
}

function loadAttachments(taskId) {
    attachmentsList.innerHTML = '';
    
    // Buscar todos los adjuntos en localStorage
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key.startsWith('attachment_')) {
            const attachment = LocalStorage.getItem(key);
            if (attachment && attachment.taskId === taskId) {
                displayAttachment(attachment, key);
            }
        }
    }
}

function uploadFile() {
    if (!currentTaskId) {
        alert('Debes seleccionar una tarea primero');
        return;
    }

    const files = fileInput.files;
    if (files.length === 0) {
        alert('Selecciona un archivo');
        return;
    }
    
    // Guardar en localStorage
    Array.from(files).forEach(file => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const attachment = {
                name: file.name,
                size: file.size,
                type: file.type,
                taskId: currentTaskId,
                data: e.target.result
            };
            LocalStorage.setItem(`attachment_${Date.now()}`, attachment);
            displayAttachment(attachment);
        };
        reader.readAsDataURL(file);
    });
    
    fileInput.value = '';
    alert('Archivos cargados exitosamente');
}

function displayAttachment(attachment, storageKey = null) {
    const attachmentEl = document.createElement('div');
    attachmentEl.className = 'attachment-item';
    
    const sizeKB = (attachment.size / 1024).toFixed(2);
    
    attachmentEl.innerHTML = `
        <div>
            <strong>${attachment.name}</strong>
            <small>(${sizeKB} KB)</small>
            <br>
            <a href="${attachment.data}" download="${attachment.name}" class="btn-download">Descargar</a>
            ${storageKey ? `<button class="btn-danger" onclick="deleteAttachment('${storageKey}')" style="padding: 5px 10px; font-size: 12px;">Eliminar</button>` : ''}
        </div>
    `;
    attachmentsList.appendChild(attachmentEl);
}

function deleteAttachment(storageKey) {
    if (confirm('¿Deseas eliminar este archivo?')) {
        LocalStorage.removeItem(storageKey);
        loadAttachments(currentTaskId);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    fetchTasks();
    const form = document.getElementById('task-form');
    form.onsubmit = createTask;
});