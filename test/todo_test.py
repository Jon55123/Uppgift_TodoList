import os
import unittest
import sys
import json

sys.path.append("../Todo")

os.environ['APP_SETTINGS'] = "config.TestingConfig"

from Todo import app



class TestCase(unittest.TestCase):
    def setUp(self):

        self.app = app.test_client()

    def add_Todo(self, text, tags=[]):
        data = json.dumps({"text": text,"tags": tags})
        response = self.app.put('/todos', data=data, content_type='application/json')

        return json.loads(response.data), response.status_code

    def delete_todo(self,todo):
        response = self.app.delete('/todo/%s' % todo)

        return response.status_code

    def get_todo(self,todo):
        response = self.app.get('/todo/%s' % todo)

        return json.loads(response.data), response.status_code

    def get_todos(self):
        response = self.app.get('/todos')
        return json.loads(response.data), response.status_code

    def test_add_todo_with_tags(self):
        text = "buy_milk"
        tags = ['coffe','breakfast']
        response,status = self.add_Todo(text,tags=tags)

        self.assertEqual(response['text'], text)
        self.assertEqual(response['tags'], tags)
        self.assertEqual(status, 201)

    def test_add_todo_without_tag(self):
        text = "always buy_milk"
        response,status = self.add_Todo(text)
        tags=[]
        self.assertEqual(response['text'], text)
        self.assertEqual(response['tags'], tags)
        self.assertEqual(status, 201)

    def test_get_todos(self):

        response, status =self.get_todos()
        self.assertEqual(status, 200)

    def test_delete_todo(self):
        text = "always buy_milk"
        response,status = self.add_Todo(text)

        status=self.delete_todo(response['Todo'])
        self.assertEqual(status, 204)

    def test_get_todo(self):
        text = "buy_milk"
        tags=['coffe','breakfast']
        response,status = self.add_Todo(text,tags=tags)

        todo=response['Todo']
        response, status = self.get_todo(todo)

        self.assertEqual(response['Todo'], todo)
        self.assertEqual(response['text'], text)
        self.assertEqual(response['tags'], tags)
        self.assertEqual(status, 200)

    def test_404(self):
        response = self.app.put('/missingpoin')
        self.assertEqual(response.status_code, 404)

    def test_400(self):
        data = json.dumps({"wrong_key": "bla bla"})
        response = self.app.put('/todos', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_415(self):
        data = json.dumps({"text": "bla bal"})
        response = self.app.put('/todos', data=data)
        self.assertEqual(response.status_code, 415)


if __name__ == '__main__':
    unittest.main()