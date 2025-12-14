"""
Tests de integración end-to-end para la aplicación
"""
import pytest
import json
from models import Task


class TestTaskWorkflow:
    """Tests de flujos completos de trabajo con tareas"""
    
    def test_complete_task_lifecycle(self, client, db_connection):
        """Test del ciclo de vida completo de una tarea"""
        # 1. Verificar que no hay tareas
        response = client.get('/api/tasks')
        assert response.status_code == 200
        assert len(json.loads(response.data)) == 0
        
        # 2. Crear una tarea
        task_data = {
            'title': 'Integration Test Task',
            'description': 'Complete lifecycle test',
            'category': 'testing',
            'priority': 4,
            'due_date': '2025-12-31'
        }
        
        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        assert response.status_code == 201
        task_id = json.loads(response.data)['id']
        
        # 3. Verificar que la tarea se creó
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        task = json.loads(response.data)
        assert task['title'] == task_data['title']
        assert task['status'] == 'pending'
        
        # 4. Listar todas las tareas
        response = client.get('/api/tasks')
        assert response.status_code == 200
        tasks = json.loads(response.data)
        assert len(tasks) == 1
        
        # 5. Actualizar la tarea
        updated_data = task_data.copy()
        updated_data['title'] = 'Updated Integration Task'
        updated_data['status'] = 'in-progress'
        
        response = client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        # 6. Verificar la actualización
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        task = json.loads(response.data)
        assert task['title'] == 'Updated Integration Task'
        assert task['status'] == 'in-progress'
        
        # 7. Completar la tarea
        updated_data['status'] = 'completed'
        response = client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        # 8. Eliminar la tarea
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        
        # 9. Verificar que se eliminó
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 404
        
        # 10. Verificar que la lista está vacía
        response = client.get('/api/tasks')
        assert response.status_code == 200
        assert len(json.loads(response.data)) == 0
    
    def test_multiple_tasks_management(self, client, db_connection):
        """Test de gestión de múltiples tareas"""
        # Crear varias tareas
        tasks_to_create = [
            {
                'title': f'Task {i}',
                'description': f'Description {i}',
                'category': 'work' if i % 2 == 0 else 'personal',
                'priority': (i % 5) + 1,
                'due_date': f'2025-12-{10 + i:02d}'
            }
            for i in range(1, 6)
        ]
        
        created_ids = []
        for task_data in tasks_to_create:
            response = client.post(
                '/api/tasks',
                data=json.dumps(task_data),
                content_type='application/json'
            )
            assert response.status_code == 201
            created_ids.append(json.loads(response.data)['id'])
        
        # Verificar que todas se crearon
        response = client.get('/api/tasks')
        assert response.status_code == 200
        tasks = json.loads(response.data)
        assert len(tasks) == 5
        
        # Actualizar algunas tareas a completadas
        for task_id in created_ids[:3]:
            task = Task.get_by_id(task_id)
            task['status'] = 'completed'
            response = client.put(
                f'/api/tasks/{task_id}',
                data=json.dumps(task),
                content_type='application/json'
            )
            assert response.status_code == 200
        
        # Verificar el estado de las tareas
        response = client.get('/api/tasks')
        tasks = json.loads(response.data)
        completed_count = sum(1 for t in tasks if t['status'] == 'completed')
        pending_count = sum(1 for t in tasks if t['status'] == 'pending')
        assert completed_count == 3
        assert pending_count == 2
        
        # Eliminar tareas completadas
        for task_id in created_ids[:3]:
            response = client.delete(f'/api/tasks/{task_id}')
            assert response.status_code == 200
        
        # Verificar que quedan solo las pendientes
        response = client.get('/api/tasks')
        tasks = json.loads(response.data)
        assert len(tasks) == 2
        assert all(t['status'] == 'pending' for t in tasks)
    
    def test_task_priority_workflow(self, client, db_connection):
        """Test de flujo de trabajo con diferentes prioridades"""
        priorities = [1, 2, 3, 4, 5]
        task_ids = []
        
        # Crear tareas con diferentes prioridades
        for priority in priorities:
            task_data = {
                'title': f'Priority {priority} Task',
                'description': f'Task with priority {priority}',
                'category': 'priority-test',
                'priority': priority,
                'due_date': '2025-12-31'
            }
            
            response = client.post(
                '/api/tasks',
                data=json.dumps(task_data),
                content_type='application/json'
            )
            assert response.status_code == 201
            task_ids.append(json.loads(response.data)['id'])
        
        # Verificar que todas las tareas tienen las prioridades correctas
        for i, task_id in enumerate(task_ids):
            response = client.get(f'/api/tasks/{task_id}')
            assert response.status_code == 200
            task = json.loads(response.data)
            assert task['priority'] == priorities[i]
    
    def test_error_handling_workflow(self, client, db_connection):
        """Test de manejo de errores en flujos de trabajo"""
        # Intentar obtener tarea inexistente
        response = client.get('/api/tasks/99999')
        assert response.status_code == 404
        
        # Intentar crear tarea sin datos requeridos
        response = client.post(
            '/api/tasks',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Crear tarea válida
        task_data = {
            'title': 'Valid Task',
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
        assert response.status_code == 201
        task_id = json.loads(response.data)['id']
        
        # Intentar actualizar con datos inválidos
        response = client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps({'description': 'No title'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Eliminar tarea válida
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        
        # Intentar obtener tarea eliminada
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 404
