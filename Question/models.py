from django.db import models


class QuestionTbl(models.Model):
    email = models.CharField(max_length=30)
    description = models.CharField(max_length=150)

    class Meta:
        ordering = ['-id']
        managed = False
        db_table = 'question_tbl'
