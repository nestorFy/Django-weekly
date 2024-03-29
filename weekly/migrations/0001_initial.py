# Generated by Django 2.2.5 on 2019-09-23 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_number', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='ProjectNumber')),
                ('project_name', models.CharField(max_length=128, verbose_name='ProjectName')),
                ('project_start_time', models.DateField(verbose_name='ProjectStartTime')),
                ('project_end_time', models.DateField(verbose_name='ProjectEndTime')),
            ],
            options={
                'db_table': 'my_project',
            },
        ),
    ]
