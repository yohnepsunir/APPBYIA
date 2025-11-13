from datetime import datetime
from database import get_db

class Task:
    def __init__(self, title, description, category, priority, due_date, status='pending', id=None):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.due_date = due_date
        self.status = status
        self.created_at = datetime.now().isoformat()

    @staticmethod
    def create(title, description, category, priority, due_date):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, category, priority, due_date, status)
            VALUES (?, ?, ?, ?, ?, 'pending')
        ''', (title, description, category, priority, due_date))
        db.commit()
        task_id = cursor.lastrowid
        db.close()
        return task_id

    @staticmethod
    def get_all():
        db = get_db()
        tasks = db.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
        db.close()
        return [dict(task) for task in tasks]

    @staticmethod
    def get_by_id(task_id):
        db = get_db()
        task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        db.close()
        return dict(task) if task else None

    @staticmethod
    def update(task_id, title, description, category, priority, due_date, status):
        db = get_db()
        db.execute('''
            UPDATE tasks 
            SET title = ?, description = ?, category = ?, priority = ?, due_date = ?, status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, description, category, priority, due_date, status, task_id))
        db.commit()
        db.close()

    @staticmethod
    def delete(task_id):
        db = get_db()
        db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        db.commit()
        db.close()