# Generated by Django 2.2 on 2020-10-27 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Question', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questiontbl',
            options={'managed': False, 'ordering': ['-id']},
        ),
    ]