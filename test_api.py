import requests
import json
import time
import subprocess
import signal
import os

# Start the Flask server in the background
print("Starting Flask server...")
server_process = subprocess.Popen(['python', 'main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait a moment for the server to start
time.sleep(3)

try:
    BASE_URL = 'http://localhost:8000'
    
    print("\n--- Testing GET /tasks (initial) ---")
    response = requests.get(f'{BASE_URL}/tasks')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n--- Testing POST /tasks ---")
    new_task = {
        "title": "Buy groceries",
        "description": "Milk, bread, eggs, and fruits",
        "completed": False
    }
    response = requests.post(f'{BASE_URL}/tasks', json=new_task)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n--- Testing POST /tasks (another task) ---")
    another_task = {
        "title": "Walk the dog",
        "description": "Take Max for a walk in the park",
        "completed": True
    }
    response = requests.post(f'{BASE_URL}/tasks', json=another_task)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n--- Testing GET /tasks (after adding tasks) ---")
    response = requests.get(f'{BASE_URL}/tasks')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n--- Testing DELETE /tasks (first task) ---")
    # Get the first task ID to delete
    response = requests.get(f'{BASE_URL}/tasks')
    tasks = response.json()['tasks']
    if tasks:
        first_task_id = tasks[0]['id']
        response = requests.delete(f'{BASE_URL}/tasks/{first_task_id}')
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n--- Testing GET /tasks (after deletion) ---")
    response = requests.get(f'{BASE_URL}/tasks')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n--- Testing error case: DELETE non-existent task ---")
    response = requests.delete(f'{BASE_URL}/tasks/9999')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n--- Testing error case: POST without title ---")
    invalid_task = {"description": "This should fail"}
    response = requests.post(f'{BASE_URL}/tasks', json=invalid_task)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

except requests.exceptions.ConnectionError:
    print("Could not connect to the server. Make sure it's running on http://localhost:5000")
except Exception as e:
    print(f"An error occurred during testing: {e}")

finally:
    # Terminate the server process
    print("\nTerminating server...")
    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server_process.kill()

print("\nTesting completed!")