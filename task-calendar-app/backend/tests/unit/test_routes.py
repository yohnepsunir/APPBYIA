"""
Tests unitarios para las rutas de la API
"""
import pytest
import json
from models import Task


class TestTaskRoutes:
    """Tests para las rutas de tasks"""
    
    def test_get_tasks_empty(self, client, db_connection):
        """Test GET /api/tasks sin tareas"""
        response = client.get('/api/tasks')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_tasks_with_data(self, client, db_connection, create_sample_tasks):
        """Test GET /api/tasks con tareas"""
        response = client.get('/api/tasks')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 3
    
    def test_get_task_by_id_success(self, client, db_connection, sample_task_data):
        """Test GET /api/tasks/<id> exitoso"""
        # Crear tarea
        task_id = Task.create(
            sample_task_data['title'],
            sample_task_data['description'],
            sample_task_data['category'],
            sample_task_data['priority'],
            sample_task_data['due_date']
        )
        
        # Obtener tarea
        response = client.get(f'/api/tasks/{task_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == task_id
        assert data['title'] == sample_task_data['title']
    
    def test_get_task_by_id_not_found(self, client, db_connection):
        """Test GET /api/tasks/<id> con ID inexistente"""
        response = client.get('/api/tasks/9999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Task not found'
    
    def test_create_task_success(self, client, db_connection, sample_task_data):
        """Test POST /api/tasks exitoso"""
        response = client.post(
            '/api/tasks',
            data=json.dumps(sample_task_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'id' in data
        assert 'message' in data
        assert data['message'] == 'Task created'
        
        # Verificar que se creó en la BD
        task = Task.get_by_id(data['id'])
        assert task is not None
        assert task['title'] == sample_task_data['title']
    
    def test_create_task_minimal_data(self, client, db_connection):
        """Test POST /api/tasks con datos mínimos"""
        minimal_data = {'title': 'Minimal Task'}
        
        response = client.post(
            '/api/tasks',
            data=json.dumps(minimal_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'id' in data
        
        # Verificar valores por defecto
        task = Task.get_by_id(data['id'])
        assert task['title'] == 'Minimal Task'
        assert task['description'] == ''
        assert task['priority'] == 3
        assert task['status'] == 'pending'
    
    def test_create_task_missing_title(self, client, db_connection):
        """Test POST /api/tasks sin título (requerido)"""
        invalid_data = {'description': 'No title'}
        
        response = client.post(
            '/api/tasks',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_update_task_success(self, client, db_connection, sample_task_data):
        """Test PUT /api/tasks/<id> exitoso"""
        # Crear tarea
        task_id = Task.create(
            sample_task_data['title'],
            sample_task_data['description'],
            sample_task_data['category'],
            sample_task_data['priority'],
            sample_task_data['due_date']
        )
        
        # Actualizar tarea
        updated_data = sample_task_data.copy()
        updated_data['title'] = 'Updated Title'
        updated_data['status'] = 'completed'
        
        response = client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Task updated'
        
        # Verificar actualización en BD
        task = Task.get_by_id(task_id)
        assert task['title'] == 'Updated Title'
        assert task['status'] == 'completed'
    
    def test_update_task_invalid_data(self, client, db_connection, sample_task_data):
        """Test PUT /api/tasks/<id> con datos inválidos"""
        task_id = Task.create(
            sample_task_data['title'],
            sample_task_data['description'],
            sample_task_data['category'],
            sample_task_data['priority'],
            sample_task_data['due_date']
        )
        
        # Datos inválidos (sin título)
        invalid_data = {'description': 'No title'}
        
        response = client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_delete_task_success(self, client, db_connection, sample_task_data):
        """Test DELETE /api/tasks/<id> exitoso"""
        # Crear tarea
        task_id = Task.create(
            sample_task_data['title'],
            sample_task_data['description'],
            sample_task_data['category'],
            sample_task_data['priority'],
            sample_task_data['due_date']
        )
        
        # Eliminar tarea
        response = client.delete(f'/api/tasks/{task_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Task deleted'
        
        # Verificar que se eliminó
        task = Task.get_by_id(task_id)
        assert task is None
    
    def test_health_endpoint(self, client):
        """Test del endpoint /api/health"""
        response = client.get('/api/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
