from django.db import models


class ReportTbl(models.Model):
    description = models.CharField(max_length=150)
    access = models.CharField(max_length=5)
    type = models.CharField(max_length=7)
    grade = models.CharField(max_length=9)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.IntegerField()
    languages = models.CharField(max_length=100)
    file_name = models.CharField(max_length=50)
    comment = models.CharField(max_length=100, blank=True, null=True)
    field = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        ordering = ["-id"]
        managed = False
        db_table = 'report_tbl'


class TeamTbl(models.Model):
    name = models.CharField(max_length=50)
    user_email = models.ForeignKey('UserTbl', models.DO_NOTHING, db_column='user_email')
    report = models.ForeignKey('ReportTbl', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'team_tbl'


class MemberTbl(models.Model):
    team = models.ForeignKey('TeamTbl', models.DO_NOTHING)
    user_email = models.ForeignKey('UserTbl', models.DO_NOTHING, db_column='user_email')

    class Meta:
        managed = False
        db_table = 'member_tbl'


class UserTbl(models.Model):
    email = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=36)
    name = models.CharField(max_length=12)
    self_intro = models.CharField(max_length=200, blank=True, null=True)
    auth_status = models.IntegerField()

    class Meta:
        ordering = ["-email"]
        managed = False
        db_table = 'user_tbl'


class CommentTbl(models.Model):
    report = models.ForeignKey('ReportTbl', models.DO_NOTHING)
    created_at = models.DateTimeField()
    content = models.TextField()
    user_email = models.ForeignKey('UserTbl', models.DO_NOTHING, db_column='user_email')

    class Meta:
        ordering = ["-id"]
        managed = False
        db_table = 'comment_tbl'