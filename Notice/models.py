from django.db import models


class NoticeTbl(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["-id"]
        managed = False
        db_table = 'notice_tbl'
