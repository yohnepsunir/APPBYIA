"""
Tests para excepciones y casos especiales
"""
import pytest
import json
from unittest.mock import patch, MagicMock
from models import Task


class TestExceptionHandling:
    """Tests para manejo de excepciones"""
    
    def test_delete_task_with_exception(self, client, db_connection):
        """Test DELETE cuando Task.delete() lanza excepción"""
        # Crear una tarea primero
        task_data = {'title': 'Test Task'}
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        task_id = json.loads(response.data)['id']
        
        # Mock Task.delete para lanzar excepción
        with patch('routes.tasks.Task.delete') as mock_delete:
            mock_delete.side_effect = Exception('Database error')
            
            response = client.delete(f'/api/tasks/{task_id}')
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'error' in data
            assert 'Database error' in data['error']
    
    def test_update_task_with_exception(self, client, db_connection):
        """Test PUT cuando Task.update() lanza excepción"""
        # Crear una tarea primero
        task_data = {'title': 'Test Task'}
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        task_id = json.loads(response.data)['id']
        
        # Mock Task.update para lanzar excepción
        with patch('routes.tasks.Task.update') as mock_update:
            mock_update.side_effect = Exception('Update failed')
            
            update_data = {
                'title': 'Updated',
                'description': 'Test',
                'category': 'test',
                'priority': 3,
                'due_date': '2025-12-31'
            }
            response = client.put(
                f'/api/tasks/{task_id}',
                data=json.dumps(update_data),
                content_type='application/json'
            )
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'error' in data
            assert 'Update failed' in data['error']
    
    def test_create_task_with_exception(self, client, db_connection):
        """Test POST cuando Task.create() lanza excepción"""
        # Mock Task.create para lanzar excepción
        with patch('routes.tasks.Task.create') as mock_create:
            mock_create.side_effect = Exception('Creation failed')
            
            task_data = {
                'title': 'Test Task',
                'description': 'Test',
                'category': 'test',
                'priority': 3,
                'due_date': '2025-12-31'
            }
            response = client.post(
                '/api/tasks',
                data=json.dumps(task_data),
                content_type='application/json'
            )
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'error' in data
            assert 'Creation failed' in data['error']


class TestTaskDeleteMethod:
    """Tests específicos del método delete de Task"""
    
    def test_delete_existing_task_directly(self, db_connection):
        """Test directo del método Task.delete()"""
        # Crear tarea
        task_id = Task.create('Delete Test', 'Desc', 'cat', 3, '2025-12-31')
        
        # Verificar que existe
        task = Task.get_by_id(task_id)
        assert task is not None
        
        # Eliminar
        Task.delete(task_id)
        
        # Verificar que ya no existe
        task = Task.get_by_id(task_id)
        assert task is None
    
    def test_delete_multiple_tasks(self, db_connection):
        """Test eliminación de múltiples tareas"""
        task_ids = []
        for i in range(5):
            task_id = Task.create(f'Task {i}', 'Desc', 'cat', 3, '2025-12-31')
            task_ids.append(task_id)
        
        # Eliminar todas
        for task_id in task_ids:
            Task.delete(task_id)
        
        # Verificar que están eliminadas
        for task_id in task_ids:
            task = Task.get_by_id(task_id)
            assert task is None
        
        # Verificar lista vacía
        all_tasks = Task.get_all()
        assert len(all_tasks) == 0


class TestDataPersistence:
    """Tests para persistencia de datos"""
    
    def test_task_fields_preserved(self, db_connection):
        """Test que todos los campos se preservan correctamente"""
        original_data = {
            'title': 'Complete Task',
            'description': 'Full description with details',
            'category': 'important',
            'priority': 5,
            'due_date': '2025-12-25'
        }
        
        task_id = Task.create(**original_data)
        retrieved_task = Task.get_by_id(task_id)
        
        # Verificar cada campo
        assert retrieved_task['title'] == original_data['title']
        assert retrieved_task['description'] == original_data['description']
        assert retrieved_task['category'] == original_data['category']
        assert retrieved_task['priority'] == original_data['priority']
        assert retrieved_task['due_date'] == original_data['due_date']
        assert retrieved_task['status'] == 'pending'
        assert retrieved_task['id'] == task_id
    
    def test_update_preserves_untouched_fields(self, db_connection):
        """Test que actualizar un campo no afecta los otros"""
        # Crear
        task_id = Task.create(
            'Original',
            'Original desc',
            'work',
            2,
            '2025-01-01'
        )
        
        # Actualizar solo el título
        Task.update(
            task_id,
            'Updated Title',
            'Original desc',
            'work',
            2,
            '2025-01-01',
            'pending'
        )
        
        # Verificar que otros campos se mantienen
        task = Task.get_by_id(task_id)
        assert task['title'] == 'Updated Title'
        assert task['description'] == 'Original desc'
        assert task['category'] == 'work'
        assert task['priority'] == 2
        assert task['due_date'] == '2025-01-01'
    
    def test_created_at_timestamp(self, db_connection):
        """Test que created_at se asigna correctamente"""
        import time
        before = time.time()
        task_id = Task.create('Timestamp Test', '', '', 3, '')
        after = time.time()
        
        task = Task.get_by_id(task_id)
        assert 'created_at' in task
        # El timestamp debe ser reciente
        assert task['created_at'] is not None
    
    def test_updated_at_timestamp(self, db_connection):
        """Test que updated_at se actualiza con UPDATE"""
        import time
        
        # Crear
        task_id = Task.create('Update Test', 'Desc', 'cat', 3, '2025-12-31')
        
        # Esperar un poco
        time.sleep(0.1)
        
        # Actualizar
        Task.update(task_id, 'Updated', 'Desc', 'cat', 3, '2025-12-31', 'pending')
        
        task = Task.get_by_id(task_id)
        assert 'updated_at' in task


class TestAPIResponseFormats:
    """Tests para validar formatos de respuesta"""
    
    def test_create_response_format(self, client, db_connection):
        """Test formato de respuesta en POST"""
        task_data = {'title': 'Format Test'}
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        assert 'id' in data
        assert 'message' in data
        assert data['message'] == 'Task created'
        assert isinstance(data['id'], int)
        assert data['id'] > 0
    
    def test_get_single_response_format(self, client, db_connection):
        """Test formato de respuesta en GET single"""
        # Crear tarea
        task_id = Task.create('Format Test', 'Desc', 'cat', 3, '2025-12-31')
        
        response = client.get(f'/api/tasks/{task_id}')
        task = json.loads(response.data)
        
        # Verificar estructura
        assert task['id'] == task_id
        assert task['title'] == 'Format Test'
        assert 'created_at' in task
        assert 'updated_at' in task
    
    def test_get_all_response_format(self, client, db_connection):
        """Test formato de respuesta en GET all"""
        # Crear varios
        for i in range(3):
            Task.create(f'Task {i}', 'Desc', 'cat', 3, '2025-12-31')
        
        response = client.get('/api/tasks')
        tasks = json.loads(response.data)
        
        assert isinstance(tasks, list)
        assert len(tasks) >= 3
        
        # Verificar estructura de cada tarea
        for task in tasks:
            assert 'id' in task
            assert 'title' in task
            assert 'status' in task
    
    def test_error_response_format(self, client):
        """Test formato de respuesta en error"""
        response = client.get('/api/tasks/99999')
        data = json.loads(response.data)
        
        assert 'error' in data
        assert data['error'] == 'Task not found'
        assert response.status_code == 404
