# Generated by Django 3.1.2 on 2020-10-11 01:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20201010_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 10, 21, 18, 3, 848379)),
        ),
        migrations.AddField(
            model_name='task',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 10, 21, 18, 3, 848346)),
        ),
    ]
