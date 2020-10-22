from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from User.models import AdminTbl
CREATE_USER_URL = reverse('User:create')
AUTH_URL = reverse('User:auth')
REFRESH_URL = reverse('User:refresh')


def create_user(**params):
    return AdminTbl.objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the usrs API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user with valid user is successful"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
