import requests
from rest_framework import viewsets
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

    def perform_create(self, serializer):
        pk = JWTService.run_auth_process(self.request.headers)
        admin = AdminTbl.objects.get(id=pk)
        serializer.save(admin=admin)

        board_id = NoticeTbl.objects.last().id + 1
        image_list = self.request.FILES.getlist('image_path')
        for image in image_list:
            data = {'email': 'testt@test.com', 'username': 'user', 'password': 'password'}
            URL = 'https://mini-avocat-1.herokuapp.com/users/create/'
            headers = {'Content-Type': 'application/json'}
            res = requests.post(URL, data=data, headers=headers)
            print(res.status_code)



notice_list = NoticeViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

notice_detail = NoticeViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})
