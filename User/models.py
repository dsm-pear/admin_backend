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
