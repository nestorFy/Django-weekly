# Generated by Django 2.2.5 on 2019-09-25 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weekly', '0004_weeklyconf_weeklyinfo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WeeklyConf',
            new_name='ConfWeekly',
        ),
    ]