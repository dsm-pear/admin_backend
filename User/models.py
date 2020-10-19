# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from .services import HashService


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, password=HashService.hash_string_to_password(password))
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None):
        return self._create_user(email, password)


class AdminTbl(models.Model):
    id = models.IntegerField(primary_key=True)
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

    def __str__(self):
        return self.email
