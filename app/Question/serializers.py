from rest_framework import serializers
from .models import QuestionTbl


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionTbl
        fields = ('id', 'email', 'description')
