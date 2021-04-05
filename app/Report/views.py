from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from core.models import AdminTbl
from User.services import JWTService
from .serializers import DetailSerializer, ListSerializer, \
    CommentSerializer, RequestSerializer, DenySerializer
from core.models import ReportTbl, CommentTbl, UserTbl, MemberTbl
from .exceptions import InvalidSort
# import requests
from app.utils import ScrollPagination


class RequestViewSet(viewsets.ModelViewSet):
    pagination_class = ScrollPagination

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return ListSerializer
        elif self.action == 'retrieve':
            return RequestSerializer
        elif self.action == 'partial_update':
            return DenySerializer

    # def partial_update(self, request, *args, **kwargs):
    #     data = {'board_id': '',
    #             'accepted': '',
    #             'body': '',
    #             'email': ''}
    #     URL = 'http://20.55.121.118:8000/email/notification'
    #     headers = {'Content-Type': 'application/json'}
    #     res = requests.post(URL, data=data, headers=headers)
    #     print(res.status_code)
    #     return Response(status=status.HTTP_200_OK)

    def get_queryset(self, *args, **kwargs):
        pk = JWTService.run_auth_process(self.request.headers)
        if len(AdminTbl.objects.filter(id=pk).values()):
            queryset = ReportTbl.objects.filter(is_accepted=0)\
                .filter(comment__isnull=True)\
                .filter(is_submitted=1)
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
            queryset = ReportTbl.objects.filter(is_accepted=1)\
                .filter(is_submitted=1)
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
        pk = JWTService.run_auth_process(self.request.headers)
        if len(AdminTbl.objects.filter(id=pk).values()):
            if 'q' not in self.request.GET:
                raise InvalidSort

            sort = self.request.GET['sort']
            search = self.request.GET['q']
            report_ids = []

            if sort == 'title':
                queryset = ReportTbl.objects.filter(is_accepted=1) \
                    .filter(title__contains=search)\
                    .filter(is_submitted=1)
                return queryset
            elif sort == 'user':
                queryset = ReportTbl.objects.filter(is_accepted=1) \
                    .filter(team_name__contains=search)\
                    .filter(is_submitted=1)
                users = UserTbl.objects.filter(name__contains=search)
                for user in users:
                    members = MemberTbl.objects.filter(user_email=user.email)
                    for member in members:
                        report_ids.append(member.report_id)

                for report_id in report_ids:
                    report = ReportTbl.objects.filter(is_accepted=1) \
                        .filter(id=report_id)\
                        .filter(is_submitted=1)
                    queryset = queryset | report
                return queryset
            else:
                raise InvalidSort


class FilterViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return ListSerializer

    def get_queryset(self):
        pk = JWTService.run_auth_process(self.request.headers)
        if len(AdminTbl.objects.filter(id=pk).values()):
            if 'q' not in self.request.GET:
                raise InvalidSort

            filter = self.request.GET['q']

            if filter == '2021':
                queryset = ReportTbl.objects\
                    .filter(created_at__startswith='2021')\
                    .filter(is_accepted=1).filter(is_submitted=1)
                return queryset
            elif filter == 'SOLE':
                queryset = ReportTbl.objects.filter(type='SOLE')\
                    .filter(is_accepted=1).filter(is_submitted=1)
                return queryset
            elif filter == 'TEAM':
                queryset = ReportTbl.objects.filter(type='TEAM')\
                    .filter(is_accepted=1).filter(is_submitted=1)
                return queryset
            elif filter == 'CIRCLE':
                queryset = ReportTbl.objects.filter(type='CIRCLE')\
                    .filter(is_accepted=1).filter(is_submitted=1)
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

filter_list = FilterViewSet.as_view({'get': 'list'})

delete_comment = DeleteCommentViewSet.as_view({
    'delete': 'destroy',
})
