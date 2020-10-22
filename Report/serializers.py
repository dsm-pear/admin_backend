from rest_framework import serializers
from .models import ReportTbl, CommentTbl


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportTbl
        fields = ('id', 'title', 'created_at')


class DetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportTbl
        fields = ('id', 'user', 'description', 'access', 'type',
                  'grade', 'title', 'created_at', 'is_accepted',
                  'stars', 'languages')


class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()

    class Meta:
        model = CommentTbl
        fields = ('report_id', 'id', 'user_id', 'created_at', 'content')
        # read_only_fields = ['user']
