import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Project, ConfWeekly
from .forms import ProjectForm, ConfWeeklyForm
from users.models import UserProfile
from users.forms import UserForm

from django.contrib.auth.decorators import login_required

# @login_required
def index(request):

    return render(request, 'weekly/index.html')
@login_required
class ProjectView(ListView):
    """
    显示项目列表，展示所有项目数据
    """
    template_name = 'weekly/project.html'
    context_object_name = "project_list"
    model = Project

class ProjectCreateView(CreateView):
    """创建项目"""
    form_class = ProjectForm
    template_name = 'weekly/project_add.html'
    success_url = '/project/'

    def form_invalid(self, form):
        # 对表单进行验证，返回错误信息
        error = "请填写完整的项目信息！"
        return render(self.request, 'weekly/project_add.html', {"error": error, })

class ProjectUpdateView(UpdateView):
    """编辑项目信息"""
    context_object_name = 'project'
    form_class = ProjectForm
    model = Project
    template_name = 'weekly/project_update.html'
    success_url = '/project/'

    def get_object(self, queryset=None):
        # 我也搞不清这是在做什么，但是有这个有结果，在此记录下
        obj = Project.objects.get(id=self.kwargs['project_id'])
        return obj

class ProjectDeleteView(DeleteView):
    """删除项目"""
    model = Project
    success_url = reverse_lazy('weekly:project')


class ConfWeeklyView(ListView):
    """周报配置浏览页面"""
    model = ConfWeekly
    template_name = "weekly/conf_weekly.html"
    context_object_name = 'conf_list'

class ConfWeeklyCreateView(CreateView):
    """增加一条将要写的周报记录"""
    form_class = ConfWeeklyForm
    template_name = "weekly/conf_weekly_form.html"
    success_url = '/conf_weekly/'
