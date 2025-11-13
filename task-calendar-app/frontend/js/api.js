const API_URL = '/api/tasks';

class TaskAPI {
    static async getTasks() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error('Error al obtener tareas');
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return [];
        }
    }

    static async getTask(id) {
        try {
            const response = await fetch(`${API_URL}/${id}`);
            if (!response.ok) throw new Error('Error al obtener tarea');
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    }

    static async createTask(data) {
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Error al crear tarea');
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    }

    static async updateTask(id, data) {
        try {
            const response = await fetch(`${API_URL}/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Error al actualizar tarea');
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    }

    static async deleteTask(id) {
        try {
            const response = await fetch(`${API_URL}/${id}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error('Error al eliminar tarea');
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    }
}