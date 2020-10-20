from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from User.models import AdminTbl
from User.services import JWTService
from .serializers import DetailSerializer, ListSerializer, CommentSerializer
from .models import ReportTbl, CommentTbl


class RequestViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return ListSerializer
        elif self.action == 'retrieve':
            return DetailSerializer

        return self.serializer_class

    def get_queryset(self, *args, **kwargs):
        pk = JWTService.run_auth_process(self.request.headers)
        if len(AdminTbl.objects.filter(id=pk).values()):
            queryset = ReportTbl.objects.filter(is_accepted=0)
            return queryset
        Response({"message": "User didn't exist."}, status=status.HTTP_400_BAD_REQUEST)


class ListViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return ListSerializer
        elif self.action == 'retrieve':
            return DetailSerializer

        return self.serializer_class

    def get_queryset(self, *args, **kwargs):
        pk = JWTService.run_auth_process(self.request.headers)
        if len(AdminTbl.objects.filter(id=pk).values()):
            queryset = ReportTbl.objects.filter(is_accepted=0)
            return queryset
        Response({"message": "User didn't exist."}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = CommentTbl.objects.all()
    serializer_class = CommentSerializer


request_list = RequestViewSet.as_view({
    'get': 'list',
})

request_detail = RequestViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    # 'delete': 'destroy',
})

list_list = ListViewSet.as_view({
    'get': 'list',
})

list_detail = ListViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    # 'delete': 'destroy',
})
