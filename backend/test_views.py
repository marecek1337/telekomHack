from django.test import TestCase, Client
from django.urls import reverse
import json
import os
import shutil

class TodoViewTests(TestCase):
    def setUp(self):
        # If the storage directory doesn't exist, create it
        os.makedirs('storage', exist_ok=True)
        self.client = Client()

    def tearDown(self):
        # Delete everything in the storage directory after each test
        for filename in os.listdir('storage'):
            file_path = os.path.join('storage', filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        print("Cleanup: Storage directory cleared after the test.")

    def test_create_todo(self):
        print("\nTesting: Create ToDo")
        url = reverse('create_todo')
        data = {
            'name': 'Grocery Shopping',
            'message': 'Buy milk, bread, and eggs',
            'date': '2024-03-20',
            'completion': False
        }
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        print("Passed: Status Code is 200")

        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Todo item saved successfully')
        self.assertDictEqual(response_data['data'], data)
        print("Passed: ToDo item saved successfully")

        files = os.listdir('storage')
        self.assertEqual(len(files), 1)
        with open(os.path.join('storage', files[0]), 'r') as file:
            file_data = json.load(file)
        self.assertDictEqual(file_data, data)
        print("Passed: ToDo item file created with correct data")

    def test_invalid_json(self):
        print("\nTesting: Invalid JSON Submission")
        url = reverse('create_todo')
        response = self.client.post(url, '{"name": "Incomplete JSON"', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        print("Passed: Correctly handled invalid JSON")

    def test_wrong_method(self):
        print("\nTesting: Wrong Method GET instead of POST")
        url = reverse('create_todo')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        print("Passed: Correctly handled wrong method with 405 Response")
