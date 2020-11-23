from rest_framework import serializers
from .models import ReportTbl, CommentTbl


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportTbl
        fields = ('id', 'title', 'created_at')


class DetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = CommentTbl.objects.filter(report_id=obj.id)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    class Meta:
        model = ReportTbl
        fields = ('id', 'description', 'access', 'type',
                  'grade', 'title', 'created_at', 'is_accepted', 'languages',
                  'comments', 'field', 'file_name')


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportTbl
        fields = ('id', 'description', 'access', 'type',
                  'grade', 'title', 'created_at', 'languages', 'field')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentTbl
        fields = ('id', 'user_email', 'created_at', 'content')
