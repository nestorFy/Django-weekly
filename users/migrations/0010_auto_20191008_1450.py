# Generated by Django 2.2.5 on 2019-10-08 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='department',
            field=models.CharField(choices=[('d00001', 'Development Department'), ('d00002', 'Operation and maintenance Department'), ('d00003', 'Product Department'), ('d00004', 'Testing Division')], default='d00001', max_length=150, verbose_name='Department'),
        ),
    ]
