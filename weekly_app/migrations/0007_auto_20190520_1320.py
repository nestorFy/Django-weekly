# Generated by Django 2.2 on 2019-05-20 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weekly_app', '0006_weeklyrecords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklyrecords',
            name='work_this_week',
            field=models.TextField(max_length=500, verbose_name='本周工作'),
        ),
    ]
