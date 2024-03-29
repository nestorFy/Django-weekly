# Generated by Django 2.2.5 on 2019-09-30 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weekly', '0006_auto_20190925_1529'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='confweekly',
            options={'ordering': ['-weekly_cycle']},
        ),
        migrations.AlterUniqueTogether(
            name='confweekly',
            unique_together={('weekly_no', 'weekly_cycle')},
        ),
        migrations.AlterUniqueTogether(
            name='weeklyinfo',
            unique_together={('weekly_cycle', 'username')},
        ),
    ]
