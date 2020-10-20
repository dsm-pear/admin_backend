# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ReportTbl(models.Model):
    user = models.ForeignKey('UserTbl', models.DO_NOTHING)
    description = models.CharField(max_length=150)
    access = models.CharField(max_length=5)
    type = models.CharField(max_length=4)
    grade = models.CharField(max_length=9)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.IntegerField()
    stars = models.IntegerField()
    languages = models.CharField(max_length=11, blank=True, null=True)
    report_tblcol = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_tbl'


class UserTbl(models.Model):
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=36)
    name = models.CharField(max_length=12)
    self_intro = models.CharField(max_length=200, blank=True, null=True)
    auth_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_tbl'


class CommentTbl(models.Model):
    report = models.ForeignKey('ReportTbl', models.DO_NOTHING)
    user_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'comment_tbl'


class TeamTbl(models.Model):
    report = models.ForeignKey('ReportTbl', models.DO_NOTHING)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'team_tbl'


class MemberTbl(models.Model):
    team = models.ForeignKey('TeamTbl', models.DO_NOTHING)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'member_tbl'