# Generated by Django 3.1.2 on 2020-10-12 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_task_task_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='weekday',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Monday', max_length=10),
        ),
    ]