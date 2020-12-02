from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from app.Notice import NoticeTbl
from app.Notice import NoticeSerializer
from app.User import AdminTbl


LIST_URL = reverse('Notice:list')
AUTH_URL = reverse('User:auth')


def get_access_token():
    payload = {'email': 'test@test.com', 'password': 'testpass'}
    AdminTbl.objects.create_user(**payload)
    res = APIClient().post(AUTH_URL, payload)
    return res.data['access_token']


def get_refresh_token():
    payload = {'email': 'test@test.com', 'password': 'testpass'}
    AdminTbl.objects.create_user(**payload)
    res = APIClient().post(AUTH_URL, payload)
    return res.data['refresh_token']


def detail_url(notice_id):
    """Return notice detail URL"""
    return reverse('Notice:detail', args=[notice_id])


def sample_notice(title='test title', description='description'):
    """Create and return a sample Notice"""
    return NoticeTbl.objects.create(title=title,
                                    description=description)


class PublicApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_incorrect_access_token(self):
        """Test that access_token is incorrect"""
        self.client.credentials(HTTP_AUTHORIZATION=get_refresh_token())
        res = self.client.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)


class PrivateNoticeApiTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_list_recipe(self):
        """Test a list of notices"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        sample_notice()

        res = self.client.get(LIST_URL)
        recipes = NoticeTbl.objects.all().order_by('-id')
        serializer = NoticeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    # def test_post_recipe(self):
    #     """Test creating a notice"""
    #     self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
    #
    #     self.id = AdminTbl.objects.get(email='test@test.com').id
    #     payload = {
    #         'id': self.id,
    #         'title': 'test title',
    #         'description': 'description'
    #     }
    #     res = self.client.post(LIST_URL, payload)
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     recipe = NoticeTbl.objects.get(id=res.data['id'])
    #     recipes = NoticeTbl.objects.all()
    #     self.assertIn(recipe, recipes)

    def test_retrieve_notice(self):
        """Test retrieving detail notice"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        notice = sample_notice()

        url = detail_url(notice.id)
        res = self.client.get(url)

        serializer = NoticeSerializer(notice)
        self.assertEqual(res.data['description'],
                         serializer.data['description'])

    def test_partial_update_notice(self):
        """Test partial update notice"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        notice = sample_notice()

        payload = {'title': 'changed title'}
        url = detail_url(notice.id)
        self.client.patch(url, payload)

        notice.refresh_from_db()
        self.assertEqual(notice.title, payload['title'])
