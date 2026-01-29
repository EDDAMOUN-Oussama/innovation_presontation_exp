from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Define the JSON file for storing tasks
DATA_FILE = 'tasks.json'

def load_tasks():
    """Load tasks from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # If file is corrupted, return an empty list
                return []
    else:
        # Create the file with an empty list if it doesn't exist
        save_tasks([])
        return []

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    """Endpoint to get all tasks."""
    try:
        tasks = load_tasks()
        return jsonify({
            'success': True,
            'tasks': tasks,
            'count': len(tasks)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/tasks', methods=['POST'])
def create_task():
    """Endpoint to create a new task."""
    try:
        tasks = load_tasks()
        
        # Check if request body is valid JSON
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Request must be in JSON format'
            }), 400
        
        data = request.get_json()
        
        # Validate required fields
        if 'title' not in data or not data['title'].strip():
            return jsonify({
                'success': False,
                'error': 'Task title is required and cannot be empty'
            }), 400
        
        # Create a new task
        new_task = {
            'id': max([task['id'] for task in tasks], default=0) + 1,  # Generate ID
            'title': data['title'].strip(),
            'description': data.get('description', '').strip(),
            'completed': data.get('completed', False),
            'created_at': datetime.now().isoformat()
        }
        
        tasks.append(new_task)
        save_tasks(tasks)
        
        return jsonify({
            'success': True,
            'task': new_task
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Endpoint to delete a task by ID."""
    try:
        tasks = load_tasks()
        
        # Find the task with the given ID
        task_index = None
        for i, task in enumerate(tasks):
            if task['id'] == task_id:
                task_index = i
                break
        
        if task_index is None:
            return jsonify({
                'success': False,
                'error': f'Task with ID {task_id} not found'
            }), 404
        
        deleted_task = tasks.pop(task_index)
        save_tasks(tasks)
        
        return jsonify({
            'success': True,
            'message': f'Task "{deleted_task["title"]}" deleted successfully',
            'deleted_task': deleted_task
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Initialize the tasks file if it doesn't exist
    load_tasks()
    app.run(debug=True, host='0.0.0.0', port=8000)