import json

from django.test import TestCase
from .models import Application, Good
from django.test import Client

class ApplicationTests(TestCase):
    def setUp(self):
        good = Good.objects.create(name="testGood")
        app = Application.objects.create(name="testApp", destination="london")
        app.goods.add(good)
        self.c = Client()

    def test_get_applications(self):
        response = self.c.get('/application/')
        self.assertEquals(response.status_code, 200)
        applications = json.loads(response.content.decode('utf-8'))
        self.assertGreater(len(applications), 0)
        for app in applications:
            self.assertTrue("id" in app.keys())
            self.assertTrue("name" in app.keys())
            self.assertTrue("date" in app.keys())
            self.assertTrue("destination" in app.keys())
            self.assertTrue("goods" in app.keys())

    def test_create_application(self):
        response = self.c.post('/application/', { "name": "abc", "destination": "abc", "goods": ['1'] }, content_type="application/json")
        self.assertEquals(response.status_code, 201)
