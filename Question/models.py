from django.db import models


class QuestionTbl(models.Model):
    user = models.ForeignKey('Report.UserTbl', models.DO_NOTHING)
    email = models.CharField(max_length=30)
    description = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'question_tbl'
