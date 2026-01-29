# To-Do List REST API

A Flask-based REST API for managing a To-Do List with JSON file storage.

## Features

- GET all tasks (`/tasks`)
- POST a new task (`/tasks`) 
- DELETE a task (`/tasks/<task_id>`)
- JSON file storage (`tasks.json`)
- Error handling for missing data

## Endpoints

### GET /tasks
Returns all tasks in the to-do list.

Response:
```json
{
  "success": true,
  "tasks": [...],
  "count": 2
}
```

### POST /tasks
Creates a new task.

Request body:
```json
{
  "title": "Task title",
  "description": "Optional description",
  "completed": false
}
```

Response:
```json
{
  "success": true,
  "task": { ... }
}
```

### DELETE /tasks/<task_id>
Deletes a task by ID.

Response:
```json
{
  "success": true,
  "message": "Task 'Title' deleted successfully",
  "deleted_task": { ... }
}
```

## How to Run

1. Install dependencies:
   ```bash
   pip install flask
   ```

2. Run the application:
   ```bash
   python main.py
   ```

The server will start on `http://localhost:8000`.