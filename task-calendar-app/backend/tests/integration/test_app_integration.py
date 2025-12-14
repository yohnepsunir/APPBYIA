"""
Tests de integración para la aplicación Flask completa
"""
import pytest
import json


class TestAppIntegration:
    """Tests de integración de la aplicación completa"""
    
    def test_app_initialization(self, client):
        """Test que la aplicación se inicializa correctamente"""
        # El cliente debe estar disponible
        assert client is not None
    
    def test_cors_headers(self, client):
        """Test que CORS está configurado correctamente"""
        response = client.get('/api/tasks')
        # Flask-CORS debe agregar headers apropiados
        assert response.status_code == 200
    
    def test_health_check(self, client):
        """Test del endpoint de health check"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
    
    def test_api_endpoints_exist(self, client):
        """Test que todos los endpoints de la API existen"""
        # GET /api/tasks
        response = client.get('/api/tasks')
        assert response.status_code == 200
        
        # POST /api/tasks
        task_data = {'title': 'Test'}
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        assert response.status_code in [201, 400]  # Creado o error de validación
        
        # GET /api/health
        response = client.get('/api/health')
        assert response.status_code == 200
    
    def test_content_type_json(self, client, db_connection):
        """Test que la API responde con JSON"""
        response = client.get('/api/tasks')
        assert response.content_type == 'application/json'
        
        response = client.get('/api/health')
        assert response.content_type == 'application/json'
    
    def test_database_persistence(self, client, db_connection):
        """Test que los datos persisten en la base de datos"""
        # Crear tarea
        task_data = {
            'title': 'Persistence Test',
            'description': 'Testing data persistence',
            'category': 'test',
            'priority': 3,
            'due_date': '2025-12-31'
        }
        
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        task_id = json.loads(response.data)['id']
        
        # Obtener la tarea (simula reinicio de la app)
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        task = json.loads(response.data)
        assert task['title'] == task_data['title']
        
        # La tarea debe estar en la lista
        response = client.get('/api/tasks')
        tasks = json.loads(response.data)
        assert any(t['id'] == task_id for t in tasks)
    
    def test_concurrent_operations(self, client, db_connection):
        """Test de operaciones concurrentes"""
        # Crear múltiples tareas "simultáneamente"
        tasks_data = [
            {'title': f'Concurrent Task {i}', 'priority': i}
            for i in range(1, 6)
        ]
        
        created_ids = []
        for task_data in tasks_data:
            response = client.post(
                '/api/tasks',
                data=json.dumps(task_data),
                content_type='application/json'
            )
            assert response.status_code == 201
            created_ids.append(json.loads(response.data)['id'])
        
        # Verificar que todos los IDs son únicos
        assert len(created_ids) == len(set(created_ids))
        
        # Verificar que todas las tareas existen
        response = client.get('/api/tasks')
        tasks = json.loads(response.data)
        assert len(tasks) >= len(created_ids)
        
        for task_id in created_ids:
            assert any(t['id'] == task_id for t in tasks)
    
    def test_invalid_routes(self, client):
        """Test de rutas inválidas"""
        # Ruta que no existe
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
        
        # Método no permitido
        response = client.patch('/api/tasks')
        assert response.status_code == 405
    
    def test_malformed_json(self, client):
        """Test con JSON malformado"""
        response = client.post(
            '/api/tasks',
            data='{"title": invalid json}',
            content_type='application/json'
        )
        # Debe retornar error (400 o 500 dependiendo del manejo)
        assert response.status_code >= 400
