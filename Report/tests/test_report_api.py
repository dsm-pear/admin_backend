import json

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from Report.models import UserTbl, ReportTbl, CommentTbl
from Report.serializers import ListSerializer, DetailSerializer
from User.models import AdminTbl


REQUEST_URL = reverse('Report:request')
LIST_URL = reverse('Report:list')
SEARCH_URL = reverse('Report:search_list')
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


def comments_detail_url(pk, comment):
    """Return notice detail URL"""
    return reverse('Report:delete_comment', args=[pk, comment])


def create_user(name='username'):
    return UserTbl.objects.create(email='test@test.com', password='testpass',
                                  name=name, auth_status='1')


def sample_request():
    """Create and return a sample Notice"""
    return ReportTbl.objects.create(user_id=create_user().id,
                                    description='description',
                                    access='admin', type='team',
                                    grade='1Grade', title='title',
                                    is_accepted='0', languages='Python')


def sample_list(pk=0, title='test title'):
    """Create and return a sample Notice"""
    if pk == 0:
        pk = create_user().id
    return ReportTbl.objects.create(user_id=pk,
                                    description='description',
                                    access='admin', type='team',
                                    grade='1Grade', title=title,
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

    def test_auth_required_retrieve_request(self):
        """Test that authentication is required"""
        request = sample_request()

        url = reqeust_detail_url(request.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_retrieve_list(self):
        """Test that authentication is required"""
        list = sample_list()

        url = list_detail_url(list.id)
        res = self.client.get(url)

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

    def test_retrieve_invalid_request(self):
        """Test retrieving invalid detail request"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())

        url = reqeust_detail_url(0)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_lists(self):
        """Test a list of lists"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())

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

    def test_retrieve_invalid_list(self):
        """Test retrieving invalid detail request"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())

        url = list_detail_url(0)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_comment_in_list(self):
        """Test retrieving detail list with a comment"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        list = sample_list()
        sample_comment(list.id)
        serializer = DetailSerializer(list)
        self.assertNotEqual(serializer.data['comments'], [])

    def test_delete_comment_success(self):
        """Test deleting the comment successful"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        list = sample_list()
        comment = sample_comment(list.id)
        url = comments_detail_url(list.id, comment.id)

        serializer = DetailSerializer(list)
        self.assertNotEqual(serializer.data['comments'], [])

        res = self.client.delete(url)
        self.assertEqual(res.data, {'detail': 'ok'})

        serializer = DetailSerializer(list)
        self.assertEqual(serializer.data['comments'], [])

    def test_delete_invalid_comment(self):
        """Test deleting the invalid comment"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        list = sample_list()
        sample_comment(list.id)
        url = comments_detail_url(list.id, '3')

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_with_title(self):
        """Test searching to title"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        sample_list(title='error')
        list = sample_list()

        serializer = ListSerializer(list)
        res = self.client.get(SEARCH_URL, {'sort': 'title', 'q': 'test title'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)
        self.assertEqual(int(json.dumps(res.data['results'][0]['id'])),
                         serializer.data['id'])

    def test_search_with_user(self):
        """Test searching to title"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        erroruser = create_user('JeongGoEun')
        sample_list(erroruser.id)
        list = sample_list()

        serializer = ListSerializer(list)
        res = self.client.get(SEARCH_URL, {'sort': 'user', 'q': 'username'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)
        self.assertEqual(int(json.dumps(res.data['results'][0]['id'])),
                         serializer.data['id'])

    def test_search_with_invalid_sort(self):
        """Test searching with invalid sort"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        res = self.client.get(SEARCH_URL, {'sort': '', 'q': ''})

        self.assertIn('detail', res.data)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_request(self):
        """Test updating request"""
        self.client.credentials(HTTP_AUTHORIZATION=get_access_token())
        request = sample_request()

        url = reqeust_detail_url(request.id)
        payload = {'is_accepted': '0', 'comment': '구리네요'}
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
