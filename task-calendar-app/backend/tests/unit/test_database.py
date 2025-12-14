"""
Tests unitarios para el módulo de base de datos
"""
import pytest
import sqlite3
from database import get_db, init_db


class TestDatabase:
    """Tests para funciones de base de datos"""
    
    def test_get_db_returns_connection(self, db_connection):
        """Test que get_db retorna una conexión válida"""
        db = get_db()
        assert db is not None
        assert isinstance(db, sqlite3.Connection)
        db.close()
    
    def test_get_db_row_factory(self, db_connection):
        """Test que get_db configura row_factory correctamente"""
        db = get_db()
        assert db.row_factory == sqlite3.Row
        db.close()
    
    def test_init_db_creates_tables(self, db_connection):
        """Test que init_db crea las tablas necesarias"""
        db = get_db()
        cursor = db.cursor()
        
        # Verificar que existe la tabla tasks
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='tasks'
        """)
        assert cursor.fetchone() is not None
        
        # Verificar que existe la tabla attachments
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='attachments'
        """)
        assert cursor.fetchone() is not None
        
        db.close()
    
    def test_tasks_table_structure(self, db_connection):
        """Test que la tabla tasks tiene la estructura correcta"""
        db = get_db()
        cursor = db.cursor()
        
        # Obtener información de las columnas
        cursor.execute("PRAGMA table_info(tasks)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        # Verificar columnas esperadas
        expected_columns = {
            'id', 'title', 'description', 'category', 
            'priority', 'due_date', 'status', 'created_at', 'updated_at'
        }
        assert expected_columns.issubset(set(columns.keys()))
        
        # Verificar tipos de datos clave
        assert 'INTEGER' in columns['id']
        assert 'TEXT' in columns['title']
        assert 'TEXT' in columns['status']
        
        db.close()
    
    def test_attachments_table_structure(self, db_connection):
        """Test que la tabla attachments tiene la estructura correcta"""
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("PRAGMA table_info(attachments)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        expected_columns = {'id', 'task_id', 'filename', 'file_path', 'created_at'}
        assert expected_columns.issubset(set(columns.keys()))
        
        db.close()
