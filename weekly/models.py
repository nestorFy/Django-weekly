from django.db import models

# project information table
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField('ProjectName', max_length=128)
    start_date = models.DateField('ProjectStartTime')
    end_date = models.DateField('ProjectEndTime')
    project_create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "my_project"

class ConfWeekly(models.Model):
    id = models.AutoField(primary_key=True)
    weekly_no = models.CharField(max_length=32)
    weekly_cycle = models.CharField(max_length=64)
    create_no_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conf_weekly"
        ordering = ['-weekly_cycle']
        unique_together = ('weekly_no', 'weekly_cycle')

class WeeklyInfo(models.Model):
    """周报记录表"""
    id = models.AutoField(primary_key=True)
    weekly_cycle = models.CharField(max_length=100)
    username = models.CharField(max_length=64)
    completed_in_this_week = models.TextField()
    working_plan_for_next_week = models.TextField()
    new_issue = models.TextField()
    submit_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "weekly_info"
        unique_together = ('weekly_cycle', 'username')