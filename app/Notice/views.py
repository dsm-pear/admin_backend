# import requests
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
        if len(AdminTbl.objects.filter(id=pk).values()):
            serializer.save()
            # if NoticeTbl.objects.last() == None:
            #     notice_id = 1
            # else:
            #     notice_id = NoticeTbl.objects.last().id + 1

            # file = self.request.data['file']
            # print(file)
            # data = {'noticeFile': file}
            # URL = f'http://3.18.113.20:3000/notice/files/{notice_id}'
            # res = requests.post(URL, data=data)
            # print(res.status_code)
            # print(res.content)


notice_list = NoticeViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

notice_detail = NoticeViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})
