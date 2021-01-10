from django.db import models
from django.contrib.auth.models import BaseUserManager
from .services import HashService


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password):
        email = self.normalize_email(email)
        user = self.model(email=email,
                          password=HashService.hash_string_to_password(
                              password))
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None):
        return self._create_user(email, password)


class AdminTbl(models.Model):
    email = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=64)

    objects = UserManager()

    is_anonymous = None
    is_authenticated = None

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    class Meta:
        managed = False
        db_table = 'admin_tbl'


class ReportTbl(models.Model):
    description = models.CharField(max_length=150)
    access = models.CharField(max_length=5)
    field = models.CharField(max_length=8)
    type = models.CharField(max_length=7)
    grade = models.CharField(max_length=9)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.IntegerField()
    is_submitted = models.IntegerField()
    languages = models.CharField(max_length=100)
    team_name = models.CharField(max_length=45)
    file_name = models.CharField(max_length=50)
    comment = models.CharField(max_length=100, blank=True, null=True)
    github = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["-id"]
        managed = False
        db_table = 'report_tbl'


class MemberTbl(models.Model):
    user_email = models.ForeignKey('UserTbl',
                                   models.DO_NOTHING,
                                   db_column='user_email')
    report = models.ForeignKey('ReportTbl', models.DO_NOTHING)

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
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    user_email = models.ForeignKey('UserTbl',
                                   models.DO_NOTHING,
                                   db_column='user_email')

    class Meta:
        ordering = ["-id"]
        managed = False
        db_table = 'comment_tbl'


class NoticeTbl(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["-id"]
        managed = False
        db_table = 'notice_tbl'


class QuestionTbl(models.Model):
    email = models.CharField(max_length=30)
    description = models.CharField(max_length=150)

    class Meta:
        ordering = ["id"]
        managed = False
        db_table = 'question_tbl'
