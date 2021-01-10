from rest_framework import viewsets
from core.models import AdminTbl
from User.services import JWTService
from .serializers import QuestionSerializer
from core.models import QuestionTbl
from app.utils import ScrollPagination


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    pagination_class = ScrollPagination

    def get_queryset(self, *args, **kwargs):
        pk = JWTService.run_auth_process(self.request.headers)
        if len(AdminTbl.objects.filter(id=pk).values()):
            queryset = QuestionTbl.objects.all()
            return queryset


questions = QuestionViewSet.as_view({
    'get': 'list',
})

question_detail = QuestionViewSet.as_view({
    'delete': 'destroy',
})
