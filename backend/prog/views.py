from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
import os 

def current_date(request):
    # Ensure the request is a GET request
    if request.method == 'GET':
        # Get the current date and time
        now = datetime.now()
        current_date_str = now.strftime("%Y-%m-%d %H:%M:%S")

        # Return the current date and time in a JSON response
        return JsonResponse({'current_date': current_date_str})
    else:
        # If the request is not a GET, return a 405 Method Not Allowed error
        return JsonResponse({'error': 'Method not allowed'}, status=405)


"""
{
    "name": "John Doe",
    "mail": "john.doe@example.com"
}
"""

@csrf_exempt
def submit_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('name')
            email = data.get('mail')  # Assuming 'mail' is the key used in your JSON
            return JsonResponse({'message': 'Data received', 'name': name, 'email': email})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


"""
{
    "name": "Grocery Shopping",
    "message": "Buy milk, bread, and eggs",
    "date": "2024-03-20",
    "completion": false
}
"""

@csrf_exempt
def create_todo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            # Extracting data from the request
            name = data.get('name')
            message = data.get('message')
            date = data.get('date')  # Expected to be a string in YYYY-MM-DD format
            completion = data.get('completion', False)  # Defaults to False if not provided
            
            # Preparing the todo item data
            todo_item = {
                'name': name,
                'message': message,
                'date': date,
                'completion': completion
            }
            
            # Directory where the JSON file will be saved
            storage_dir = 'storage'
            if not os.path.exists(storage_dir):
                os.makedirs(storage_dir)
            
            # Generating a unique filename for each todo item based on the current timestamp
            filename = os.path.join(storage_dir, f"todo_{int(datetime.now().timestamp())}.json")
            
            # Writing the todo item to a JSON file
            with open(filename, 'w') as file:
                json.dump(todo_item, file, indent=4)
            
            return JsonResponse({'message': 'Todo item saved successfully', 'data': todo_item})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)