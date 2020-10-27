from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from Report.models import UserTbl, ReportTbl, CommentTbl
from Report.serializers import ListSerializer, DetailSerializer
from User.models import AdminTbl


REQUEST_URL = reverse('Report:request')
LIST_URL = reverse('Report:list')
AUTH_URL = reverse('User:auth')


def get_access_token():
    payload = {'email': 'test@test.com', 'password': 'testpass'}
    AdminTbl.objects.create_user(**payload)
    res = APIClient().post(AUTH_URL, payload)
    return res.data['access_token']


def reqeust_detail_url(request_id):
    """Return notice detail URL"""
    return reverse('Report:request-detail', args=[request_id])


def list_detail_url(list_id):
    """Return notice detail URL"""
    return reverse('Report:list-detail', args=[list_id])


def create_user():
    return UserTbl.objects.create(email='test@test.com', password='testpass',
                                  name='username', auth_status='1')


def sample_request():
    """Create and return a sample Notice"""
    return ReportTbl.objects.create(user_id=create_user().id,
                                    description='description',
                                    access='admin', type='team',
                                    grade='1Grade', title='title',
                                    is_accepted='0', languages='Python')


def sample_list():
    """Create and return a sample Notice"""
    return ReportTbl.objects.create(user_id=create_user().id,
                                    description='description',
                                    access='admin', type='team',
                                    grade='1Grade', title='title',
                                    is_accepted='1', languages='Python')


def sample_comment(report_id):
    """Create and return a sample comment"""
    return CommentTbl.objects.create(report_id=report_id,
                                     content='content',
                                     user_id=create_user().id)


class PublicApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required_reqeust(self):
        """Test that authentication is required"""
        res = self.client.get(REQUEST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_list(self):
        """Test that authentication is required"""
        res = self.client.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateNoticeApiTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_list_request_list(self):
        """Test a list of requests"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        sample_request()

        res = self.client.get(REQUEST_URL)
        reports = ReportTbl.objects.filter(is_accepted=0)
        serializer = ListSerializer(reports, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_list_requests_with_list(self):
        """Test a list of requests"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        sample_request()
        sample_list()

        res = self.client.get(REQUEST_URL)
        self.assertEqual(res.data['count'], 1)

    def test_retrieve_request(self):
        """Test retrieving detail request"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        request = sample_request()

        url = reqeust_detail_url(request.id)
        res = self.client.get(url)

        serializer = DetailSerializer(request)
        self.assertEqual(res.data['description'],
                         serializer.data['description'])

    def test_list_lists(self):
        """Test a list of lists"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        sample_list()

        res = self.client.get(LIST_URL)
        reports = ReportTbl.objects.all()
        serializer = ListSerializer(reports, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_list_with_request(self):
        """Test a list of lists"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        sample_list()
        sample_request()

        res = self.client.get(LIST_URL)
        self.assertEqual(res.data['count'], 1)

    def test_retrieve_list(self):
        """Test retrieving detail list"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        list = sample_list()

        url = list_detail_url(list.id)
        res = self.client.get(url)
        serializer = DetailSerializer(list)
        self.assertEqual(res.data['description'],
                         serializer.data['description'])

    def test_retrieve_comment_in_list(self):
        """Test retrieving detail list with a comment"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        list = sample_list()
        sample_comment(list.id)
        serializer = DetailSerializer(list)
        self.assertNotEqual(serializer.data['comments'], [])
