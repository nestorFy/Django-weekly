import datetime
import time

from django import forms
from django.shortcuts import render

from .models import Project, ConfWeekly


def field(request):
    if request.method == 'GET':
        obj = forms.FieldForm()
        return render(request, 'field.html', {'obj': obj})
    elif request.method == 'POST':
        obj = forms.FieldForm(request.POST, request.FILES)
        obj.is_valid()
        print(obj.clean())
        print(obj.errors.as_json())
        return render(request, 'field.html', {'obj': obj})


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'start_date', 'end_date', ]
        labels = {'project_name': '', 'start_date': '', 'end_date': '', }


class ConfWeeklyForm(forms.ModelForm):
    # 获取时间、周期
    cur_date = datetime.datetime.now()
    day_num = cur_date.isoweekday()
    weekly_start_date = (cur_date - datetime.timedelta(days=day_num)).strftime('%Y%m%d')
    weekly_end_date = (cur_date - datetime.timedelta(days=day_num - 5)).strftime('%Y%m%d')
    cycle_value = str(weekly_start_date) + '-' + str(weekly_end_date)
    cur_cycle = time.strftime("%W")
    # 初始化页面值
    weekly_no = forms.CharField(label="Weekly Number", initial=cur_cycle,
                                widget=forms.TextInput(attrs={"class": 'form-control'}))
    weekly_cycle = forms.CharField(label="Weekly Cycle", initial=cycle_value,
                                   widget=forms.TextInput(attrs={"class": 'form-control'}))


    class Meta:
        model = ConfWeekly
        fields = ['weekly_no', 'weekly_cycle', ]
        labels = {'weekly_no': '', 'weekly_cycle': 'Weekly Cycle', }

        error_messages = "123 error."
