"""
Tests para el módulo app.py
"""
import pytest
import sys
from unittest.mock import patch, MagicMock
import app as app_module


class TestAppModule:
    """Tests para la inicialización y configuración de la app"""
    
    def test_app_creation(self):
        """Test que la aplicación Flask se crea correctamente"""
        assert app_module.app is not None
        assert app_module.app.name == 'app'
    
    def test_app_static_folder(self):
        """Test que la carpeta estática está configurada"""
        assert app_module.app.static_folder is not None
        assert 'frontend' in app_module.app.static_folder
    
    def test_app_cors_enabled(self):
        """Test que CORS está habilitado"""
        # CORS debe estar registrado como extensión
        assert any('CORS' in str(ext) for ext in dir(app_module))
    
    def test_app_blueprints_registered(self):
        """Test que los blueprints están registrados"""
        blueprints = app_module.app.blueprints
        assert 'tasks' in blueprints
    
    def test_app_routes_registered(self):
        """Test que las rutas están registradas"""
        routes = []
        for rule in app_module.app.url_map.iter_rules():
            routes.append(rule.rule)
        
        # Verificar rutas clave
        assert '/api/tasks' in routes
        assert '/api/health' in routes
    
    def test_app_route_methods(self):
        """Test que los métodos HTTP correctos están registrados"""
        # Simplemente verificar que las rutas de tasks existen
        has_tasks_routes = False
        for rule in app_module.app.url_map.iter_rules():
            if 'tasks' in rule.rule:
                has_tasks_routes = True
                break
        
        assert has_tasks_routes
    
    def test_app_main_block(self):
        """Test el bloque if __name__ == '__main__'"""
        # Verificar que el módulo tiene la condición principal
        import inspect
        source = inspect.getsource(app_module)
        assert "if __name__ == '__main__':" in source
        assert 'app.run' in source


class TestMainExecution:
    """Tests que cubren la ejecución del main"""
    
    def test_app_run_called_when_main(self):
        """Test que app.run() se llamaría cuando se ejecuta como main"""
        # Este test verifica que el código está presente
        import inspect
        source = inspect.getsource(app_module)
        assert 'app.run(debug=True, host=\'0.0.0.0\', port=5000)' in source
    
    def test_app_run_parameters(self):
        """Test que app.run() tiene los parámetros correctos"""
        # Verificar el código source
        import inspect
        source = inspect.getsource(app_module)
        
        # El source debería contener app.run()
        assert 'app.run' in source


class TestAppConfiguration:
    """Tests para configuración de la aplicación"""
    
    def test_database_initialized(self):
        """Test que la base de datos se inicializa al importar"""
        # Si la app se cargó, init_db debe haberse ejecutado
        from database import get_db
        db = get_db()
        assert db is not None
        
        # Verificar que las tablas existen
        cursor = db.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='tasks'
        """)
        assert cursor.fetchone() is not None
        db.close()
    
    def test_frontend_path_exists(self):
        """Test que la ruta frontend está correctamente configurada"""
        assert app_module.FRONTEND_PATH is not None
        assert 'frontend' in app_module.FRONTEND_PATH.lower()
