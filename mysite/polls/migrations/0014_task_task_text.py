# Generated by Django 3.1.2 on 2020-10-11 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20201011_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_text',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]