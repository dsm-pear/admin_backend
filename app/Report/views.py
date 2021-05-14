from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from core.models import AdminTbl
from User.services import JWTService
from .serializers import DetailSerializer, ListSerializer, \
    CommentSerializer, RequestSerializer, DenySerializer
from core.models import ReportTbl, CommentTbl, UserTbl, MemberTbl, ReportTypeTbl
from .exceptions import InvalidSort
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
                ids = ReportTypeTbl.objects.filter(type='SOLE').values_list('report_id', flat=True).distinct()
                print(list(ids))
                queryset = ReportTbl.objects.filter(pk__in=list(ids))\
                    .filter(is_accepted=1).filter(is_submitted=1)
                return queryset
            elif filter == 'TEAM':
                ids = ReportTypeTbl.objects.filter(type='TEAM').values_list('report_id', flat=True).distinct()
                print(list(ids))
                queryset = ReportTbl.objects.filter(pk__in=list(ids)) \
                    .filter(is_accepted=1).filter(is_submitted=1)
                return queryset
            elif filter == 'CIRCLE':
                ids = ReportTypeTbl.objects.filter(type='CIRCLE').values_list('report_id', flat=True).distinct()
                print(list(ids))
                queryset = ReportTbl.objects.filter(pk__in=list(ids)) \
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
