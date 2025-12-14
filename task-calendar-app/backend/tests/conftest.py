"""
Configuración de fixtures para los tests
"""
import pytest
import os
import tempfile
import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app import app as flask_app
from database import init_db, get_db


@pytest.fixture(scope='session')
def app():
    """Fixture de la aplicación Flask para toda la sesión de tests"""
    # Configurar la aplicación para testing
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': ':memory:',  # Base de datos en memoria para tests
    })
    
    # Inicializar la base de datos
    with flask_app.app_context():
        init_db()
    
    yield flask_app


@pytest.fixture(scope='function')
def client(app):
    """Fixture del cliente de pruebas Flask"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Fixture del runner CLI de Flask"""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def db_connection():
    """Fixture de conexión a base de datos de prueba"""
    # Crear un archivo temporal para la base de datos
    db_fd, db_path = tempfile.mkstemp()
    
    # Guardar el DATABASE original
    import database
    original_db = database.DATABASE
    database.DATABASE = db_path
    
    # Inicializar la base de datos
    init_db()
    
    yield db_path
    
    # Limpiar
    os.close(db_fd)
    os.unlink(db_path)
    database.DATABASE = original_db


@pytest.fixture(scope='function')
def sample_task_data():
    """Fixture con datos de ejemplo para tasks"""
    return {
        'title': 'Test Task',
        'description': 'This is a test task',
        'category': 'work',
        'priority': 3,
        'due_date': '2025-12-31',
        'status': 'pending'
    }


@pytest.fixture(scope='function')
def create_sample_tasks(db_connection):
    """Fixture que crea tareas de ejemplo en la base de datos"""
    from models import Task
    
    tasks_data = [
        {
            'title': 'Task 1',
            'description': 'First task',
            'category': 'work',
            'priority': 1,
            'due_date': '2025-12-15'
        },
        {
            'title': 'Task 2',
            'description': 'Second task',
            'category': 'personal',
            'priority': 3,
            'due_date': '2025-12-20'
        },
        {
            'title': 'Task 3',
            'description': 'Third task',
            'category': 'urgent',
            'priority': 5,
            'due_date': '2025-12-10'
        }
    ]
    
    task_ids = []
    for task_data in tasks_data:
        task_id = Task.create(**task_data)
        task_ids.append(task_id)
    
    return task_ids
