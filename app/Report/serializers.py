from rest_framework import serializers
from core.models import ReportTbl, CommentTbl, MemberTbl,\
    UserTbl, ReportTypeTbl, LanguageTbl


class ListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.team_name

    class Meta:
        model = ReportTbl
        fields = ('id', 'author', 'title', 'created_at')


class DetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()
    field = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = CommentTbl.objects.filter(report_id=obj.id)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def get_author(self, obj):
        return obj.team_name

    def get_member(self, obj):
        member = MemberTbl.objects.filter(report=obj.id)
        serializer = MemberSerializer(member, many=True)
        return serializer.data

    def get_access(self, obj):
        report = ReportTypeTbl.objects.get(report=obj.id)
        return report.access

    def get_field(self, obj):
        report = ReportTypeTbl.objects.get(report=obj.id)
        return report.field

    def get_type(self, obj):
        report = ReportTypeTbl.objects.get(report=obj.id)
        return report.type

    def get_grade(self, obj):
        report = ReportTypeTbl.objects.get(report=obj.id)
        return report.grade

    def get_languages(self, obj):
        language = LanguageTbl.objects.filter(report_id=obj.id)
        str = ""
        for lan in language:
            str += lan.languages + ", "
        return str[:-2]

    class Meta:
        model = ReportTbl
        fields = ('id', 'description', 'title', 'type',
                  'created_at', 'author', 'member', 'comments',
                  'github', 'grade', 'access', 'field', 'languages')


class RequestSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()
    field = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.team_name

    def get_access(self, obj):
        report = ReportTypeTbl.objects.get(report=obj.id)
        return report.access

    def get_field(self, obj):
        report = ReportTypeTbl.objects.get(report=obj.id)
        return report.field

    def get_type(self, obj):
        report = ReportTypeTbl.objects.get(report=obj.id)
        return report.type

    def get_grade(self, obj):
        report = ReportTypeTbl.objects.get(report=obj.id)
        return report.grade

    def get_member(self, obj):
        member = MemberTbl.objects.filter(report=obj.id)
        serializer = MemberSerializer(member, many=True)
        return serializer.data

    def get_languages(self, obj):
        language = LanguageTbl.objects.filter(report_id=obj.id)
        str = ""
        for lan in language:
            str += lan.languages + ", "
        return str[:-2]

    class Meta:
        model = ReportTbl
        fields = ('id', 'description', 'title', 'type',
                  'created_at', 'author', 'member',
                  'github', 'grade', 'access', 'field', 'languages')


class DenySerializer(serializers.ModelSerializer):
    is_submitted = serializers.SerializerMethodField()

    def get_is_submitted(self, obj):
        if obj.is_accepted == 1:
            return 1
        elif obj.is_accepted == 0:
            report = ReportTbl.objects.get(id=obj.id)
            report.is_submitted = 0
            report.save()
            return 0

    class Meta:
        model = ReportTbl
        fields = ('is_accepted', 'comment', 'is_submitted')


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
