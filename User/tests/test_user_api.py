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


def get_refresh_token():
    payload = {'email': 'test@test.com', 'password': 'testpass'}
    create_user(**payload)
    res = APIClient().post(AUTH_URL, payload)
    return res.data['refresh_token']


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user with valid user is successful"""
        payload = {'email': 'test@test.com', 'password': 'testpass'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test@test.com', 'password': 'testpass'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertIn('message', res.data)
        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@test.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(AUTH_URL, payload)

        self.assertIn('access_token', res.data)
        self.assertIn('refresh_token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email="test@test.com", password="testpass")
        payload = {'email': 'test@test.com', 'password': 'wrong'}
        res = self.client.post(AUTH_URL, payload)

        self.assertIn('message', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@test.com', 'password': 'testpass'}
        res = self.client.post(AUTH_URL, payload)

        self.assertIn('message', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_none(self):
        """Test that access_token is created again"""
        res = self.client.post(REFRESH_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_refresh_success(self):
        """Test that access_token is created again"""
        self.client.credentials(HTTP_AUTHORIZATION=get_refresh_token())
        res = self.client.post(REFRESH_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
