from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# File to store the to-do list data
DATA_FILE = 'todos.json'

def load_todos():
    """Load todos from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        # Initialize with an empty list if file doesn't exist
        save_todos([])
        return []

def save_todos(todos):
    """Save todos to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

@app.route('/')
def index():
    """Serve the HTML interface."""
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>To-Do List Manager</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }
            
            .container {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .input-section {
                display: flex;
                margin-bottom: 20px;
                gap: 10px;
            }
            
            #taskInput {
                flex: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 16px;
            }
            
            button {
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            
            button:hover {
                background-color: #0056b3;
            }
            
            .delete-btn {
                background-color: #dc3545;
                padding: 5px 10px;
                font-size: 14px;
            }
            
            .delete-btn:hover {
                background-color: #c82333;
            }
            
            ul {
                list-style-type: none;
                padding: 0;
            }
            
            li {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px;
                margin-bottom: 10px;
                background-color: #f9f9f9;
                border-radius: 4px;
                border-left: 4px solid #007bff;
            }
            
            .task-text {
                flex: 1;
                word-break: break-word;
                padding-right: 10px;
            }
            
            .error {
                color: #dc3545;
                text-align: center;
                margin-top: 10px;
            }
            
            .loading {
                text-align: center;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>To-Do List Manager</h1>
            
            <div class="input-section">
                <input type="text" id="taskInput" placeholder="Enter a new task..." />
                <button onclick="addTask()">Add Task</button>
            </div>
            
            <ul id="taskList">
                <!-- Tasks will be loaded here -->
            </ul>
            
            <div id="errorMessage" class="error"></div>
        </div>

        <script>
            // Load tasks when page loads
            document.addEventListener('DOMContentLoaded', function() {
                loadTasks();
            });
            
            // Function to load all tasks
            async function loadTasks() {
                try {
                    const response = await fetch('/api/todos');
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const tasks = await response.json();
                    
                    const taskList = document.getElementById('taskList');
                    taskList.innerHTML = '';
                    
                    if (tasks.length === 0) {
                        taskList.innerHTML = '<p style="text-align:center; color:#666;">No tasks found. Add a new task above!</p>';
                        return;
                    }
                    
                    tasks.forEach(task => {
                        const li = document.createElement('li');
                        li.innerHTML = `
                            <span class="task-text">${task.task}</span>
                            <button class="delete-btn" onclick="deleteTask(${task.id})">Delete</button>
                        `;
                        taskList.appendChild(li);
                    });
                    
                    document.getElementById('errorMessage').textContent = '';
                } catch (error) {
                    console.error('Error loading tasks:', error);
                    document.getElementById('errorMessage').textContent = 'Failed to load tasks';
                }
            }
            
            // Function to add a new task
            async function addTask() {
                const taskInput = document.getElementById('taskInput');
                const taskText = taskInput.value.trim();
                
                if (!taskText) {
                    alert('Please enter a task');
                    return;
                }
                
                try {
                    const response = await fetch('/api/todos', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ task: taskText })
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.error || 'Failed to add task');
                    }
                    
                    taskInput.value = '';
                    loadTasks(); // Reload the task list
                } catch (error) {
                    console.error('Error adding task:', error);
                    document.getElementById('errorMessage').textContent = error.message;
                }
            }
            
            // Function to delete a task
            async function deleteTask(taskId) {
                if (!confirm('Are you sure you want to delete this task?')) {
                    return;
                }
                
                try {
                    const response = await fetch(`/api/todos/${taskId}`, {
                        method: 'DELETE'
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.error || 'Failed to delete task');
                    }
                    
                    loadTasks(); // Reload the task list
                } catch (error) {
                    console.error('Error deleting task:', error);
                    document.getElementById('errorMessage').textContent = error.message;
                }
            }
            
            // Allow adding task with Enter key
            document.getElementById('taskInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    addTask();
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/api/todos', methods=['GET'])
def get_all_todos():
    """Get all tasks."""
    try:
        todos = load_todos()
        return jsonify(todos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos', methods=['POST'])
def create_todo():
    """Create a new task."""
    try:
        todos = load_todos()
        
        # Get the JSON data from the request
        data = request.get_json()
        
        # Validate that the request has the required fields
        if not data or 'task' not in data or not data['task'].strip():
            return jsonify({'error': 'Task field is required and cannot be empty'}), 400
        
        # Create a new task
        new_task = {
            'id': max([t['id'] for t in todos], default=0) + 1,  # Generate next ID
            'task': data['task'].strip(),
            'created_at': datetime.now().isoformat()
        }
        
        # Add the new task to the list
        todos.append(new_task)
        
        # Save the updated list to the file
        save_todos(todos)
        
        return jsonify(new_task), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a task by ID."""
    try:
        todos = load_todos()
        
        # Find the task with the given ID
        task_index = None
        for i, todo in enumerate(todos):
            if todo['id'] == todo_id:
                task_index = i
                break
        
        # If the task doesn't exist, return an error
        if task_index is None:
            return jsonify({'error': 'Task not found'}), 404
        
        # Remove the task from the list
        deleted_task = todos.pop(task_index)
        
        # Save the updated list to the file
        save_todos(todos)
        
        return jsonify({'message': 'Task deleted successfully', 'deleted_task': deleted_task}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)