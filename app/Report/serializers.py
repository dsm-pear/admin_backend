from rest_framework import serializers
from core.models import ReportTbl, CommentTbl, MemberTbl, UserTbl


class ListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        if(obj.type == 'SOLE'):
            member = MemberTbl.objects.get(report_id=obj.id)
            serializer = MemberSerializer(member)
            return serializer.data["name"]
        else:
            return obj.team_name

    class Meta:
        model = ReportTbl
        fields = ('id', 'author', 'title', 'created_at')


class DetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = CommentTbl.objects.filter(report_id=obj.id)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def get_author(self, obj):
        return obj.team_name

    def get_member(self, obj):
        member = MemberTbl.objects.filter(report_id=obj.id)
        serializer = MemberSerializer(member, many=True)
        return serializer.data

    class Meta:
        model = ReportTbl
        fields = ('id', 'description', 'title', 'type',
                  'created_at', 'languages', 'author',
                  'comments', 'member', 'file_name', 'github')


class RequestSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        member = MemberTbl.objects.get(report_id=obj.id)
        serializer = MemberSerializer(member)
        return serializer.data

    class Meta:
        model = ReportTbl
        fields = ('id', 'description', 'title', 'type',
                  'created_at', 'languages', 'author',
                  'file_name', 'github')


class DenySerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportTbl
        fields = ('is_accepted', 'comment')


class CommentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.user_email.name

    class Meta:
        model = CommentTbl
        fields = ('id', 'user_email', 'name', 'created_at', 'content')


class MemberSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.user_email.name

    class Meta:
        model = MemberTbl
        fields = ('user_email', 'name', )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTbl
        fields = ('name', )
