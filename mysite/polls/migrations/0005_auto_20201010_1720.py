# Generated by Django 3.1.2 on 2020-10-10 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20201010_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]