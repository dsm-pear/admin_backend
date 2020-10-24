from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from User.models import AdminTbl
from User.services import JWTService
from .serializers import QuestionSerializer
from .models import QuestionTbl


class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self, *args, **kwargs):
        pk = JWTService.run_auth_process(self.request.headers)
        if len(AdminTbl.objects.filter(id=pk).values()):
            queryset = QuestionTbl.objects.get_queryset().order_by('id')
            return queryset
        Response({"message": "User didn't exist."},
                 status=status.HTTP_400_BAD_REQUEST)


questions = NoticeViewSet.as_view({
    'get': 'list',
})
