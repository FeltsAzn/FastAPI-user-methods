from unittest import TestCase
from fastapi.testclient import TestClient

from app.main import app as web_app
from app.config import DATABASE_URL


class APITestcase(TestCase):

    def setUp(self):
        self.client = TestClient(web_app)

    def test_main_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    #def test_user_create(self):
        # user_data = {
        #     "user": {
        #         "email": "timkin@mail.ru",
        #         "password": "Nbveh1999"
        #     }
        # }
        # response = self.client.post('/user/create', json=user_data)
        # self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        user_data = {
            "user_form": {
                "email": "timkin@mail.ru",
                "password": "Nbveh1999"
            }
        }
        response = self.client.post('/user/login', json=user_data)
        self.assertEqual(response.status_code, 200)

    # TODO поднимать базу для тестирования фунцкий
