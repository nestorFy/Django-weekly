# Generated by Django 2.2.5 on 2019-09-30 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='department',
            field=models.CharField(default='', max_length=150, verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='position',
            field=models.CharField(default='', max_length=100, verbose_name='Position'),
        ),
    ]