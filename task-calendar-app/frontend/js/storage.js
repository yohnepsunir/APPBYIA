class LocalStorage {
    static setItem(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error('Error al guardar en localStorage:', error);
        }
    }

    static getItem(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (error) {
            console.error('Error al obtener de localStorage:', error);
            return null;
        }
    }

    static removeItem(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error('Error al eliminar de localStorage:', error);
        }
    }

    static clear() {
        try {
            localStorage.clear();
        } catch (error) {
            console.error('Error al limpiar localStorage:', error);
        }
    }
}

function saveTaskToLocalStorage(task) {
    let tasks = getTasksFromLocalStorage();
    tasks.push(task);
    LocalStorage.setItem('tasks', tasks);
}

function getTasksFromLocalStorage() {
    const tasks = LocalStorage.getItem('tasks');
    return tasks ? JSON.parse(tasks) : [];
}

function updateTaskInLocalStorage(updatedTask) {
    let tasks = getTasksFromLocalStorage();
    tasks = tasks.map(task => task.id === updatedTask.id ? updatedTask : task);
    LocalStorage.setItem('tasks', tasks);
}

function deleteTaskFromLocalStorage(taskId) {
    let tasks = getTasksFromLocalStorage();
    tasks = tasks.filter(task => task.id !== taskId);
    LocalStorage.setItem('tasks', tasks);
}

function clearLocalStorage() {
    LocalStorage.clear();
}