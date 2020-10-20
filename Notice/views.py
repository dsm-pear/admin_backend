from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from User.models import AdminTbl
from User.services import JWTService
from .serializers import NoticeSerializer
from .models import NoticeTbl


class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = NoticeSerializer

    def get_queryset(self, *args, **kwargs):
        pk = JWTService.run_auth_process(self.request.headers)
        if len(AdminTbl.objects.filter(id=pk).values()):
            queryset = NoticeTbl.objects.all()
            return queryset
        Response({"message": "User didn't exist."}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        pk = JWTService.run_auth_process(self.request.headers)
        admin = AdminTbl.objects.get(id=pk)
        serializer.save(admin=admin)


notice_list = NoticeViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

notice_detail = NoticeViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})
