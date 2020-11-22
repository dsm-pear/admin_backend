from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from User.models import AdminTbl
from User.services import JWTService
from .serializers import DetailSerializer, ListSerializer,\
    CommentSerializer, RequestSerializer
from .models import ReportTbl, CommentTbl, UserTbl
from .exceptions import InvalidSort
import requests


class RequestViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return ListSerializer
        elif self.action == 'retrieve' or 'partial_update':
            return RequestSerializer

    def partial_update(self, request, *args, **kwargs):
        data = {'email': 'testt@test.com',
                'username': 'user',
                'password': 'password'}
        URL = 'https://mini-avocat-1.herokuapp.com/users/create/'
        headers = {'Content-Type': 'application/json'}
        res = requests.post(URL, data=data, headers=headers)
        print(res.status_code)
        return Response({"detail": "ok"},
                        status=status.HTTP_200_OK)

    def get_queryset(self, *args, **kwargs):
        pk = JWTService.run_auth_process(self.request.headers)
        if len(AdminTbl.objects.filter(id=pk).values()):
            queryset = ReportTbl.objects.filter(is_accepted=0)
            return queryset


class ListViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return ListSerializer
        elif self.action == 'retrieve':
            return DetailSerializer

    def get_queryset(self, *args, **kwargs):
        pk = JWTService.run_auth_process(self.request.headers)
        if len(AdminTbl.objects.filter(id=pk).values()):
            queryset = ReportTbl.objects.filter(is_accepted=1)
            return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = CommentTbl.objects.all()
    serializer_class = CommentSerializer


class DeleteCommentViewSet(viewsets.ViewSet):

    def destroy(self, request, pk=None, comment=None):
        reports = ReportTbl.objects.get(id=pk)
        try:
            comment = CommentTbl.objects.filter(report_id=reports.id)\
                .get(id=comment)
            comment.delete()
        except CommentTbl.DoesNotExist:
            return Response({"detail": "Not found."},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "ok"},
                        status=status.HTTP_200_OK)


class SearchViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return ListSerializer

    def get_queryset(self):
        sort = self.request.GET['sort']
        search = self.request.GET['q']

        if sort == 'title':
            queryset = ReportTbl.objects.filter(is_accepted=1) \
                .filter(title__contains=search)
            return queryset
        elif sort == 'user':
            user_pk = UserTbl.objects.filter(name__contains=search)
            queryset = ReportTbl.objects.filter(is_accepted=1)\
                .filter(user__id__in=user_pk.all())
            return queryset
        else:
            raise InvalidSort


request_list = RequestViewSet.as_view({
    'get': 'list',
})

request_detail = RequestViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})

list_list = ListViewSet.as_view({
    'get': 'list',
})

list_detail = ListViewSet.as_view({
    'get': 'retrieve'
})

search_list = SearchViewSet.as_view({'get': 'list'})

delete_comment = DeleteCommentViewSet.as_view({
    'delete': 'destroy',
})
