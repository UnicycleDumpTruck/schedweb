# Generated by Django 3.1.2 on 2020-10-10 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20201010_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='start_time',
            field=models.TimeField(),
        ),
    ]
