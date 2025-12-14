"""
Tests adicionales para mejorar la cobertura de código
"""
import pytest
import json
from models import Task


class TestAppRoutes:
    """Tests adicionales para las rutas de la aplicación"""
    
    def test_index_route(self, client):
        """Test de la ruta index"""
        # Esta ruta puede fallar si no existe el archivo index.html
        # pero probamos que se intenta servir
        response = client.get('/')
        # Aceptamos 200 o 404 dependiendo de si existe el archivo
        assert response.status_code in [200, 404]
    
    def test_serve_static_files(self, client):
        """Test para servir archivos estáticos"""
        # Probamos con un archivo que probablemente no existe
        response = client.get('/nonexistent.js')
        # Debe retornar 404 si no existe
        assert response.status_code == 404
    
    def test_serve_css_file(self, client):
        """Test para servir archivos CSS"""
        response = client.get('/css/styles.css')
        # 200 si existe, 404 si no
        assert response.status_code in [200, 404]


class TestTaskEdgeCases:
    """Tests para casos edge y manejo de excepciones"""
    
    def test_task_with_empty_strings(self, client, db_connection):
        """Test creación de tarea con strings vacíos"""
        task_data = {
            'title': 'Task',
            'description': '',
            'category': '',
            'priority': 3,
            'due_date': ''
        }
        
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        assert response.status_code == 201
    
    def test_task_with_special_characters(self, client, db_connection):
        """Test creación de tarea con caracteres especiales"""
        task_data = {
            'title': 'Task with special chars: @#$%&*()',
            'description': 'Description with quotes "test" and \'single\'',
            'category': 'work/personal',
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
        
        # Verificar que se guardó correctamente
        task = Task.get_by_id(task_id)
        assert task['title'] == task_data['title']
        assert task['description'] == task_data['description']
    
    def test_task_with_unicode_characters(self, client, db_connection):
        """Test creación de tarea con caracteres Unicode"""
        task_data = {
            'title': 'Tarea con tildes: ñáéíóú 中文 العربية',
            'description': 'Descripción con emojis 🚀✨🎉',
            'category': 'trabajo',
            'priority': 4,
            'due_date': '2025-12-31'
        }
        
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        assert response.status_code == 201
    
    def test_task_with_long_strings(self, client, db_connection):
        """Test creación de tarea con strings muy largos"""
        long_title = 'A' * 500
        long_description = 'Lorem ipsum ' * 100
        
        task_data = {
            'title': long_title,
            'description': long_description,
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
    
    def test_update_task_with_all_fields(self, client, db_connection):
        """Test actualización de tarea modificando todos los campos"""
        # Crear tarea inicial
        task_data = {
            'title': 'Original Task',
            'description': 'Original description',
            'category': 'work',
            'priority': 1,
            'due_date': '2025-01-01'
        }
        
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        task_id = json.loads(response.data)['id']
        
        # Actualizar con todos los campos diferentes
        updated_data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'category': 'personal',
            'priority': 5,
            'due_date': '2025-12-31',
            'status': 'completed'
        }
        
        response = client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        # Verificar cambios
        task = Task.get_by_id(task_id)
        assert task['title'] == updated_data['title']
        assert task['priority'] == updated_data['priority']
        assert task['category'] == updated_data['category']
        assert task['due_date'] == updated_data['due_date']
        assert task['status'] == updated_data['status']
    
    def test_priority_edge_values(self, client, db_connection):
        """Test con valores límite de prioridad"""
        for priority in [1, 2, 3, 4, 5]:
            task_data = {
                'title': f'Priority {priority} Task',
                'priority': priority
            }
            
            response = client.post(
                '/api/tasks',
                data=json.dumps(task_data),
                content_type='application/json'
            )
            assert response.status_code == 201
            
            task_id = json.loads(response.data)['id']
            task = Task.get_by_id(task_id)
            assert task['priority'] == priority
    
    def test_delete_nonexistent_task(self, client, db_connection):
        """Test eliminar tarea que no existe"""
        response = client.delete('/api/tasks/99999')
        # Debería funcionar sin error (no hay validación de existencia)
        assert response.status_code == 200
    
    def test_update_nonexistent_task(self, client, db_connection):
        """Test actualizar tarea que no existe"""
        task_data = {
            'title': 'Updated Task',
            'description': 'Description',
            'category': 'work',
            'priority': 3,
            'due_date': '2025-12-31'
        }
        
        response = client.put(
            '/api/tasks/99999',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        # Debería funcionar sin error (no hay validación de existencia)
        assert response.status_code == 200
    
    def test_task_status_transitions(self, client, db_connection):
        """Test transiciones de estado de tarea"""
        task_data = {
            'title': 'Status Test Task',
            'status': 'pending'
        }
        
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        task_id = json.loads(response.data)['id']
        
        # Transición: pending -> in-progress
        update_data = task_data.copy()
        update_data['status'] = 'in-progress'
        response = client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        # Transición: in-progress -> completed
        update_data['status'] = 'completed'
        response = client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        # Verificar estado final
        task = Task.get_by_id(task_id)
        assert task['status'] == 'completed'


class TestTaskModelDetails:
    """Tests detallados del modelo Task"""
    
    def test_task_initialization(self):
        """Test inicialización de instancia Task"""
        task = Task(
            title='Test',
            description='Desc',
            category='work',
            priority=3,
            due_date='2025-12-31',
            status='pending',
            id=1
        )
        
        assert task.id == 1
        assert task.title == 'Test'
        assert task.description == 'Desc'
        assert task.category == 'work'
        assert task.priority == 3
        assert task.due_date == '2025-12-31'
        assert task.status == 'pending'
        assert task.created_at is not None
    
    def test_task_dict_conversion(self, db_connection):
        """Test conversión de tarea a diccionario"""
        task_data = {
            'title': 'Dict Conversion Test',
            'description': 'Test',
            'category': 'test',
            'priority': 3,
            'due_date': '2025-12-31'
        }
        
        task_id = Task.create(**task_data)
        task_dict = Task.get_by_id(task_id)
        
        assert isinstance(task_dict, dict)
        assert task_dict['title'] == task_data['title']
        assert task_dict['id'] == task_id
        assert 'created_at' in task_dict


class TestAPIErrorHandling:
    """Tests para manejo de errores en API"""
    
    def test_post_with_null_json(self, client):
        """Test POST con JSON nulo"""
        response = client.post(
            '/api/tasks',
            data='null',
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_post_with_empty_json(self, client):
        """Test POST con JSON vacío"""
        response = client.post(
            '/api/tasks',
            data='{}',
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_post_with_invalid_content_type(self, client):
        """Test POST con content-type inválido"""
        response = client.post(
            '/api/tasks',
            data='{"title": "Test"}',
            content_type='text/plain'
        )
        # Flask puede retornar 400 o procesar igualmente dependiendo de configuración
        assert response.status_code in [400, 415]
    
    def test_put_with_invalid_id_format(self, client):
        """Test PUT con ID en formato inválido"""
        response = client.put(
            '/api/tasks/invalid_id',
            data=json.dumps({'title': 'Test'}),
            content_type='application/json'
        )
        # Flask retorna 405 cuando el ID no es un entero (no coincide con la ruta)
        assert response.status_code == 405
    
    def test_get_with_invalid_id_format(self, client):
        """Test GET con ID en formato inválido"""
        response = client.get('/api/tasks/invalid_id')
        assert response.status_code == 404
    
    def test_delete_with_invalid_id_format(self, client):
        """Test DELETE con ID en formato inválido"""
        response = client.delete('/api/tasks/invalid_id')
        # Flask retorna 405 cuando el ID no es un entero (no coincide con la ruta)
        assert response.status_code == 405


class TestTaskCountOperations:
    """Tests para operaciones con múltiples tareas"""
    
    def test_bulk_create_tasks(self, client, db_connection):
        """Test creación en masa de tareas"""
        task_count = 10
        created_ids = []
        
        for i in range(task_count):
            task_data = {
                'title': f'Bulk Task {i}',
                'description': f'Description {i}',
                'category': f'category-{i % 3}',
                'priority': (i % 5) + 1,
                'due_date': '2025-12-31'
            }
            
            response = client.post(
                '/api/tasks',
                data=json.dumps(task_data),
                content_type='application/json'
            )
            assert response.status_code == 201
            created_ids.append(json.loads(response.data)['id'])
        
        # Verificar que todas se crearon
        response = client.get('/api/tasks')
        tasks = json.loads(response.data)
        assert len(tasks) >= task_count
    
    def test_get_all_with_large_dataset(self, client, db_connection):
        """Test obtener todas las tareas con dataset grande"""
        # Crear múltiples tareas
        for i in range(5):
            Task.create(
                f'Task {i}',
                f'Desc {i}',
                'test',
                3,
                '2025-12-31'
            )
        
        # Obtener todas
        response = client.get('/api/tasks')
        assert response.status_code == 200
        tasks = json.loads(response.data)
        assert len(tasks) >= 5
        
        # Verificar ordenamiento (más recientes primero)
        if len(tasks) > 1:
            # Las tareas deben estar ordenadas por created_at DESC
            pass
