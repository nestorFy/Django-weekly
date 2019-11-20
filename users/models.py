from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin)

class UserProfile(AbstractUser):
    """
    用户信息
    通过Abstractuser 继承 django原有自带的User类
    """
    department_list = (
        ('d00001', 'Development Department'),
        ('d00002', 'Operation and maintenance Department'),
        ('d00003', 'Product Department'),
        ('d00004', 'Testing Division')
    )

    position_list = (
        ('p00001', 'Boos'),
        ('p00002', 'Manager'),
        ('p00003', 'workers')
    )

    department = models.CharField('Department', max_length=150,choices=department_list ,default='d00001')
    position = models.CharField('Position', max_length=100,choices=position_list, default='p00003')

    class Meta:
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username



