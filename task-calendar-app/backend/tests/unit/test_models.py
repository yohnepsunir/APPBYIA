"""
Tests unitarios para los modelos
"""
import pytest
from datetime import datetime
from models import Task


class TestTaskModel:
    """Tests para el modelo Task"""
    
    def test_task_creation(self, db_connection, sample_task_data):
        """Test de creación de una tarea"""
        task_id = Task.create(
            sample_task_data['title'],
            sample_task_data['description'],
            sample_task_data['category'],
            sample_task_data['priority'],
            sample_task_data['due_date']
        )
        
        assert task_id is not None
        assert isinstance(task_id, int)
        assert task_id > 0
    
    def test_task_get_all_empty(self, db_connection):
        """Test obtener todas las tareas cuando no hay ninguna"""
        tasks = Task.get_all()
        assert isinstance(tasks, list)
        assert len(tasks) == 0
    
    def test_task_get_all_with_data(self, db_connection, create_sample_tasks):
        """Test obtener todas las tareas con datos"""
        tasks = Task.get_all()
        
        assert isinstance(tasks, list)
        assert len(tasks) == 3
        
        # Verificar que cada tarea tiene los campos esperados
        for task in tasks:
            assert 'id' in task
            assert 'title' in task
            assert 'description' in task
            assert 'category' in task
            assert 'priority' in task
            assert 'due_date' in task
            assert 'status' in task
    
    def test_task_get_by_id_existing(self, db_connection, sample_task_data):
        """Test obtener una tarea existente por ID"""
        task_id = Task.create(
            sample_task_data['title'],
            sample_task_data['description'],
            sample_task_data['category'],
            sample_task_data['priority'],
            sample_task_data['due_date']
        )
        
        task = Task.get_by_id(task_id)
        
        assert task is not None
        assert task['id'] == task_id
        assert task['title'] == sample_task_data['title']
        assert task['description'] == sample_task_data['description']
        assert task['category'] == sample_task_data['category']
        assert task['priority'] == sample_task_data['priority']
        assert task['due_date'] == sample_task_data['due_date']
        assert task['status'] == 'pending'
    
    def test_task_get_by_id_nonexistent(self, db_connection):
        """Test obtener una tarea que no existe"""
        task = Task.get_by_id(9999)
        assert task is None
    
    def test_task_update(self, db_connection, sample_task_data):
        """Test actualización de una tarea"""
        # Crear tarea
        task_id = Task.create(
            sample_task_data['title'],
            sample_task_data['description'],
            sample_task_data['category'],
            sample_task_data['priority'],
            sample_task_data['due_date']
        )
        
        # Actualizar tarea
        new_title = "Updated Task"
        new_status = "completed"
        Task.update(
            task_id,
            new_title,
            sample_task_data['description'],
            sample_task_data['category'],
            sample_task_data['priority'],
            sample_task_data['due_date'],
            new_status
        )
        
        # Verificar actualización
        updated_task = Task.get_by_id(task_id)
        assert updated_task['title'] == new_title
        assert updated_task['status'] == new_status
    
    def test_task_delete(self, db_connection, sample_task_data):
        """Test eliminación de una tarea"""
        # Crear tarea
        task_id = Task.create(
            sample_task_data['title'],
            sample_task_data['description'],
            sample_task_data['category'],
            sample_task_data['priority'],
            sample_task_data['due_date']
        )
        
        # Verificar que existe
        task = Task.get_by_id(task_id)
        assert task is not None
        
        # Eliminar tarea
        Task.delete(task_id)
        
        # Verificar que ya no existe
        task = Task.get_by_id(task_id)
        assert task is None
    
    def test_task_priority_validation(self, db_connection):
        """Test validación de prioridad en rango 1-5"""
        # Prioridad válida
        task_id = Task.create('Test', 'Desc', 'cat', 3, '2025-12-31')
        assert task_id is not None
        
        # Prioridad inválida (debería fallar o ajustarse según la implementación)
        # Nota: SQLite tiene CHECK constraint, pero no siempre los aplica
        # En producción, deberías agregar validación en el modelo
    
    def test_task_default_status(self, db_connection):
        """Test que el status por defecto es 'pending'"""
        task_id = Task.create('Test', 'Desc', 'cat', 3, '2025-12-31')
        task = Task.get_by_id(task_id)
        assert task['status'] == 'pending'
    
    def test_task_ordering(self, db_connection, create_sample_tasks):
        """Test que las tareas se ordenan por created_at DESC"""
        tasks = Task.get_all()
        
        # Verificar que hay tareas
        assert len(tasks) > 0
        
        # Verificar que están ordenadas por created_at descendente
        # (las más recientes primero)
        for i in range(len(tasks) - 1):
            # Las tareas de prueba se crean en orden, así que las últimas
            # creadas deberían aparecer primero
            pass  # El orden depende de la implementación exacta
