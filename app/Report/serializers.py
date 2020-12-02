from rest_framework import serializers
from core.models import ReportTbl, CommentTbl, TeamTbl, MemberTbl, UserTbl


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportTbl
        fields = ('id', 'title', 'created_at')


class DetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = CommentTbl.objects.filter(report_id=obj.id)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def get_team(self, obj):
        team = TeamTbl.objects.get(report_id=obj.id)
        serializer = TeamSerializer(team)
        return serializer.data

    def get_member(self, obj):
        if obj.type == 'SOLE':
            member = TeamTbl.objects.get(report_id=obj.id)
            serializer = MemberSerializer(member)
            return serializer.data
        elif obj.type == "TEAM" or obj.type == "CIRCLES":
            team = TeamTbl.objects.get(report_id=obj.id).id
            members = MemberTbl.objects.filter(team_id=team)
            serializer = MemberSerializer(members, many=True)
            return serializer.data

    class Meta:
        model = ReportTbl
        fields = ('id', 'description', 'access', 'type',
                  'grade', 'title', 'created_at', 'languages',
                  'comments', 'field', 'team', 'member', 'file_name', 'github')


class RequestSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()

    def get_team(self, obj):
        team = TeamTbl.objects.get(report_id=obj.id)
        serializer = TeamSerializer(team)
        return serializer.data

    def get_member(self, obj):
        if obj.type == 'SOLE':
            member = TeamTbl.objects.get(report_id=obj.id)
            serializer = MemberSerializer(member)
            return serializer.data
        elif obj.type == "TEAM" or obj.type == "CIRCLES":
            team = TeamTbl.objects.get(report_id=obj.id).id
            members = MemberTbl.objects.filter(team_id=team)
            serializer = MemberSerializer(members, many=True)
            return serializer.data

    class Meta:
        model = ReportTbl
        fields = ('id', 'description', 'access', 'type',
                  'grade', 'title', 'created_at', 'languages',
                  'field', 'team', 'member', 'github')


class DenySerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportTbl
        fields = ('is_accepted', 'comment')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentTbl
        fields = ('id', 'user_email', 'created_at', 'content')


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamTbl
        fields = ('name', )


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
