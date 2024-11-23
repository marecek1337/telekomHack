import ssl
import zipfile
from os.path import basename
from urllib.request import urlopen

from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
import os
import requests
import os
import zipfile
import io

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

@csrf_exempt
def download_file(request):
    url = request.json.get('url')
    if not url:
        return JsonResponse({'error': 'URL is required'}, status=400)

    save_path = os.path.join("data")
    os.makedirs(save_path, exist_ok=True)

    response = requests.get(url)
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        if 'zip' in content_type:
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(save_path)
            return JsonResponse({'message': f'ZIP file downloaded and extracted successfully to {save_path}'}, status=200)
        else:
            file_name = os.path.join(save_path, os.path.basename(url))
            with open(file_name, 'wb') as file:
                file.write(response.content)
            return JsonResponse({'message': f'File downloaded successfully to {file_name}'}, status=200)
    else:
        return JsonResponse({'error': f'Failed to download file. Status code: {response.status_code}'}, status=500)
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


import requests
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def download_file(request):
    print("Downloading file")
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            url = data.get('url')
            if not url:
                return JsonResponse({'error': 'URL is required'}, status=400)

            context = ssl._create_unverified_context()

            url = "https://data.montgomerycountymd.gov/api/views/mmzv-x632/rows.csv?accessType=DOWNLOAD"
            response = urlopen(url, context=context)
            # Get the Content-Disposition header
            content_disposition = response.getheader('Content-Disposition')

            # Extract filename from the Content-Disposition header
            filename = "default.csv"
            if content_disposition:
                # The header will look like 'attachment; filename="Crash_Reporting_-_Drivers_Data.csv"'
                filename = content_disposition.split('filename=')[-1].strip('\"')
            else:
                # Fallback to the URL's basename if no content disposition header exists
                filename = url.split('/')[-1].split('?')[0]

            save_path = os.path.join("../data/Downloads/")
            os.makedirs(save_path, exist_ok=True)
            file_name = os.path.join(save_path, filename)

            # Download the file
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                return JsonResponse({'message': f'File downloaded successfully to {file_name}'}, status=200)
            else:
                return JsonResponse({'error': f'Failed to download file. Status code: {response.status_code}'},
                                    status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'Failed to download file: {e}'}, status=500)
        except PermissionError as e:
            return JsonResponse({'error': f'Permission denied: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    # response = requests.get(url)
    # if response.status_code == 200:
    #     content_type = response.headers.get('Content-Type')
    #     if 'zip' in content_type:
    #         with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
    #             zip_ref.extractall(save_path)
    #         return JsonResponse({'message': f'ZIP file downloaded and extracted successfully to {save_path}'}, status=200)
    #     else:
    #         print("saving normal file")
    #         file_name = os.path.join(save_path, os.path.basename(url))
    #         with open(file_name, 'wb') as file:
    #             file.write(response.content)
    #         return JsonResponse({'message': f'File downloaded successfully to {file_name}'}, status=200)
    # else:
    #     return JsonResponse({'error': f'Failed to download file. Status code: {response.status_code}'}, status=500)

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