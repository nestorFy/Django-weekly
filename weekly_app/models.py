# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.

class Employee(models.Model):
    """docstring for employee"""
    department_list = (
        ('D0001', '产品部'),
        ('D0002', '开发部'),
        ('D0003', '运维部'),
        ('D0004', '信息技术部'),
        ('D0003', '其他'),
    )
    company_list = (
        ('C0001', '北京中科云链信息技术有限公司'),
        ('C0002', '北京合力中税信息技术有限公司'),
    )
    personnel_role = (
        ('R0001', '职员'),
        ('R0002', '部门领导'),
        ('R0003', '领导'),
        ('R0004', '管理员'),
    )

    company_name = models.CharField('company', max_length=1, choices=company_list)
    department = models.CharField('department', max_length=1, choices=department_list)
    role = models.CharField('role', max_length=1, choices=personnel_role)
    username = models.CharField('username', max_length=100)
    email = models.CharField('email', max_length=500, primary_key=True)
    password = models.CharField('password', max_length=64, default='A111111')

    def __unicode__(self):
        return self.username

    class Meta:
        db_table = "employee"
        # unique_together = ["account", "password"]


# Weekly information configurtion table
class ConfigWeekly(models.Model):
    """"""
    status = (
        ('0', 'Enable'),
        ('1', 'Disable'),
    )
    weeklyNumber = models.CharField(
        'weeklyNumber', max_length=40, primary_key=True)
    timeLimit = models.CharField('timeLimit', max_length=64)
    weeklySubmit = models.CharField(
        'weeklySubmit', max_length=1, choices=status)


# project information table
class Project(models.Model):
    project_number = models.CharField('ProjectNumber', max_length=64, primary_key=True)
    project_name = models.CharField('ProjectName', max_length=128)
    project_start_time = models.DateField('ProjectStartTime')
    project_end_time = models.DateField('ProjectEndTime')

    class Meta:
        db_table = "my_project"


# # Weekly Data table (Improve version)
class WeeklyRecords(models.Model):
    weeklyNumber = models.CharField('weeklyNumber', max_length=40)
    timeLimit = models.CharField('timeLimit', max_length=64)
    department = models.CharField('department', max_length=100)
    username = models.CharField('username', max_length=100)
    work_this_week = models.TextField('本周工作', max_length=500)
    next_week_plan = models.CharField('下周计划', max_length=500)
    problems_in_work = models.CharField('存在问题', max_length=500)
    weekly_submit_time = models.DateTimeField('提交时间', auto_now=True)

    class Meta:
        db_table = "weekly_records"
        unique_together = ('weeklyNumber', 'timeLimit', 'department', 'username')
