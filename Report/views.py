from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from User.models import AdminTbl
from User.services import JWTService
from .serializers import DetailSerializer, ListSerializer,\
    CommentSerializer, RequestSerializer
from .models import ReportTbl, CommentTbl, UserTbl


class RequestViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return ListSerializer
        elif self.action == 'retrieve':
            return RequestSerializer
        elif self.action == 'partial_update':
            return RequestSerializer

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
        elif self.action == 'partial_update':
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
        comment = CommentTbl.objects.filter(report_id=reports.id) \
            .get(id=comment)
        comment.delete()
        return Response({"detail": "ok"},
                        status=status.HTTP_200_OK)


class SearchViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            sort = request.GET['sort']
        except ValueError:
            return Response({"detail": "please enter sort"},
                            status=status.HTTP_400_BAD_REQUEST)

        search = request.GET['q']

        if sort == 'title':
            list = ReportTbl.objects.filter(is_accepted=1)\
                .filter(title__contains=search)
            serializer = ListSerializer(list, many=True)
            return Response(serializer.data)
        elif sort == 'user':
            user_pk = UserTbl.objects.filter(name__contains=search)
            list__in = ReportTbl.objects.filter(is_accepted=1)\
                .filter(user__id__in=user_pk.all())
            serializer = ListSerializer(list__in, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "please input correct sort"},
                            status=status.HTTP_400_BAD_REQUEST)


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
    'get': 'retrieve',
    'patch': 'partial_update',
})

search_list = SearchViewSet.as_view({'get': 'list'})

delete_comment = DeleteCommentViewSet.as_view({
    'delete': 'destroy',
})
