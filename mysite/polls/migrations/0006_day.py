# Generated by Django 3.1.2 on 2020-10-10 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20201010_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbreviation', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
    ]
