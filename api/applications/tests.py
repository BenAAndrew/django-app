import json

from django.test import TestCase
from .models import Application, Good
from django.test import Client

GOOD_NAME = "testGood"
APP_NAME = "testApp"
APP_DEST = "london"

class ApplicationTests(TestCase):
    def setUp(self):
        app = Application.objects.create(name=APP_NAME, destination=APP_DEST)
        app.goods.add(Good.objects.create(name=GOOD_NAME))
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
        response = self.c.get('/application/')
        applications = json.loads(response.content.decode('utf-8'))
        self.assertGreater(len(applications), 1)

    def test_create_application_fails(self):
        response = self.c.post('/application/', {"name": "abc", "destination": "abc"}, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_get_application_detail(self):
        response = self.c.get('/application/1/')
        self.assertEquals(response.status_code, 200)
        application = json.loads(response.content.decode('utf-8'))
        self.assertEquals(application["id"], 1)
        self.assertEquals(application["name"], APP_NAME)
        self.assertIsNotNone(application["date"])
        self.assertEquals(application["destination"], APP_DEST)
        self.assertEquals(application["goods"][0], 1)

    def test_get_invalid_application_detial(self):
        response = self.c.get('/application/2/')
        self.assertEquals(response.status_code, 404)

    def test_delete_application(self):
        response = self.c.delete('/application/1/')
        self.assertEquals(response.status_code, 204)
        response = self.c.get('/application/')
        applications = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(applications), 0)

class GoodTests(TestCase):
    def setUp(self):
        Good.objects.create(name=GOOD_NAME)
        self.c = Client()

    def test_get_goods(self):
        response = self.c.get('/application/good/')
        self.assertEquals(response.status_code, 200)
        goods = json.loads(response.content.decode('utf-8'))
        self.assertGreater(len(goods), 0)
        for good in goods:
            self.assertTrue("id" in good.keys())
            self.assertTrue("name" in good.keys())

    def test_create_good(self):
        response = self.c.post('/application/good/', {"name": "abc"}, content_type="application/json")
        self.assertEquals(response.status_code, 201)
        response = self.c.get('/application/good/')
        applications = json.loads(response.content.decode('utf-8'))
        self.assertGreater(len(applications), 1)

    def test_create_good_fails(self):
        response = self.c.post('/application/good/', {}, content_type="application/json")
        self.assertEquals(response.status_code, 400)

    def test_get_good_detail(self):
        response = self.c.get('/application/good/1/')
        self.assertEquals(response.status_code, 200)
        good = json.loads(response.content.decode('utf-8'))
        self.assertEquals(good["id"], 1)
        self.assertEquals(good["name"], GOOD_NAME)

    def test_get_invalid_good_detail(self):
        response = self.c.get('/application/good/2/')
        self.assertEquals(response.status_code, 404)

    def test_delete_good(self):
        response = self.c.delete('/application/good/1/')
        self.assertEquals(response.status_code, 204)
        response = self.c.get('/application/good/')
        goods = json.loads(response.content.decode('utf-8'))
        self.assertEquals(len(goods), 0)
