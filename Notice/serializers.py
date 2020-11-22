from rest_framework import serializers
from .models import NoticeTbl


class NoticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = NoticeTbl
        fields = ('admin', 'id', 'title', 'description', 'created_at', 'path')
