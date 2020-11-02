from django.db import models
from django.conf import settings


class NoticeTbl(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL,
                              models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=100, blank=True, null=True)
    image = models.FileField()

    class Meta:
        ordering = ["-id"]
        managed = False
        db_table = 'notice_tbl'
