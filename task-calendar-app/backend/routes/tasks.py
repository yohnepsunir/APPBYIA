from flask import Blueprint, request, jsonify
from models import Task

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    tasks = Task.get_all()
    return jsonify(tasks), 200

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.get_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task), 200

@tasks_bp.route('', methods=['POST'])
def create_task():
    data = request.json
    try:
        task_id = Task.create(
            data['title'],
            data.get('description', ''),
            data.get('category', ''),
            data.get('priority', 3),
            data.get('due_date', '')
        )
        return jsonify({'id': task_id, 'message': 'Task created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    try:
        Task.update(
            task_id,
            data['title'],
            data.get('description', ''),
            data.get('category', ''),
            data.get('priority', 3),
            data.get('due_date', ''),
            data.get('status', 'pending')
        )
        return jsonify({'message': 'Task updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        Task.delete(task_id)
        return jsonify({'message': 'Task deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400