from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from Question.models import QuestionTbl
from Question.serializers import QuestionSerializer
from User.models import AdminTbl


LIST_URL = reverse('Question:list')
AUTH_URL = reverse('User:auth')


def get_access_token():
    payload = {'email': 'test@test.com', 'password': 'testpass'}
    AdminTbl.objects.create_user(**payload)
    res = APIClient().post(AUTH_URL, payload)
    return res.data['access_token']


def sample_question():
    """Create and return a sample Question"""
    return QuestionTbl.objects.create(
        email='test@test.com',
        description='description')


class PublicApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateQuestionApiTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_list_question(self):
        """Test a list of notices"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        sample_question()

        res = self.client.get(LIST_URL)
        recipes = QuestionTbl.objects.all().order_by('-id')
        serializer = QuestionSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)
